"""
QuantAINexus — evaluate/metrics/forecasting.py
Forecasting metrics.
"""
import polars as pl
import numpy as np
from .registry import METRIC

@METRIC.register_module(force=True)
def ic(predictions: pl.Series, actuals: pl.Series) -> float:
    """Information Coefficient (Pearson correlation)."""
    df = pl.DataFrame({"p": predictions, "a": actuals}).drop_nulls()
    if len(df) < 2: return 0.0
    return df.select(pl.corr("p", "a")).item()

@METRIC.register_module(force=True)
def rank_ic(predictions: pl.Series, actuals: pl.Series) -> float:
    """Rank Information Coefficient (Spearman correlation)."""
    df = pl.DataFrame({"p": predictions, "a": actuals}).drop_nulls()
    if len(df) < 2: return 0.0
    return df.select(pl.corr("p", "a", method="spearman")).item()

@METRIC.register_module(force=True)
def mse(predictions: pl.Series, actuals: pl.Series) -> float:
    """Mean Squared Error."""
    df = pl.DataFrame({"p": predictions, "a": actuals}).drop_nulls()
    return float(((df["p"] - df["a"]) ** 2).mean())

@METRIC.register_module(force=True)
def rmse(predictions: pl.Series, actuals: pl.Series) -> float:
    """Root Mean Squared Error."""
    return mse(predictions, actuals) ** 0.5

@METRIC.register_module(force=True)
def mae(predictions: pl.Series, actuals: pl.Series) -> float:
    """Mean Absolute Error."""
    df = pl.DataFrame({"p": predictions, "a": actuals}).drop_nulls()
    return float((df["p"] - df["a"]).abs().mean())
