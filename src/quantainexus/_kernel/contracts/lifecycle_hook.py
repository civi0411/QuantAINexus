"""
QuantAINexus — _kernel/contracts/lifecycle_hook.py

LifecycleHook Protocol (Contract #10 of 12, Article V).

CRITICAL DESIGN RULE (Article VII):
  - pre_execute() returns HookResult — it NEVER raises.
  - Raising is the EXCLUSIVE responsibility of LocalRunner.
  - This separation ensures Guardian has no side effects and is easily testable.

Import policy: ONLY typing. No heavy dependencies.
"""
from __future__ import annotations

from typing import Any, Optional, Protocol, runtime_checkable

from ..governance.check import HookResult


@runtime_checkable
class LifecycleHook(Protocol):
    """
    Contract for any object that intercepts DAG node execution.

    pre_execute:  Called BEFORE a node runs. Returns HookResult.
                  If HookResult.blocking is True, Runner will raise GuardianBlockedError.
    post_execute: Called AFTER a node runs. Used for audit/telemetry only.
                  Must NOT raise under any circumstances.
    """

    def pre_execute(
        self,
        node: Any,
        ctx: Any,
    ) -> Optional[HookResult]:
        """
        Evaluate whether execution of `node` is permitted.

        Returns:
            HookResult with blocking=True to halt execution,
            HookResult with blocking=False (or None) to allow it.
        """
        ...

    def post_execute(
        self,
        node: Any,
        ctx: Any,
        result: Any,
    ) -> None:
        """
        Audit hook called after node execution.
        MUST NOT raise. Use try/except internally if needed.
        """
        ...
