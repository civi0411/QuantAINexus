"""
QuantAINexus — methods/factors/technical/momentum.py
Momentum indicators.
"""
import polars as pl
from . import FACTOR
from .._base import BaseFactor

@FACTOR.register_module(force=True)
class RSI(BaseFactor):
    """Relative Strength Index."""
    def __init__(self, period: int = 14):
        super().__init__(name="rsi")
        self.period = period
        
    def compute(self, data: pl.DataFrame) -> pl.DataFrame:
        try:
            from quantainexus._native import rsi_rs
            arr = rsi_rs(data["close"].to_arrow(), self.period)
            return data.with_columns(pl.from_arrow(arr).alias(f"rsi_{self.period}"))
        except ImportError:
            delta = data["close"].diff()
            gain = delta.clip(lower_bound=0).rolling_mean(self.period)
            loss = (-delta.clip(upper_bound=0)).rolling_mean(self.period)
            
            # Avoid division by zero
            loss_safe = pl.when(loss == 0).then(1e-9).otherwise(loss)
            rs = gain / loss_safe
            
            rsi = 100 - (100 / (1 + rs))
            return data.with_columns(rsi.alias(f"rsi_{self.period}"))

@FACTOR.register_module(force=True)
class MACD(BaseFactor):
    """Moving Average Convergence Divergence."""
    def __init__(self, fast: int = 12, slow: int = 26, signal: int = 9):
        super().__init__(name="macd")
        self.fast = fast
        self.slow = slow
        self.signal = signal

    def compute(self, data: pl.DataFrame) -> pl.DataFrame:
        fast_ema = data["close"].ewm_mean(span=self.fast)
        slow_ema = data["close"].ewm_mean(span=self.slow)
        macd_line = fast_ema - slow_ema
        signal_line = macd_line.ewm_mean(span=self.signal)
        histogram = macd_line - signal_line
        
        return data.with_columns([
            macd_line.alias(f"macd_line_{self.fast}_{self.slow}"),
            signal_line.alias(f"macd_signal_{self.signal}"),
            histogram.alias(f"macd_hist")
        ])
