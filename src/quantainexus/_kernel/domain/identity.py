"""
QuantAINexus — _kernel/domain/identity.py

Strongly-typed identity value objects (Article IV §4.1).
These are the ONLY place where raw string IDs are wrapped into typed values.

Import policy: ONLY dataclasses, typing. No heavy dependencies.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class AssetID:
    """Unique identity of any Asset (dataset, model, strategy, backtest_result)."""
    value: str

    def __post_init__(self) -> None:
        if not self.value or not self.value.strip():
            raise ValueError("AssetID.value must be a non-empty string")

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True)
class OrderID:
    """Unique identity of an Order. Wrap before passing across boundaries."""
    value: str

    def __post_init__(self) -> None:
        if not self.value or not self.value.strip():
            raise ValueError("OrderID.value must be a non-empty string")

    def __str__(self) -> str:
        return self.value
