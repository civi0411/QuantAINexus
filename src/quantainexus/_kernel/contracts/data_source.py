from typing import Protocol, Iterator, Any
from ..domain.value_objects import KnowledgeTime
from ..domain.asset import Asset

class DataSource(Protocol):
    """
    Contract cho mọi data source.
    as_of bắt buộc → Point-in-Time safety.
    modality khai báo loại dữ liệu → fusion engine biết cách align.
    """
    modality: str   # "ohlcv" | "tick" | "orderbook" | "fundamental" | "text" | "sentiment" | "esg" | "macro"
    
    def load(self, *, as_of: KnowledgeTime, **kwargs) -> Any:
        ...

    def stream(self, **kwargs) -> Iterator[Any]:
        ...
