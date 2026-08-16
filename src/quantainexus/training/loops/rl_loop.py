"""
QuantAINexus — training/loops/rl_loop.py
RL training loop.
"""
from typing import Any

class RLLoop:
    """
    env.reset -> step -> reward -> update
    """
    def run_epoch(self, model: Any, dataloader: Any, optimizer: Any) -> dict:
        return {"reward": 0.0}
