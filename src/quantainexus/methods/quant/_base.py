"""
QuantAINexus — methods/quant/_base.py
Base class for pure quantitative math models.
"""
from typing import Any
import numpy as np
import polars as pl
from quantainexus._kernel.contracts.method import Method

class QuantModel(Method):
    """
    Base class for deterministic quant math models.
    """
    def __init__(self, name: str):
        self.name = name

    def fit(self, data: Any, **kwargs) -> "QuantModel":
        # Fit here means calibration (e.g., calibrating Heston model parameters)
        return self.calibrate(data)

    def predict(self, data: Any, **kwargs) -> Any:
        raise NotImplementedError("Use simulate() or price() for Quant models")
        
    def calibrate(self, market_data: pl.DataFrame) -> "QuantModel":
        """Calibrate model parameters using market data."""
        return self
        
    def simulate(self, n_paths: int, n_steps: int, dt: float) -> np.ndarray:
        """Simulate stochastic paths."""
        raise NotImplementedError
        
    def price(self, instrument: dict) -> float:
        """Price a financial instrument."""
        raise NotImplementedError
