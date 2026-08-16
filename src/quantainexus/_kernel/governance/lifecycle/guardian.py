"""
QuantAINexus — _kernel/governance/lifecycle/guardian.py

Guardian — the ONLY implementation of LifecycleHook (Article VII §7.2).

CRITICAL DESIGN RULES:
  1. Guardian NEVER raises an exception. It returns HookResult.
  2. LocalRunner reads HookResult.blocking and is the ONLY place that raises
     GuardianBlockedError.
  3. Guardian is injected into LocalRunner via constructor — not hardcoded.
  4. post_execute() is for audit/telemetry only. Wrapped in try/except.

Import policy: typing, governance-internal only. No heavy dependencies.
"""
from __future__ import annotations

from typing import Any, List, Optional

from ..check import CheckResult, GuardianCheck, HookResult


class Guardian:
    """
    Aggregates GuardianCheck instances and exposes pre_execute / post_execute.

    Usage:
        checks = [PITCheck(), SchemaCheck()]
        guardian = Guardian(checks=checks, profile="research")
        runner = LocalRunner(hooks=[guardian])
    """

    def __init__(
        self,
        checks: List[GuardianCheck],
        profile: str = "lab",
    ) -> None:
        self._checks = checks
        self._profile = profile

    # ── LifecycleHook implementation ─────────────────────────────────────

    def pre_execute(
        self,
        node: Any,
        ctx: Any,
    ) -> Optional[HookResult]:
        """
        Run all checks. Return HookResult — NEVER raise.

        Returns HookResult(blocking=True) if any blocking check failed.
        Returns HookResult(blocking=False) if all checks passed.
        """
        results: List[CheckResult] = []

        for check in self._checks:
            try:
                result = check.evaluate(node, ctx)
                results.append(result)
            except Exception as exc:
                # A check itself crashed — treat as a non-blocking warning
                results.append(
                    CheckResult(
                        check_name=check.name,
                        passed=False,
                        blocking=False,
                        message=f"Check raised unexpectedly: {exc!r}",
                    )
                )

        failing_blockers = [r for r in results if r.blocking and not r.passed]

        if failing_blockers:
            return HookResult.block(failing_blockers)

        return HookResult.allow()

    def post_execute(
        self,
        node: Any,
        ctx: Any,
        result: Any,
    ) -> None:
        """
        Audit hook — called after successful execution.
        MUST NOT propagate exceptions.
        """
        try:
            self._audit(node, ctx, result)
        except Exception:
            pass  # telemetry failures must never break the execution path

    def _audit(self, node: Any, ctx: Any, result: Any) -> None:
        """Override or extend in subclasses for custom post-execution auditing."""
        # Default: no-op. Infrastructure observability will be wired here in Phase 2.
        pass

    # ── Profile-aware check loading ──────────────────────────────────────

    @classmethod
    def from_profile(cls, profile: str) -> "Guardian":
        """
        Factory — build a Guardian from a named profile.
        Profiles control which checks are active and their severity.
        """
        from ..checks import load_checks_for_profile
        checks = load_checks_for_profile(profile)
        return cls(checks=checks, profile=profile)
