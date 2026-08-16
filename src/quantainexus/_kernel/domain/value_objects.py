"""
QuantAINexus — _kernel/domain/value_objects.py

Shared value objects used across multiple domain models.

Note: KnowledgeTime has been moved to domain/time.py.
      This module re-exports it for backward compatibility.

Import policy: ONLY dataclasses, typing. No heavy dependencies.
"""
from __future__ import annotations

from dataclasses import dataclass

# Re-export for backward compat — canonical definition is in time.py
from .time import KnowledgeTime  # noqa: F401


@dataclass(frozen=True)
class Money:
    """Value object representing a monetary amount in a given currency."""
    amount:   float
    currency: str = "USD"

    def __post_init__(self) -> None:
        if not self.currency or len(self.currency) != 3:
            raise ValueError(f"Currency must be a 3-letter ISO code, got {self.currency!r}")

    def __add__(self, other: "Money") -> "Money":
        if other.currency != self.currency:
            raise ValueError(
                f"Cannot add Money of different currencies: "
                f"{self.currency} + {other.currency}"
            )
        return Money(self.amount + other.amount, self.currency)

    def __sub__(self, other: "Money") -> "Money":
        if other.currency != self.currency:
            raise ValueError(
                f"Cannot subtract Money of different currencies: "
                f"{self.currency} - {other.currency}"
            )
        return Money(self.amount - other.amount, self.currency)

    def __str__(self) -> str:
        return f"{self.amount:.2f} {self.currency}"


@dataclass(frozen=True)
class Price:
    """Value object representing a market price in a given currency."""
    value:    float
    currency: str = "USD"

    def __post_init__(self) -> None:
        if self.value < 0:
            raise ValueError(f"Price cannot be negative, got {self.value}")
