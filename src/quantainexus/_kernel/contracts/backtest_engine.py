from typing import Protocol, Any

class BacktestEngine(Protocol):
    """
    Contract for running historical simulations.
    """
    def run(self, strategy: Any, data: Any) -> Any:
        ...
