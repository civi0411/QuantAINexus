"""
QuantAINexus — _kernel/graph/builder.py

GraphBuilder — fluent API for constructing Graphs (Article VIII §8.2).

Usage:
    graph = (
        GraphBuilder()
        .add_data("prices", source="yahoo", symbol="VN30")
        .add_transform("cleaned", transformer="zscore_normalizer", depends_on=["prices"])
        .add_method("signal", name="lightgbm", depends_on=["cleaned"])
        .add_evaluate("metrics", name="sharpe_evaluator", depends_on=["signal"])
        .build()
    )

Import policy: typing ONLY (plus internal graph modules). No heavy dependencies.
"""
from __future__ import annotations

from typing import Any

from .node import Node
from .graph import Graph


class GraphBuilder:
    """
    Fluent builder that accumulates Nodes and produces an immutable Graph.

    Each add_*() call returns self to enable method chaining.
    build() validates the DAG (topological sort) and returns the frozen Graph.
    """

    def __init__(self) -> None:
        self._nodes: list[Node] = []

    # ── Node factories ───────────────────────────────────────────────────

    def add_data(
        self,
        id: str,
        source: str,
        **params: Any,
    ) -> "GraphBuilder":
        """Add a data-loading node (kind='data')."""
        self._nodes.append(
            Node(id=id, kind="data", name=source, params=dict(params))
        )
        return self

    def add_transform(
        self,
        id: str,
        transformer: str,
        depends_on: list[str],
        **params: Any,
    ) -> "GraphBuilder":
        """Add a transformation node (kind='transform')."""
        self._nodes.append(
            Node(
                id=id,
                kind="transform",
                name=transformer,
                params=dict(params),
                depends_on=tuple(depends_on),
            )
        )
        return self

    def add_method(
        self,
        id: str,
        name: str,
        depends_on: list[str],
        **params: Any,
    ) -> "GraphBuilder":
        """Add a model/method node (kind='method')."""
        self._nodes.append(
            Node(
                id=id,
                kind="method",
                name=name,
                params=dict(params),
                depends_on=tuple(depends_on),
            )
        )
        return self

    def add_evaluate(
        self,
        id: str,
        name: str,
        depends_on: list[str],
        **params: Any,
    ) -> "GraphBuilder":
        """Add an evaluation node (kind='evaluate')."""
        self._nodes.append(
            Node(
                id=id,
                kind="evaluate",
                name=name,
                params=dict(params),
                depends_on=tuple(depends_on),
            )
        )
        return self

    def add_execution(
        self,
        id: str,
        venue: str,
        depends_on: list[str],
        **params: Any,
    ) -> "GraphBuilder":
        """Add an order-execution node (kind='execution')."""
        self._nodes.append(
            Node(
                id=id,
                kind="execution",
                name=venue,
                params=dict(params),
                depends_on=tuple(depends_on),
            )
        )
        return self

    def add_node(self, node: Node) -> "GraphBuilder":
        """Add a pre-constructed Node directly."""
        self._nodes.append(node)
        return self

    # ── Build ────────────────────────────────────────────────────────────

    def build(self) -> Graph:
        """
        Validate and return the immutable Graph.
        Raises ValueError if nodes are missing or CyclicGraphError if a cycle exists.
        """
        if not self._nodes:
            raise ValueError("Cannot build an empty Graph — add at least one node.")

        entry_points = self._infer_entry_points()
        graph = Graph(
            nodes=tuple(self._nodes),
            entry_points=tuple(entry_points),
        )
        # Fail-fast: validate topological order at build time
        graph.topological_order()
        return graph

    # ── Internal helpers ─────────────────────────────────────────────────

    def _infer_entry_points(self) -> list[str]:
        """Nodes that are not depended upon by anyone → they are roots."""
        all_deps: set[str] = set()
        for node in self._nodes:
            all_deps.update(node.depends_on)

        # Entry points = nodes WITH no depends_on (they have no predecessors)
        return [n.id for n in self._nodes if not n.depends_on]
