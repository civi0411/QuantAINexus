"""
QuantAINexus — _kernel/contracts/risk_check_provider.py

RiskCheckProvider Contract #12 (Article V).
Provides Barra-style factor risk model data to the Governance layer.

The Barra covariance model:  V = X F X^T + Δ
  where:
    X = factor exposure matrix (assets × factors)
    F = factor covariance matrix (factors × factors)
    Δ = specific risk diagonal matrix (assets × assets)

Guardian uses this to compute ex-ante portfolio risk during promotion checks.
By depending only on this contract (not on qnx_trading.risk), Governance
remains cleanly separated from Adapter implementations.

Import policy: typing ONLY. No heavy dependencies.
"""
from __future__ import annotations

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class RiskCheckProvider(Protocol):
    """
    Contract for providing factor model risk data to the Governance layer.

    Governance ONLY depends on this contract — it never imports qnx_trading.risk
    or any concrete risk implementation directly.
    """

    def factor_exposure(self) -> Any:
        """
        Return the factor exposure matrix X of shape (n_assets × n_factors).
        Compatible with numpy ndarray or Polars DataFrame.
        """
        ...

    def factor_covariance(self) -> Any:
        """
        Return the factor covariance matrix F of shape (n_factors × n_factors).
        """
        ...

    def specific_risk(self) -> Any:
        """
        Return the specific (idiosyncratic) risk diagonal Δ, shape (n_assets,).
        """
        ...
