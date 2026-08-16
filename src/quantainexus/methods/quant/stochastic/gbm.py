"""
QuantAINexus — methods/quant/stochastic/gbm.py
Geometric Brownian Motion.
"""
import numpy as np
import polars as pl
from . import QUANT
from .._base import QuantModel

@QUANT.register_module(force=True)
class GBM(QuantModel):
    """Geometric Brownian Motion."""
    def __init__(self, mu: float = 0.0, sigma: float = 0.2, s0: float = 100.0):
        super().__init__(name="gbm")
        self.mu = mu
        self.sigma = sigma
        self.s0 = s0

    def calibrate(self, market_data: pl.DataFrame) -> "GBM":
        # Calibrate mu and sigma from historical close prices
        returns = (market_data["close"] / market_data["close"].shift(1)) - 1
        returns = returns.drop_nulls()
        dt = 1.0 / 252.0
        self.mu = returns.mean() / dt
        self.sigma = returns.std() / np.sqrt(dt)
        self.s0 = market_data["close"].tail(1).item()
        return self

    def simulate(self, n_paths: int, n_steps: int, dt: float) -> np.ndarray:
        try:
            from quantainexus._native import gbm_simulate_rs
            return gbm_simulate_rs(self.mu, self.sigma, self.s0, n_paths, n_steps, dt)
        except ImportError:
            # Pure Python fallback
            np.random.seed(42) # for reproducibility if seed not set externally
            dW = np.random.normal(0, np.sqrt(dt), (n_paths, n_steps))
            paths = np.zeros((n_paths, n_steps + 1))
            paths[:, 0] = self.s0
            for t in range(1, n_steps + 1):
                paths[:, t] = paths[:, t-1] * np.exp((self.mu - 0.5 * self.sigma**2) * dt + self.sigma * dW[:, t-1])
            return paths
