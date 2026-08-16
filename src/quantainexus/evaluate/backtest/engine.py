"""
QuantAINexus — evaluate/backtest/engine.py
Base backtest engine interface implementation.
"""
from typing import Any
import polars as pl
from quantainexus._kernel.contracts.backtest_engine import BacktestEngine
from . import BACKTEST

class BaseBacktestEngine(BacktestEngine):
    """
    Base backtest engine implementing core lifecycle hooks.
    """
    def run(self, strategy: Any, data: Any) -> Any:
        raise NotImplementedError
