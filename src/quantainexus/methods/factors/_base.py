"""
QuantAINexus — methods/factors/_base.py
Base factor class.
"""
from typing import Any
import polars as pl
from quantainexus._kernel.contracts.factor import Factor
from quantainexus._kernel.contracts.method import Method

class BaseFactor(Factor, Method):
    """
    Base class for all factors.
    Implements Method contract (fit is a no-op, predict wraps compute).
    """
    def __init__(self, name: str):
        self.name = name

    def compute(self, data: pl.DataFrame) -> pl.DataFrame:
        raise NotImplementedError

    def fit(self, data: Any, **kwargs) -> "BaseFactor":
        # Deterministic factors don't need training
        return self

    def predict(self, data: Any, **kwargs) -> Any:
        # Wrap compute for Method contract compatibility
        if not isinstance(data, pl.DataFrame):
            raise TypeError("BaseFactor expects Polars DataFrame")
        return self.compute(data)
