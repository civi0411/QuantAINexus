"""
QuantAINexus — _kernel/domain/asset.py

Asset Aggregate Root (Article IV §4.2).
Represents any artifact that travels through the Research → Live lifecycle.

Rules enforced here:
  - content_hash MUST be non-empty (SHA-256 of payload).
  - stage transitions are controlled by _ALLOWED_TRANSITIONS.
  - promote() is the ONLY way to change stage — always returns a NEW Asset.

Import policy: ONLY dataclasses, enum, typing. No heavy dependencies.
"""
from dataclasses import dataclass, field, replace
from enum import Enum, auto
from typing import Any

from .identity import AssetID
from ..errors import InvalidTransitionError


class AssetStage(Enum):
    """Five-stage lifecycle. Transitions are strictly ordered."""
    RESEARCH   = auto()
    VALIDATION = auto()
    PAPER      = auto()
    SHADOW     = auto()
    LIVE       = auto()


# Allowed one-step promotions.  Demotions are NEVER allowed.
_ALLOWED_TRANSITIONS: dict[AssetStage, set[AssetStage]] = {
    AssetStage.RESEARCH:   {AssetStage.VALIDATION},
    AssetStage.VALIDATION: {AssetStage.PAPER},
    AssetStage.PAPER:      {AssetStage.SHADOW},
    AssetStage.SHADOW:     {AssetStage.LIVE},
    # LIVE has no outgoing transitions.
}


@dataclass
class Asset:
    """
    Aggregate Root — single entry point for all lifecycle state changes.

    Attributes:
        id:           Strongly-typed identity (AssetID).
        kind:         One of "dataset" | "model" | "strategy" | "backtest_result".
        version:      Semantic-ish version string, e.g. "1.2.0".
        stage:        Current lifecycle stage.
        content_hash: SHA-256 hex digest of the payload (MANDATORY).
        lineage:      Tuple of parent AssetIDs (immutable DAG lineage).
        metadata:     Free-form dict for tags, author, description, etc.
    """
    id:           AssetID
    kind:         str
    version:      str
    stage:        AssetStage
    content_hash: str
    lineage:      tuple[AssetID, ...] = field(default_factory=tuple)
    metadata:     dict[str, Any]     = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.content_hash or not self.content_hash.strip():
            raise ValueError(
                f"Asset '{self.id}' must have a non-empty content_hash (SHA-256). "
                "Compute it from the serialised payload before creating the Asset."
            )
        allowed_kinds = {"dataset", "model", "strategy", "backtest_result"}
        if self.kind not in allowed_kinds:
            raise ValueError(
                f"Asset.kind must be one of {allowed_kinds!r}, got {self.kind!r}"
            )

    def promote(self, target: AssetStage) -> "Asset":
        """
        Return a NEW Asset at the target stage.
        Raises InvalidTransitionError if the transition is not allowed.
        """
        if target not in _ALLOWED_TRANSITIONS.get(self.stage, set()):
            raise InvalidTransitionError(self.stage, target)
        return replace(self, stage=target)

    @property
    def is_live(self) -> bool:
        return self.stage is AssetStage.LIVE
