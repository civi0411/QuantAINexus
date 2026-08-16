"""
QuantAINexus — training/callbacks/base.py
Base callback protocol.
"""
from typing import Protocol, Any

class Callback(Protocol):
    """Hook into Trainer lifecycle."""
    def on_train_start(self, trainer: Any, model: Any) -> None:
        ...
        
    def on_train_end(self, trainer: Any, model: Any) -> None:
        ...
        
    def on_epoch_start(self, trainer: Any, model: Any, epoch: int) -> None:
        ...
        
    def on_epoch_end(self, trainer: Any, model: Any, epoch: int, metrics: dict) -> None:
        ...
        
    def on_batch_start(self, trainer: Any, model: Any, batch: Any, batch_idx: int) -> None:
        ...
        
    def on_batch_end(self, trainer: Any, model: Any, batch: Any, batch_idx: int, loss: float) -> None:
        ...
        
    def on_validation_start(self, trainer: Any, model: Any) -> None:
        ...
        
    def on_validation_end(self, trainer: Any, model: Any, metrics: dict) -> None:
        ...
