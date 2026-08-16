from typing import Protocol, Any

class Trainer(Protocol):
    """
    Contract to orchestrate training loop.
    """
    def fit(self, model: Any, train_data: Any, val_data: Any = None) -> Any:
        ...
        
    def test(self, model: Any, test_data: Any) -> Any:
        ...
        
    def predict(self, model: Any, data: Any) -> Any:
        ...
