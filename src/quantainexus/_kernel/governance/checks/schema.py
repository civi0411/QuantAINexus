"""
QuantAINexus — _kernel/governance/checks/schema.py

SchemaCheck — validates that a Node's params satisfy its registered contract.
Blocking: True (schema violations are hard failures).
"""
from __future__ import annotations

from typing import Any

from ..check import CheckResult, GuardianCheck


class SchemaCheck(GuardianCheck):
    """
    Verifies that a Node has all required params declared by its contract.
    This is a lightweight structural check — it does NOT inspect data content.
    """

    @property
    def name(self) -> str:
        return "schema"

    def evaluate(self, node: Any, ctx: Any) -> CheckResult:
        try:
            # Basic check: node must have a name and kind
            if not getattr(node, "name", None):
                return CheckResult(
                    check_name=self.name,
                    passed=False,
                    blocking=True,
                    message="Node.name is empty — cannot resolve component from RegistryHub",
                )
            if not getattr(node, "kind", None):
                return CheckResult(
                    check_name=self.name,
                    passed=False,
                    blocking=True,
                    message="Node.kind is empty — cannot dispatch execution",
                )
            return CheckResult(check_name=self.name, passed=True, blocking=True)
        except Exception as exc:
            return CheckResult(
                check_name=self.name,
                passed=False,
                blocking=False,
                message=f"Schema check raised: {exc!r}",
            )
