"""
QuantAINexus — _kernel/governance/checks/pit.py

PITCheck — Point-in-Time integrity check.
Ensures that data nodes do not use a KnowledgeTime in the future relative to ctx.pit_as_of.
Blocking: True (look-ahead bias is a hard failure in research/production).
"""
from __future__ import annotations

from typing import Any

from ..check import CheckResult, GuardianCheck


class PITCheck(GuardianCheck):
    """
    Validates that data-loading nodes do not request data beyond ctx.pit_as_of.

    For non-data nodes (method, evaluate, execution), this check always passes
    because they operate on already-fetched data slices.
    """

    @property
    def name(self) -> str:
        return "pit_integrity"

    def evaluate(self, node: Any, ctx: Any) -> CheckResult:
        try:
            # Only applicable to data nodes
            if getattr(node, "kind", None) != "data":
                return CheckResult(check_name=self.name, passed=True, blocking=True)

            # Check if params contain an explicit 'end' date beyond pit_as_of
            params = getattr(node, "params", {})
            end = params.get("end")

            if end is None or ctx is None:
                # No explicit end date — PIT boundary will be enforced by DataSource
                return CheckResult(check_name=self.name, passed=True, blocking=True)

            pit = getattr(ctx, "pit_as_of", None)
            if pit is None:
                return CheckResult(check_name=self.name, passed=True, blocking=True)

            # Compare as strings if both are date/datetime — basic check
            if str(end) > str(pit):
                return CheckResult(
                    check_name=self.name,
                    passed=False,
                    blocking=True,
                    message=(
                        f"Node '{node.id}' requests data until {end!r} "
                        f"which is after pit_as_of={pit!r}. Look-ahead bias detected."
                    ),
                )

            return CheckResult(check_name=self.name, passed=True, blocking=True)

        except Exception as exc:
            return CheckResult(
                check_name=self.name,
                passed=False,
                blocking=False,
                message=f"PIT check raised: {exc!r}",
            )
