from dataclasses import dataclass
from enum import Enum, auto

class OrderSide(Enum):
    BUY = auto()
    SELL = auto()

@dataclass(frozen=True)
class Order:
    id: str
    asset_id: str
    side: OrderSide
    quantity: float
    price: float
    idempotency_key: str    # bắt buộc — enforce bằng contract test, chống double-submit
