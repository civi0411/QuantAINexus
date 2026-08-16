"""
QuantAINexus — evaluate/metrics/portfolio.py
Portfolio metrics.
"""
import polars as pl
from .registry import METRIC

@METRIC.register_module(force=True)
def annual_return(returns: pl.Series, periods_per_year: int = 252) -> float:
    """Annualized return."""
    returns = returns.drop_nulls()
    if len(returns) == 0: return 0.0
    cum_ret = (1 + returns).prod()
    years = len(returns) / periods_per_year
    if years == 0: return 0.0
    return float(cum_ret ** (1 / years) - 1)

@METRIC.register_module(force=True)
def volatility(returns: pl.Series, periods_per_year: int = 252) -> float:
    """Annualized volatility."""
    returns = returns.drop_nulls()
    if len(returns) < 2: return 0.0
    return float(returns.std() * (periods_per_year ** 0.5))
