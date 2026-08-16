"""
QuantAINexus — evaluate/backtest/__init__.py
Backtest engines.
"""
from quantainexus._kernel.registry import Registry

BACKTEST = Registry.namespace("backtest")
