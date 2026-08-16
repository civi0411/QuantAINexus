"""
QuantAINexus — evaluate/backtest/event_driven.py
Event-driven backtest engine.
"""
from typing import Any
import polars as pl
from . import BACKTEST
from .engine import BaseBacktestEngine

@BACKTEST.register_module(force=True)
class EventDrivenBacktester(BaseBacktestEngine):
    """
    Tick-by-tick or bar-by-bar event-driven engine.
    """
    def __init__(self, initial_capital: float = 100000.0):
        self.initial_capital = initial_capital

    def run(self, strategy: Any, events_stream: Any) -> Any:
        try:
            from quantainexus._native import run_backtest_rs
            # Fall down to Rust backtest core
            return run_backtest_rs(strategy, events_stream, self.initial_capital)
        except ImportError:
            # Python event loop fallback
            return None
