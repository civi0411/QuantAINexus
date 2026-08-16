"""
QuantAINexus — portfolio/rebalancer.py
Portfolio rebalancer.
"""
from typing import Any

class Rebalancer:
    def __init__(self, frequency: str = "daily"):
        self.frequency = frequency
        
    def should_rebalance(self, current_time: Any, last_rebalance_time: Any) -> bool:
        return True
