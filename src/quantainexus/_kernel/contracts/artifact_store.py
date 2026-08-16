from typing import Protocol
from ..domain.asset import Asset

class ArtifactStore(Protocol):
    """
    Contract cho hệ thống lưu trữ Asset (Metadata + Data/Model weights).
    """
    def save(self, asset: Asset, payload: bytes) -> str:
        ...
        
    def load(self, asset_id: str) -> bytes:
        ...
        
    def get_metadata(self, asset_id: str) -> Asset:
        ...
