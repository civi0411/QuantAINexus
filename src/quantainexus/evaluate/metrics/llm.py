"""
QuantAINexus — evaluate/metrics/llm.py
LLM evaluation metrics.
"""
import polars as pl
from .registry import METRIC

@METRIC.register_module(force=True)
def perplexity(predictions: pl.Series) -> float:
    """Placeholder for Perplexity."""
    return 0.0
