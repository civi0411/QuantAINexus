from typing import Protocol
import polars as pl

class Factor(Protocol):
    """
    Contract for computing features/factors.
    """
    name: str
    
    def compute(self, data: pl.DataFrame) -> pl.DataFrame:
        ...
