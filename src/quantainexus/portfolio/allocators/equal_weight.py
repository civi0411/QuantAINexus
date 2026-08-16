"""
QuantAINexus — portfolio/allocators/equal_weight.py
Equal weight allocator.
"""
from typing import Dict
from . import ALLOCATOR

@ALLOCATOR.register_module(force=True)
class EqualWeightAllocator:
    def allocate(self, assets: list[str]) -> Dict[str, float]:
        if not assets: return {}
        w = 1.0 / len(assets)
        return {asset: w for asset in assets}
