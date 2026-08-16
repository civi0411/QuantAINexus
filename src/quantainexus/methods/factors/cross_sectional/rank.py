"""
QuantAINexus — methods/factors/cross_sectional/rank.py
Cross-sectional ranking.
"""
import polars as pl
from . import FACTOR
from .._base import BaseFactor

@FACTOR.register_module(force=True)
class CrossSectionalRank(BaseFactor):
    """Rank values across assets at a point in time."""
    def __init__(self, target_column: str, group_column: str = "date"):
        super().__init__(name="cross_sectional_rank")
        self.target = target_column
        self.group = group_column

    def compute(self, data: pl.DataFrame) -> pl.DataFrame:
        ranked = data.group_by(self.group).agg(
            pl.col(self.target).rank(method="average").alias(f"{self.target}_rank")
        ).explode(f"{self.target}_rank")
        # Ensure ordering is preserved, assuming stable join or identical row ordering.
        return data.with_columns(ranked[f"{self.target}_rank"])
