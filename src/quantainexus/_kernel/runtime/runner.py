"""
QuantAINexus — _kernel/runtime/runner.py

Runner Protocol — the contract for any execution engine (Article VIII).

Import policy: typing ONLY. No heavy dependencies.
"""
from __future__ import annotations

from typing import Any, Protocol, runtime_checkable

from ..graph.graph import Graph
from ..domain.context import ResearchContext


@runtime_checkable
class Runner(Protocol):
    """
    Contract for a DAG execution engine.

    run() traverses the graph in topological order, calling hooks before/after
    each node, and returns the final materialised result.
    """

    def run(self, graph: Graph, ctx: ResearchContext) -> Any:
        """Execute the graph and return the final result."""
        ...
