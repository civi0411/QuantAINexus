# QuantAINexus (QNX) 🐙

A next-generation High-Frequency Quantitative AI Framework designed to unify the chasm between Research and Production.

> **One Domain · One Engine · One Lifecycle · Multiple Deployments**

## Overview
QuantAINexus eliminates the "research in Pandas/Jupyter, rewrite in C++/Java for live" anti-pattern. 
It offers a unified API utilizing a lazy-evaluated, DAG-based engine powered by Polars and Rust to process millions of tick-level market data points with sub-millisecond latency.

## Features
- **Zero-Copy Performance**: Rust extensions (`qnx-compute`) pass memory to Python via Apache Arrow, virtually eliminating data serialization overhead across process boundaries.
- **Strict Point-In-Time (PIT)**: The `Guardian` validation engine ensures future data leakage is mathematically impossible during research.
- **Unified Contracts**: Agents, forecasting models, and execution venues all speak the same core domain language, supporting complex multi-asset statistical arbitrage and algorithmic execution routing.

## Project Structure
The repository is structured to separate high-performance execution from high-level Python API contracts:
- `native/crates/qnx-compute`: Core Rust backend for heavy computational lifting and zero-copy Arrow memory transfers.
- `native/crates/qnx-arrow`: FFI translation layer between Polars/Rust and Python memory spaces.
- `src/quantainexus/_kernel/governance/lifecycle/`: Home of the `Guardian` engine, enforcing strict Point-In-Time (PIT) validation checks.
- `src/quantainexus/portfolio/`: Modular portfolio construction and position sizing logic.

## Documentation
- [Architecture Details](docs/architecture.md)
- [Getting Started](docs/getting_started.md)
- [API Reference](docs/api_reference.md)

## Status
Under active development (Sprint 4 of the v4.1 Architecture Plan).