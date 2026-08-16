"""
QuantAINexus — _kernel/domain/__init__.py

Public re-exports for the domain layer.
Import from this package, not from individual modules, to maintain stability.
"""
from .identity import AssetID, OrderID
from .time import KnowledgeTime
from .value_objects import Money, Price, KnowledgeTime  # KnowledgeTime re-exported twice is OK
from .asset import Asset, AssetStage
from .order import Order, OrderSide
from .context import ResearchContext
from .portfolio import Portfolio, Position
from .signal import Signal

__all__ = [
    # Identity
    "AssetID",
    "OrderID",
    # Time
    "KnowledgeTime",
    # Value objects
    "Money",
    "Price",
    # Aggregate Roots
    "Asset",
    "AssetStage",
    "Order",
    "OrderSide",
    "ResearchContext",
    "Portfolio",
    "Position",
    # Value Objects (trading)
    "Signal",
]
