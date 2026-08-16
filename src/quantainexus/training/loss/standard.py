"""
QuantAINexus — training/loss/standard.py
Standard ML loss functions.
"""
from typing import Any
from . import LOSS

@LOSS.register_module(force=True)
class MSELoss:
    """Mean Squared Error."""
    def __call__(self, predictions: Any, targets: Any) -> Any:
        return 0.0

@LOSS.register_module(force=True)
class MAELoss:
    """Mean Absolute Error."""
    def __call__(self, predictions: Any, targets: Any) -> Any:
        return 0.0

@LOSS.register_module(force=True)
class HuberLoss:
    """Huber Loss."""
    def __init__(self, delta: float = 1.0):
        self.delta = delta
        
    def __call__(self, predictions: Any, targets: Any) -> Any:
        return 0.0
