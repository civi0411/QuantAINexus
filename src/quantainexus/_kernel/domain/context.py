"""
QuantAINexus — _kernel/domain/context.py

ResearchContext — immutable execution context (Article IV §4.1).

Frozen so it can be safely passed across DAG nodes, threads, and agents
without risk of mutation. trace_id is auto-generated per run so all logs,
spans, and artifacts belonging to the same run can be correlated.

Import policy: ONLY dataclasses, typing, uuid, datetime. No heavy dependencies.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional
from uuid import uuid4

from .time import KnowledgeTime


@dataclass(frozen=True)
class ResearchContext:
    """
    Immutable execution context — guaranteed determinism and traceability.

    Attributes:
        pit_as_of: Point-in-Time boundary. No data after this date may be used.
        seed:      Optional random seed for reproducible stochastic ops.
        trace_id:  Auto-generated UUID to correlate all events in one run.
    """
    pit_as_of: KnowledgeTime
    seed:      Optional[int] = None
    trace_id:  str           = field(default_factory=lambda: str(uuid4()))
