"""
QuantAINexus — _kernel/contracts/transformer.py

Transformer Contract #2 (Article V).
A Transformer is stateless (or stateful-but-serialisable) data processor.

Import policy: typing ONLY. No heavy dependencies.
"""
from __future__ import annotations

from typing import Any, Protocol, runtime_checkable

from ..domain.context import ResearchContext


@runtime_checkable
class Transformer(Protocol):
    """
    Contract for any data transformation step in the pipeline.

    transform() must be pure relative to ctx — same ctx + same input → same output.
    It must respect ctx.pit_as_of (no future data leakage).
    """

    def transform(self, dataset: Any, ctx: ResearchContext) -> Any:
        """
        Apply transformation and return the transformed dataset.

        Args:
            dataset: Input dataset (typically a Polars DataFrame).
            ctx:     ResearchContext carrying PIT boundary and trace_id.

        Returns:
            Transformed dataset (same type as input, or compatible).
        """
        ...
