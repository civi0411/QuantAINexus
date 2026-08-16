"""
QuantAINexus — evaluate/metrics/trading.py
Trading metrics.
"""
import polars as pl
from .registry import METRIC

@METRIC.register_module(force=True)
def sharpe_ratio(returns: pl.Series, risk_free: float = 0.0, periods_per_year: int = 252) -> float:
    """Sharpe ratio. Auto Rust if available."""
    try:
        from quantainexus._native import sharpe_rs
        return sharpe_rs(returns.to_arrow(), risk_free, periods_per_year)
    except ImportError:
        returns = returns.drop_nulls()
        if len(returns) < 2: return 0.0
        excess = returns - risk_free / periods_per_year
        std = excess.std()
        if std == 0.0: return 0.0
        return float(excess.mean() / std * (periods_per_year ** 0.5))

@METRIC.register_module(force=True)
def sortino_ratio(returns: pl.Series, risk_free: float = 0.0, periods_per_year: int = 252) -> float:
    """Sortino ratio."""
    returns = returns.drop_nulls()
    if len(returns) < 2: return 0.0
    excess = returns - risk_free / periods_per_year
    downside = excess.filter(excess < 0)
    downside_std = downside.std() if len(downside) > 1 else 1e-9
    if downside_std == 0.0: return 0.0
    return float(excess.mean() / downside_std * (periods_per_year ** 0.5))

@METRIC.register_module(force=True)
def max_drawdown(returns: pl.Series) -> float:
    """Maximum Drawdown."""
    try:
        from quantainexus._native import mdd_rs
        return mdd_rs(returns.to_arrow())
    except ImportError:
        returns = returns.drop_nulls()
        if len(returns) == 0: return 0.0
        cum_ret = (1 + returns).cum_prod()
        running_max = cum_ret.cum_max()
        drawdown = (cum_ret - running_max) / running_max
        return float(drawdown.min())

@METRIC.register_module(force=True)
def win_rate(returns: pl.Series) -> float:
    """Win rate."""
    returns = returns.drop_nulls()
    if len(returns) == 0: return 0.0
    return float((returns > 0).sum() / len(returns))
