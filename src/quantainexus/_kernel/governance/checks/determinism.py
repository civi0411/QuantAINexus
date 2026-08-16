"""
QuantAINexus — _kernel/governance/checks/determinism.py

DeterminismCheck — verifies seed is set for stochastic nodes.
Blocking: False (warning only — research sometimes needs stochastic exploration).
"""
from __future__ import annotations

from typing import Any

from ..check import CheckResult, GuardianCheck

_STOCHASTIC_KINDS = {"method"}  # these typically require a seed


class DeterminismCheck(GuardianCheck):
    """
    Warns when a stochastic node is executed without a random seed in ctx.

    Non-blocking (warning) so researchers aren't hard-blocked during exploration.
    Becomes blocking in the "production" profile via a subclass.
    """

    @property
    def name(self) -> str:
        return "determinism"

    def _is_blocking(self) -> bool:
        return False  # Override to True in ProductionDeterminismCheck

    def evaluate(self, node: Any, ctx: Any) -> CheckResult:
        try:
            kind = getattr(node, "kind", "")
            if kind not in _STOCHASTIC_KINDS:
                return CheckResult(check_name=self.name, passed=True, blocking=self._is_blocking())

            seed = getattr(ctx, "seed", None)
            if seed is None:
                return CheckResult(
                    check_name=self.name,
                    passed=False,
                    blocking=self._is_blocking(),
                    message=(
                        f"Node '{getattr(node, 'id', '?')}' (kind={kind!r}) "
                        "is stochastic but ResearchContext.seed is None. "
                        "Results may not be reproducible."
                    ),
                )

            return CheckResult(check_name=self.name, passed=True, blocking=self._is_blocking())

        except Exception as exc:
            return CheckResult(
                check_name=self.name,
                passed=False,
                blocking=False,
                message=f"Determinism check raised: {exc!r}",
            )
