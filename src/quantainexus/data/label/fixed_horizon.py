"""
QuantAINexus — data/label/fixed_horizon.py
Fixed horizon labeling.
"""
import polars as pl
from . import LABELER
from quantainexus._kernel.contracts.labeler import Labeler

@LABELER.register_module(force=True)
class FixedHorizonLabeler(Labeler):
    def __init__(self, horizon: int = 1):
        self.horizon = horizon
        
    def label(self, data: pl.DataFrame, **kwargs) -> pl.DataFrame:
        target = (data["close"].shift(-self.horizon) / data["close"]) - 1
        return data.with_columns(target.alias(f"label_{self.horizon}"))
