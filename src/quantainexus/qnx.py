"""
QuantAINexus — qnx.py

Public entry point. Import from here for the stable public API.

Usage:
    from quantainexus.qnx import (
        RegistryHub, Category, register,
        GraphBuilder, ResearchContext, KnowledgeTime,
        LocalRunner, QuantAINexusConfig, load_config,
    )
"""
# Registry
from ._kernel.registry import RegistryHub, Category, register, registry

# Domain
from ._kernel.domain import (
    AssetID, OrderID,
    KnowledgeTime,
    Asset, AssetStage,
    Order, OrderSide,
    ResearchContext,
    Portfolio, Position,
    Signal,
)

# Graph
from ._kernel.graph import Node, Graph, GraphBuilder

# Governance
from ._kernel.governance import (
    Guardian, AgentBreaker,
    CheckResult, HookResult,
    LifecycleState, state_from_stage,
)

# Runtime
from ._kernel.runtime import LocalRunner, Runner

# Config
from ._kernel.config import QuantAINexusConfig, load_config

# Errors
from ._kernel.errors import (
    QuantAINexusError,
    GuardianBlockedError,
    AgentBreakerTripped,
    CyclicGraphError,
)

# Legacy compat
from ._kernel.task import Task, TaskType

__all__ = [
    # Registry
    "RegistryHub", "Category", "register", "registry",
    # Domain
    "AssetID", "OrderID", "KnowledgeTime",
    "Asset", "AssetStage", "Order", "OrderSide",
    "ResearchContext", "Portfolio", "Position", "Signal",
    # Graph
    "Node", "Graph", "GraphBuilder",
    # Governance
    "Guardian", "AgentBreaker",
    "CheckResult", "HookResult",
    "LifecycleState", "state_from_stage",
    # Runtime
    "Runner", "LocalRunner",
    # Config
    "QuantAINexusConfig", "load_config",
    # Errors
    "QuantAINexusError", "GuardianBlockedError",
    "AgentBreakerTripped", "CyclicGraphError",
    # Legacy
    "Task", "TaskType",
]
