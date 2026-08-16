from typing import Protocol
import polars as pl

class Labeler(Protocol):
    """
    Contract for generating labels for machine learning.
    """
    def label(self, data: pl.DataFrame, **kwargs) -> pl.DataFrame:
        ...
