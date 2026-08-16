"""
QuantAINexus — _kernel/governance/checks/security.py

SecurityCheck — sandbox and import restriction enforcement.
Blocking: True for critical violations (e.g. system calls in node params).
"""
from __future__ import annotations

from typing import Any

from ..check import CheckResult, GuardianCheck

# Modules that are dangerous to import in a sandboxed research environment
_FORBIDDEN_TOP_LEVEL = frozenset({
    "subprocess", "os.system", "socket", "ctypes",
    "multiprocessing", "pty", "signal",
})


class SecurityCheck(GuardianCheck):
    """
    Lightweight security check that scans node params for dangerous patterns.

    This is NOT a full sandbox — it's a first-line defense.
    Full sandboxing (RestrictedPython, seccomp) is handled at the infrastructure
    layer in qnx_infrastructure.security.
    """

    @property
    def name(self) -> str:
        return "security"

    def evaluate(self, node: Any, ctx: Any) -> CheckResult:
        try:
            params = getattr(node, "params", {})
            issues = []

            # Scan string values in params for suspicious module references
            for key, val in params.items():
                if isinstance(val, str):
                    for forbidden in _FORBIDDEN_TOP_LEVEL:
                        if forbidden in val:
                            issues.append(
                                f"param '{key}' contains forbidden reference: '{forbidden}'"
                            )

            if issues:
                return CheckResult(
                    check_name=self.name,
                    passed=False,
                    blocking=True,
                    message=f"Security violations detected: {'; '.join(issues)}",
                )

            return CheckResult(check_name=self.name, passed=True, blocking=True)

        except Exception as exc:
            return CheckResult(
                check_name=self.name,
                passed=False,
                blocking=False,
                message=f"Security check raised: {exc!r}",
            )
