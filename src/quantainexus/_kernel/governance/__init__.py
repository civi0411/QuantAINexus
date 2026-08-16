"""
QuantAINexus — _kernel/governance/__init__.py
"""
from .check import CheckResult, HookResult, GuardianCheck
from .agent_breaker import AgentBreaker
from .lifecycle.guardian import Guardian
from .lifecycle.state import (
    LifecycleState,
    ResearchState,
    ValidationState,
    PaperState,
    ShadowState,
    LiveState,
    state_from_stage,
)

__all__ = [
    "CheckResult",
    "HookResult",
    "GuardianCheck",
    "AgentBreaker",
    "Guardian",
    "LifecycleState",
    "ResearchState",
    "ValidationState",
    "PaperState",
    "ShadowState",
    "LiveState",
    "state_from_stage",
]
