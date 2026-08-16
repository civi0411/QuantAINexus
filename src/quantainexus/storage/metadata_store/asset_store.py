"""
production/collaboration/strategy_registry.py — Enterprise Strategy Registry.
"""
from dataclasses import dataclass, field
from typing import Literal, List, Dict, Any, Optional
from datetime import datetime

@dataclass
class Approval:
    user: str
    role: str
    status: str
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class Deployment:
    env: str
    status: str
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class Strategy:
    id: str
    name: str
    version: str
    author: str
    status: Literal["research", "review", "paper", "live", "archived"]
    config: Dict[str, Any]
    code: str
    metrics: Dict[str, Any]
    guardian_report: Dict[str, Any]
    plugins: List[str]
    dev_contact: str = ""
    trader_contact: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    approvals: List[Approval] = field(default_factory=list)
    deployments: List[Deployment] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)


class StrategyRegistry:
    """Mock database for Strategy lifecycle management."""
    _store: Dict[str, Strategy] = {}

    @classmethod
    def save(cls, strategy: Strategy) -> None:
        strategy.updated_at = datetime.now()
        cls._store[strategy.id] = strategy

    @classmethod
    def get(cls, strategy_id: str) -> Optional[Strategy]:
        return cls._store.get(strategy_id)

    @classmethod
    def list_all(cls) -> List[Strategy]:
        return list(cls._store.values())
