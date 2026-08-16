from typing import Protocol
from ..domain.order import Order
from ..domain.portfolio import Portfolio

class ExecutionVenue(Protocol):
    """
    Contract cho môi trường thực thi lệnh (Live Broker, Paper, Backtest).
    """
    def submit_order(self, order: Order) -> None:
        ...
        
    def cancel_order(self, order_id: str) -> None:
        ...
        
    def get_portfolio(self) -> Portfolio:
        ...
