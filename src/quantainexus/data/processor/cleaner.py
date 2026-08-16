"""
QuantAINexus — data/processor/cleaner.py
Data cleaning processors.
"""
import polars as pl
from . import PROCESSOR
from quantainexus._kernel.contracts.processor import Processor

@PROCESSOR.register_module(force=True)
class DropNullProcessor(Processor):
    def fit(self, data: pl.DataFrame) -> "DropNullProcessor":
        return self
        
    def transform(self, data: pl.DataFrame) -> pl.DataFrame:
        return data.drop_nulls()

@PROCESSOR.register_module(force=True)
class FillForwardProcessor(Processor):
    def fit(self, data: pl.DataFrame) -> "FillForwardProcessor":
        return self
        
    def transform(self, data: pl.DataFrame) -> pl.DataFrame:
        return data.fill_null(strategy="forward")
