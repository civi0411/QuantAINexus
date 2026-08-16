# QuantAINexus

**Status:** v4.1 Canonical Architecture — Built on Polars, Rust (PyO3), and strict Domain-Driven Design.

## Core Philosophy
1. **One Domain**: All operations (Research, Paper, Live) share the exact same canonical `Asset`, `Order`, `Portfolio`, `Signal` models.
2. **One Engine**: The `_kernel` module is pure (0 external dependencies) and orchestrates everything via a DAG Runner.
3. **Zero-Copy**: Polars DataFrames and Apache Arrow (via `qnx-arrow`) ensure instantaneous data passing between Python and Rust.
4. **Anti-Leakage**: The `Guardian` intercepts all DAG nodes and validates Point-in-Time (PIT) integrity.

## Architecture Guidelines
- `_kernel/`: The heart of the system. Domain models, interfaces, Task orchestration.
- `native/crates/`: Rust workspace containing all performance hotpaths.
- `data/`, `methods/`, `execution/`, `portfolio/`, `evaluate/`, `agents/`, `storage/`: Concrete implementations adhering to `_kernel/contracts`.

For detailed architecture logic, refer to `docs/architecture.md`.
