from typing import Protocol
import polars as pl

class Processor(Protocol):
    """
    Contract for data processing (transformations, scaling, cleaning).
    """
    def fit(self, data: pl.DataFrame) -> "Processor":
        ...
        
    def transform(self, data: pl.DataFrame) -> pl.DataFrame:
        ...
