from typing import Protocol, Any, Dict

class Evaluator(Protocol):
    """
    Contract for evaluating model predictions.
    """
    def evaluate(self, predictions: Any, actuals: Any) -> Dict[str, float]:
        ...
