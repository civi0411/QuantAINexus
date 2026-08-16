"""
QuantAINexus — _kernel/contracts/optimizer.py

Optimizer Contract #5 (Article V).
Maps signals + portfolio + constraints → target weights.

RULE: No heavy imports here. polars import removed — use Any typing.
Import policy: typing ONLY. No heavy dependencies.
"""
from __future__ import annotations

from typing import Any, Dict, Protocol, runtime_checkable


@runtime_checkable
class Optimizer(Protocol):
    """
    Contract for portfolio weight optimisation algorithms.

    Implementations: MeanVariance, RiskParity, BlackLitterman, MaxSharpe, etc.
    """

    def optimize(
        self,
        signals: Any,
        portfolio: Any,
        constraints: Dict[str, Any],
    ) -> Any:
        """
        Compute target portfolio weights.

        Args:
            signals:     Signal scores per asset (e.g. Polars DataFrame).
            portfolio:   Current Portfolio aggregate root.
            constraints: Bounds, turnover limits, sector limits, etc.

        Returns:
            Target weights dict {asset_id: weight} or equivalent structure.
        """
        ...


# Backward compat alias
PortfolioOptimizer = Optimizer
