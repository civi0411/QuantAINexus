"""
QuantAINexus — training/loss/__init__.py
Loss functions.
"""
from quantainexus._kernel.registry import Registry

LOSS = Registry.namespace("loss")

__all__ = ["LOSS"]
