"""
QuantAINexus — _kernel/governance/agent_breaker.py

AgentBreaker — Circuit Breaker for AI Agent loops (Article X §10.2).

MANDATORY: Every agent feedback loop MUST be wrapped by AgentBreaker.
This prevents runaway LLM calls, infinite loops, and budget overruns.

Import policy: dataclasses, typing ONLY. No heavy dependencies.
"""
from __future__ import annotations

import threading
from dataclasses import dataclass, field

from ..errors import AgentBreakerTripped


@dataclass
class AgentBreaker:
    """
    Circuit breaker that trips when iteration or cost limits are exceeded.

    Usage:
        breaker = AgentBreaker(max_iterations=50, max_cost_usd=5.0)
        for _ in range(MAX):
            breaker.tick(cost_usd=0.02)  # raises AgentBreakerTripped if over limit
            result = agent.act(obs)
            ...

    Thread-safe: uses a lock so breaker can be shared across parallel agents.
    """
    max_iterations: int
    max_cost_usd:   float

    _iterations: int   = field(default=0, init=False, repr=False)
    _cost_usd:   float = field(default=0.0, init=False, repr=False)
    _lock: threading.Lock = field(
        default_factory=threading.Lock, init=False, repr=False
    )

    def __post_init__(self) -> None:
        if self.max_iterations <= 0:
            raise ValueError("max_iterations must be positive")
        if self.max_cost_usd <= 0:
            raise ValueError("max_cost_usd must be positive")

    # ── Main check ───────────────────────────────────────────────────────

    def tick(self, cost_usd: float = 0.0) -> None:
        """
        Increment counters and raise AgentBreakerTripped if any limit exceeded.

        Call at the START of each agent loop iteration, BEFORE calling the LLM.

        Args:
            cost_usd: Estimated cost of the upcoming LLM call in USD.

        Raises:
            AgentBreakerTripped: when iteration or cost limit is exceeded.
        """
        with self._lock:
            self._iterations += 1
            self._cost_usd += cost_usd

            if self._iterations > self.max_iterations:
                raise AgentBreakerTripped(
                    f"max_iterations={self.max_iterations} exceeded "
                    f"(current={self._iterations})"
                )

            if self._cost_usd > self.max_cost_usd:
                raise AgentBreakerTripped(
                    f"max_cost_usd=${self.max_cost_usd:.4f} exceeded "
                    f"(current=${self._cost_usd:.4f})"
                )

    # ── Status ───────────────────────────────────────────────────────────

    @property
    def iterations(self) -> int:
        return self._iterations

    @property
    def cost_usd(self) -> float:
        return self._cost_usd

    def is_safe(self) -> bool:
        """Return True if both limits are still within bounds."""
        return (
            self._iterations <= self.max_iterations
            and self._cost_usd <= self.max_cost_usd
        )

    def reset(self) -> None:
        """Reset counters. Use between distinct agent tasks, not mid-loop."""
        with self._lock:
            self._iterations = 0
            self._cost_usd = 0.0
