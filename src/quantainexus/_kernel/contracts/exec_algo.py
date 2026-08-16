"""
QuantAINexus — _kernel/contracts/exec_algo.py

ExecAlgo Contract #6 (Article V).
Slices a parent order into child orders for algorithmic execution (TWAP, VWAP, POV, Iceberg).

RULE: No polars import here — contracts must be pure Python + typing.
Import policy: typing ONLY. No heavy dependencies.
"""
from __future__ import annotations

from typing import Any, List, Protocol, runtime_checkable

from ..domain.order import Order


@runtime_checkable
class ExecAlgo(Protocol):
    """
    Contract for execution algorithms that slice parent orders.

    The slice() method is preferred (matches Constitution §V).
    execute() is kept as a backward-compat alias.
    """

    def slice(self, order: Order, market_state: Any) -> List[Any]:
        """
        Slice a parent order into child orders.

        Args:
            order:        Parent order to be sliced.
            market_state: Market data (e.g. Polars DataFrame, order book snapshot).

        Returns:
            List of child Order objects or execution schedules.
        """
        ...

    def execute(self, order: Order, market_data: Any) -> List[Any]:
        """Backward-compat alias for slice()."""
        return self.slice(order, market_data)
