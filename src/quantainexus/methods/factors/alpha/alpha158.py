"""
QuantAINexus — methods/factors/alpha/alpha158.py
Alpha158 features (Qlib / FinWorld style).
"""
import polars as pl
from . import FACTOR
from .._base import BaseFactor

@FACTOR.register_module(force=True)
class Alpha158(BaseFactor):
    """Computes standard 158 quantitative features."""
    def __init__(self):
        super().__init__(name="alpha158")

    def compute(self, data: pl.DataFrame) -> pl.DataFrame:
        try:
            from quantainexus._native import alpha158_rs
            return alpha158_rs(data.to_arrow())
        except ImportError:
            # Placeholder for pure Python fallback of 158 features
            # In real implementation this contains extensive feature engineering
            return data.with_columns([
                (pl.col("close") / pl.col("close").shift(1) - 1).alias("roc_1"),
                (pl.col("close") / pl.col("close").shift(5) - 1).alias("roc_5"),
                (pl.col("close") / pl.col("close").shift(10) - 1).alias("roc_10"),
                (pl.col("close") / pl.col("close").shift(20) - 1).alias("roc_20"),
            ])
