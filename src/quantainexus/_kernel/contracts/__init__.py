"""
QuantAINexus — _kernel/contracts/__init__.py

All 12 contract Protocols (Article V of Architectural Constitution v3.0).
"""
from .data_source import DataSource
from .transformer import Transformer
from .method import Method
from .trainer import Trainer
from .optimizer import Optimizer, PortfolioOptimizer
from .exec_algo import ExecAlgo
from .execution_venue import ExecutionVenue
from .evaluator import Evaluator
from .agent import Agent
from .lifecycle_hook import LifecycleHook
from .artifact_store import ArtifactStore
from .risk_check_provider import RiskCheckProvider

__all__ = [
    # Contract #1
    "DataSource",
    # Contract #2
    "Transformer",
    # Contract #3
    "Method",
    # Contract #4
    "Trainer",
    # Contract #5
    "Optimizer",
    "PortfolioOptimizer",   # backward compat alias
    # Contract #6
    "ExecAlgo",
    # Contract #7
    "ExecutionVenue",
    # Contract #8
    "Evaluator",
    # Contract #9
    "Agent",
    # Contract #10
    "LifecycleHook",
    # Contract #11
    "ArtifactStore",
    # Contract #12
    "RiskCheckProvider",
]
