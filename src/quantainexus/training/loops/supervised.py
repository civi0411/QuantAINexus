"""
QuantAINexus — training/loops/supervised.py
Supervised training loop.
"""
from typing import Any

class SupervisedLoop:
    """
    Standard train->val->test loop.
    """
    def run_epoch(self, model: Any, dataloader: Any, optimizer: Any) -> dict:
        return {"loss": 0.0}
