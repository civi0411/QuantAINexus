"""
QuantAINexus — data/label/triple_barrier.py
Triple barrier labeling (Marcos Lopez de Prado).
"""
import polars as pl
from . import LABELER
from quantainexus._kernel.contracts.labeler import Labeler

@LABELER.register_module(force=True)
class TripleBarrierLabeler(Labeler):
    def __init__(self, pt_sl: tuple[float, float], t1: int, min_ret: float = 0.001):
        self.pt_sl = pt_sl
        self.t1 = t1
        self.min_ret = min_ret
        
    def label(self, data: pl.DataFrame, **kwargs) -> pl.DataFrame:
        try:
            from quantainexus._native import triple_barrier_rs
            # Assume rust function handles it and returns labels
            return triple_barrier_rs(data.to_arrow(), self.pt_sl, self.t1, self.min_ret)
        except ImportError:
            # Basic pure python fallback (placeholder)
            return data.with_columns(pl.lit(0).alias("label_tb"))
