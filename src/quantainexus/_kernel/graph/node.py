"""
QuantAINexus — _kernel/graph/node.py

Node — the atomic unit of a DAG pipeline (Article VIII §8.1).

Import policy: dataclasses, typing, Literal ONLY. No heavy dependencies.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal


@dataclass(frozen=True)
class Node:
    """
    A single computation step in the pipeline DAG.

    Attributes:
        id:         Unique within a Graph (e.g. "prices", "signal", "metrics").
        kind:       Semantic role — determines how Runner dispatches execution.
        name:       Registered name in RegistryHub (e.g. "yahoo", "lightgbm").
        params:     Constructor kwargs forwarded to the registered component.
        depends_on: Tuple of upstream node IDs this node reads from.
    """
    id:         str
    kind:       Literal["data", "transform", "method", "evaluate", "execution"]
    name:       str
    params:     dict[str, Any]  = field(default_factory=dict)
    depends_on: tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if not self.id or not self.id.strip():
            raise ValueError("Node.id must be a non-empty string")
        if not self.name or not self.name.strip():
            raise ValueError("Node.name must be a non-empty string")
