"""
QuantAINexus — _kernel/__init__.py

The immutable kernel. All imports from this package are stable public API.
"""
from .errors import (
    QuantAINexusError,
    DomainError,
    InvalidTransitionError,
    InvariantViolationError,
    LeverageExceededError,
    RegistryError,
    UnknownComponentError,
    DuplicateRegistrationError,
    GuardianBlockedError,
    PromotionBlockedError,
    AgentBreakerTripped,
    CyclicGraphError,
)
from .domain import (
    AssetID, OrderID,
    KnowledgeTime,
    Asset, AssetStage,
    Order, OrderSide,
    ResearchContext,
    Portfolio, Position,
    Signal,
    Money, Price,
)
from .graph import Node, Graph, GraphBuilder
from .registry import RegistryHub, Category, register
from .governance import (
    CheckResult, HookResult, GuardianCheck,
    Guardian, AgentBreaker,
    LifecycleState, state_from_stage,
)
from .runtime import Runner, LocalRunner
from .config import QuantAINexusConfig, load_config

__all__ = [
    # Errors
    "QuantAINexusError",
    "DomainError", "InvalidTransitionError", "InvariantViolationError",
    "LeverageExceededError",
    "RegistryError", "UnknownComponentError", "DuplicateRegistrationError",
    "GuardianBlockedError", "PromotionBlockedError",
    "AgentBreakerTripped", "CyclicGraphError",
    # Domain
    "AssetID", "OrderID",
    "KnowledgeTime",
    "Asset", "AssetStage",
    "Order", "OrderSide",
    "ResearchContext",
    "Portfolio", "Position",
    "Signal", "Money", "Price",
    # Graph
    "Node", "Graph", "GraphBuilder",
    # Registry
    "RegistryHub", "Category", "register",
    # Governance
    "CheckResult", "HookResult", "GuardianCheck",
    "Guardian", "AgentBreaker",
    "LifecycleState", "state_from_stage",
    # Runtime
    "Runner", "LocalRunner",
    # Config
    "QuantAINexusConfig", "load_config",
]
