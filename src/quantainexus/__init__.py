"""
QuantAINexus — Quantitative AI Framework for Research & Production.

Philosophy
----------
Research-First, Production-Capable.
Polars-native. Rust-accelerated. Guardian anti-leakage protection.
DAG-driven pipelines with full lifecycle governance.

Quick start:
    from quantainexus import register, RegistryHub, Category
    from quantainexus import GraphBuilder, ResearchContext, KnowledgeTime
    from quantainexus import LocalRunner
"""
from quantainexus.qnx import (
    register,
    registry,
    RegistryHub,
    Category,
    Task,
    TaskType,
    GraphBuilder,
    ResearchContext,
    KnowledgeTime,
    LocalRunner,
    Guardian,
    AgentBreaker,
)

__version__ = "2.0.0-alpha"

__all__ = [
    "register",
    "registry",
    "RegistryHub",
    "Category",
    "Task",
    "TaskType",
    "GraphBuilder",
    "ResearchContext",
    "KnowledgeTime",
    "LocalRunner",
    "Guardian",
    "AgentBreaker",
]
