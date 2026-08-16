"""
QuantAINexus — training/callbacks/progress.py
Progress bar callback.
"""
from typing import Any
from .base import Callback

class ProgressBar(Callback):
    def on_epoch_start(self, trainer: Any, model: Any, epoch: int) -> None:
        pass
        
    def on_batch_end(self, trainer: Any, model: Any, batch: Any, batch_idx: int, loss: float) -> None:
        pass
