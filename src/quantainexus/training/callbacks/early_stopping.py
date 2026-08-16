"""
QuantAINexus — training/callbacks/early_stopping.py
Early stopping callback.
"""
from typing import Any
from .base import Callback

class EarlyStopping(Callback):
    def __init__(self, monitor: str = "val_loss", patience: int = 3, min_delta: float = 0.0):
        self.monitor = monitor
        self.patience = patience
        self.min_delta = min_delta
        self.best_score = None
        self.wait_count = 0
        
    def on_epoch_end(self, trainer: Any, model: Any, epoch: int, metrics: dict) -> None:
        score = metrics.get(self.monitor)
        if score is None:
            return
            
        if self.best_score is None:
            self.best_score = score
        elif score < self.best_score - self.min_delta: # Assuming lower is better for now
            self.best_score = score
            self.wait_count = 0
        else:
            self.wait_count += 1
            if self.wait_count >= self.patience:
                # Need a way to signal trainer to stop, e.g., trainer.should_stop = True
                if hasattr(trainer, 'should_stop'):
                    trainer.should_stop = True
