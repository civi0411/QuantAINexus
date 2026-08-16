"""
QuantAINexus — training/loss/reward.py
Reward functions for Reinforcement Learning.
"""
from typing import Any
from . import LOSS

@LOSS.register_module(force=True)
class SharpeReward:
    """Reward based on Sharpe Ratio."""
    def __call__(self, state: Any, action: Any, next_state: Any) -> float:
        return 0.0

@LOSS.register_module(force=True)
class PnLReward:
    """Reward based on Profit and Loss."""
    def __call__(self, state: Any, action: Any, next_state: Any) -> float:
        return 0.0
