"""
QuantAINexus — evaluate/metrics/risk.py
Risk measures.
"""
import polars as pl
from .registry import METRIC

@METRIC.register_module(force=True)
def value_at_risk(returns: pl.Series, alpha: float = 0.05) -> float:
    """Historical Value at Risk."""
    returns = returns.drop_nulls()
    if len(returns) == 0: return 0.0
    return float(returns.quantile(alpha))

@METRIC.register_module(force=True)
def conditional_value_at_risk(returns: pl.Series, alpha: float = 0.05) -> float:
    """Historical Conditional Value at Risk (Expected Shortfall)."""
    returns = returns.drop_nulls()
    if len(returns) == 0: return 0.0
    var = value_at_risk(returns, alpha)
    tail = returns.filter(returns <= var)
    if len(tail) == 0: return var
    return float(tail.mean())
