"""
QuantAINexus — _kernel/graph/graph.py

Graph — immutable DAG that defines a complete pipeline (Article VIII §8.1).

topological_order(): Kahn's BFS algorithm — raises CyclicGraphError on cycles.
content_hash():      SHA-256 of canonical graph representation — used for
                     result caching and reproducibility verification.

Import policy: dataclasses, hashlib, json, collections, typing ONLY.
No heavy dependencies.
"""
from __future__ import annotations

import hashlib
import json
from collections import deque
from dataclasses import dataclass, field
from typing import Any

from .node import Node
from ..errors import CyclicGraphError


@dataclass(frozen=True)
class Graph:
    """
    Immutable Directed Acyclic Graph.

    Attributes:
        nodes:        All nodes in the pipeline, keyed accessible by id.
        entry_points: Node IDs with no incoming edges (roots of the DAG).
    """
    nodes:        tuple[Node, ...]
    entry_points: tuple[str, ...]

    def __post_init__(self) -> None:
        # Validate all depends_on references point to real node IDs
        node_ids = {n.id for n in self.nodes}
        for node in self.nodes:
            for dep in node.depends_on:
                if dep not in node_ids:
                    raise ValueError(
                        f"Node '{node.id}' depends on '{dep}', "
                        f"which is not in the graph."
                    )

    # ── Kahn's topological sort ──────────────────────────────────────────

    def topological_order(self) -> list[Node]:
        """
        Return nodes in topological order using Kahn's BFS algorithm.
        Raises CyclicGraphError if the graph contains a cycle.
        """
        node_map: dict[str, Node] = {n.id: n for n in self.nodes}

        # in_degree[id] = number of predecessors
        in_degree: dict[str, int] = {n.id: 0 for n in self.nodes}
        # adjacency: successor_id → set of node_ids that depend on it
        successors: dict[str, list[str]] = {n.id: [] for n in self.nodes}

        for node in self.nodes:
            for dep in node.depends_on:
                in_degree[node.id] += 1
                successors[dep].append(node.id)

        # Start with all nodes that have no predecessors
        queue: deque[str] = deque(
            nid for nid, deg in in_degree.items() if deg == 0
        )
        result: list[Node] = []

        while queue:
            nid = queue.popleft()
            result.append(node_map[nid])
            for successor_id in successors[nid]:
                in_degree[successor_id] -= 1
                if in_degree[successor_id] == 0:
                    queue.append(successor_id)

        if len(result) != len(self.nodes):
            remaining = {
                nid for nid, deg in in_degree.items() if deg > 0
            }
            raise CyclicGraphError(
                f"Cycle detected involving nodes: {sorted(remaining)}"
            )

        return result

    # ── Content hash ────────────────────────────────────────────────────

    def content_hash(self) -> str:
        """
        SHA-256 of the canonical serialised representation of this graph.
        Two graphs with identical structure and params produce the same hash.
        """
        canonical = [
            {
                "id":         n.id,
                "kind":       n.kind,
                "name":       n.name,
                "params":     n.params,
                "depends_on": list(n.depends_on),
            }
            for n in sorted(self.nodes, key=lambda n: n.id)
        ]
        blob = json.dumps(canonical, sort_keys=True, ensure_ascii=True).encode()
        return hashlib.sha256(blob).hexdigest()

    # ── Helpers ─────────────────────────────────────────────────────────

    def get_node(self, node_id: str) -> Node:
        for n in self.nodes:
            if n.id == node_id:
                return n
        raise KeyError(f"Node '{node_id}' not found in graph")

    @property
    def node_ids(self) -> frozenset[str]:
        return frozenset(n.id for n in self.nodes)
