"""
QuantAINexus — data/processor/outlier.py
Outlier removal processors.
"""
import polars as pl
from . import PROCESSOR
from quantainexus._kernel.contracts.processor import Processor

@PROCESSOR.register_module(force=True)
class WinsorizeProcessor(Processor):
    def __init__(self, columns: list[str], lower: float = 0.01, upper: float = 0.99):
        self.columns = columns
        self.lower = lower
        self.upper = upper
        self.bounds = {}
        
    def fit(self, data: pl.DataFrame) -> "WinsorizeProcessor":
        for col in self.columns:
            l_val = data[col].quantile(self.lower)
            u_val = data[col].quantile(self.upper)
            self.bounds[col] = {"lower": l_val, "upper": u_val}
        return self
        
    def transform(self, data: pl.DataFrame) -> pl.DataFrame:
        exprs = []
        for col in self.columns:
            bound = self.bounds.get(col)
            if bound:
                expr = pl.col(col).clip(lower_bound=bound["lower"], upper_bound=bound["upper"])
                exprs.append(expr.alias(col))
        if not exprs: return data
        return data.with_columns(exprs)
