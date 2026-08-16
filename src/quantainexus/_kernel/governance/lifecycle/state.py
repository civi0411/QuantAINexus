"""
QuantAINexus — _kernel/governance/lifecycle/state.py

Lifecycle State Machine (Article IX).

Each state knows:
  - can_execute_live_orders(): whether live trading is permitted.
  - promote(): next state after passing the Guardian profile check.

Import policy: abc, typing ONLY. No heavy dependencies.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..lifecycle.guardian import Guardian
    from ...domain.asset import Asset, AssetStage

from ...errors import InvalidTransitionError, PromotionBlockedError


class LifecycleState(ABC):
    """Abstract base state in the Asset lifecycle state machine."""

    @abstractmethod
    def promote(self, asset: "Asset", guardian: "Guardian") -> "LifecycleState":
        """
        Attempt promotion to the next state.
        Raises PromotionBlockedError if Guardian rejects it.
        Raises InvalidTransitionError if no valid next state exists.
        """

    @abstractmethod
    def can_execute_live_orders(self) -> bool:
        """True only in LiveState."""

    @property
    @abstractmethod
    def stage_name(self) -> str:
        """Human-readable name matching AssetStage enum value."""


# ── Concrete states ───────────────────────────────────────────────────────────

class ResearchState(LifecycleState):
    """Initial state — free experimentation, no live trading allowed."""

    def promote(self, asset: "Asset", guardian: "Guardian") -> LifecycleState:
        report = guardian.pre_execute(asset, None)
        if report and report.blocking:
            raise PromotionBlockedError(report)
        return ValidationState()

    def can_execute_live_orders(self) -> bool:
        return False

    @property
    def stage_name(self) -> str:
        return "RESEARCH"


class ValidationState(LifecycleState):
    """Out-of-sample validation on held-out data."""

    def promote(self, asset: "Asset", guardian: "Guardian") -> LifecycleState:
        report = guardian.pre_execute(asset, None)
        if report and report.blocking:
            raise PromotionBlockedError(report)
        return PaperState()

    def can_execute_live_orders(self) -> bool:
        return False

    @property
    def stage_name(self) -> str:
        return "VALIDATION"


class PaperState(LifecycleState):
    """Paper trading — simulated fills, no real capital at risk."""

    def promote(self, asset: "Asset", guardian: "Guardian") -> LifecycleState:
        report = guardian.pre_execute(asset, None)
        if report and report.blocking:
            raise PromotionBlockedError(report)
        return ShadowState()

    def can_execute_live_orders(self) -> bool:
        return False

    @property
    def stage_name(self) -> str:
        return "PAPER"


class ShadowState(LifecycleState):
    """
    Shadow mode — real market data, parallel execution alongside production,
    but orders are not sent to the exchange.
    """

    def promote(self, asset: "Asset", guardian: "Guardian") -> LifecycleState:
        report = guardian.pre_execute(asset, None)
        if report and report.blocking:
            raise PromotionBlockedError(report)
        return LiveState()

    def can_execute_live_orders(self) -> bool:
        return False

    @property
    def stage_name(self) -> str:
        return "SHADOW"


class LiveState(LifecycleState):
    """
    Live production — real orders submitted to exchange.
    No further promotion is possible from this state.
    """

    def promote(self, asset: "Asset", guardian: "Guardian") -> LifecycleState:
        raise InvalidTransitionError("LIVE", None)

    def can_execute_live_orders(self) -> bool:
        return True

    @property
    def stage_name(self) -> str:
        return "LIVE"


# ── Factory ───────────────────────────────────────────────────────────────────

def state_from_stage(stage: Any) -> LifecycleState:
    """
    Build the correct LifecycleState from an AssetStage enum value.
    """
    from ...domain.asset import AssetStage  # local import to avoid circular
    _MAP = {
        AssetStage.RESEARCH:   ResearchState,
        AssetStage.VALIDATION: ValidationState,
        AssetStage.PAPER:      PaperState,
        AssetStage.SHADOW:     ShadowState,
        AssetStage.LIVE:       LiveState,
    }
    cls = _MAP.get(stage)
    if cls is None:
        raise ValueError(f"Unknown AssetStage: {stage!r}")
    return cls()
