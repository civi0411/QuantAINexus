"""
QuantAINexus — _kernel/registry/__init__.py
"""
from .registry import (
    RegistryHub,
    Category,
    register,
    registry,
    Registry,
    FACTOR,
    BACKTEST,
    EXEC_ALGO,
    PROCESSOR,
    LABELER,
    METRIC,
    QUANT,
)

__all__ = [
    "RegistryHub",
    "Category",
    "register",
    "registry",
    "Registry",
    # Legacy shims
    "FACTOR",
    "BACKTEST",
    "EXEC_ALGO",
    "PROCESSOR",
    "LABELER",
    "METRIC",
    "QUANT",
]
