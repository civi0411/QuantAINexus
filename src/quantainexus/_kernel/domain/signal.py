from dataclasses import dataclass
from .value_objects import KnowledgeTime

@dataclass(frozen=True)
class Signal:
    """Value Object representing a trading signal."""
    asset_id: str
    strength: float # typically -1.0 to 1.0
    timestamp: KnowledgeTime
