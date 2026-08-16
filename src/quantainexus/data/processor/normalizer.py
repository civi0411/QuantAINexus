"""
QuantAINexus — data/processor/normalizer.py
Data normalization processors.
"""
import polars as pl
from . import PROCESSOR
from quantainexus._kernel.contracts.processor import Processor

@PROCESSOR.register_module(force=True)
class ZScoreNormalizer(Processor):
    def __init__(self, columns: list[str]):
        self.columns = columns
        self.stats = {}
        
    def fit(self, data: pl.DataFrame) -> "ZScoreNormalizer":
        for col in self.columns:
            mean = data[col].mean()
            std = data[col].std()
            self.stats[col] = {"mean": mean, "std": std}
        return self
        
    def transform(self, data: pl.DataFrame) -> pl.DataFrame:
        exprs = []
        for col in self.columns:
            stat = self.stats.get(col, {"mean": 0.0, "std": 1.0})
            expr = (pl.col(col) - stat["mean"]) / stat["std"]
            exprs.append(expr.alias(col))
        return data.with_columns(exprs)
