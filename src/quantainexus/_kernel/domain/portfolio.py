"""
QuantAINexus — _kernel/domain/portfolio.py

Portfolio Aggregate Root (Article IV §4.2).

Invariant: actual leverage must never exceed max_leverage.
apply_fill() is the ONLY way to mutate positions — always returns a NEW Portfolio.

Import policy: ONLY dataclasses, typing. No heavy dependencies.
"""
from __future__ import annotations

from dataclasses import dataclass, field, replace
from typing import Optional

from .order import Order, OrderSide
from ..errors import LeverageExceededError


@dataclass(frozen=True)
class Position:
    """Value object — a single asset holding."""
    asset_id:      str
    quantity:      float
    average_price: float

    @property
    def market_value(self) -> float:
        return self.quantity * self.average_price


@dataclass
class Portfolio:
    """
    Aggregate Root for positions and cash.

    Attributes:
        id:           Unique portfolio identifier.
        cash:         Available cash (positive = long cash).
        positions:    Map of asset_id → Position.
        max_leverage: Hard limit on gross leverage (default 1.0 = no leverage).
    """
    id:           str
    cash:         float
    positions:    dict[str, Position] = field(default_factory=dict)
    max_leverage: float               = 1.0

    # ── Derived quantities ────────────────────────────────────────────────

    @property
    def gross_market_value(self) -> float:
        return sum(abs(p.market_value) for p in self.positions.values())

    @property
    def net_asset_value(self) -> float:
        return self.cash + sum(p.market_value for p in self.positions.values())

    @property
    def leverage(self) -> float:
        nav = self.net_asset_value
        if nav == 0:
            return 0.0
        return self.gross_market_value / nav

    # ── Mutations (always return NEW Portfolio) ───────────────────────────

    def apply_fill(self, order: Order, fill_price: float) -> "Portfolio":
        """
        Apply a fill to the portfolio and return a NEW Portfolio.
        Raises LeverageExceededError if the resulting leverage > max_leverage.
        """
        new_positions = dict(self.positions)
        asset_id = str(order.asset_id)

        existing = new_positions.get(asset_id)
        qty_delta = order.quantity if order.side is OrderSide.BUY else -order.quantity
        cash_delta = -qty_delta * fill_price

        if existing is None:
            if qty_delta != 0:
                new_positions[asset_id] = Position(
                    asset_id=asset_id,
                    quantity=qty_delta,
                    average_price=fill_price,
                )
        else:
            new_qty = existing.quantity + qty_delta
            if new_qty == 0:
                del new_positions[asset_id]
            else:
                # Volume-weighted average price update for additions
                if (existing.quantity > 0 and qty_delta > 0) or \
                   (existing.quantity < 0 and qty_delta < 0):
                    total_cost = abs(existing.quantity) * existing.average_price \
                                 + abs(qty_delta) * fill_price
                    new_avg = total_cost / abs(new_qty)
                else:
                    new_avg = existing.average_price  # partial close, keep avg
                new_positions[asset_id] = Position(
                    asset_id=asset_id,
                    quantity=new_qty,
                    average_price=new_avg,
                )

        candidate = replace(self, positions=new_positions, cash=self.cash + cash_delta)
        candidate._check_leverage_invariant()
        return candidate

    def _check_leverage_invariant(self) -> None:
        actual = self.leverage
        if actual > self.max_leverage + 1e-9:
            raise LeverageExceededError(actual=actual, maximum=self.max_leverage)
