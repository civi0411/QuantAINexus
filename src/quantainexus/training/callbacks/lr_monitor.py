"""
QuantAINexus — training/callbacks/lr_monitor.py
Learning rate monitor callback.
"""
from typing import Any
from .base import Callback

class LearningRateMonitor(Callback):
    def on_epoch_end(self, trainer: Any, model: Any, epoch: int, metrics: dict) -> None:
        pass
