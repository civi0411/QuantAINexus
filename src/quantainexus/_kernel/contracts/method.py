from typing import Protocol, Any

class Method(Protocol):
    """
    Contract cho mọi phương pháp biến đổi data. (ML, DL, LLM, Econometrics)
    """
    def fit(self, data: Any, **kwargs) -> "Method":
        ...

    def predict(self, data: Any, **kwargs) -> Any:
        ...
