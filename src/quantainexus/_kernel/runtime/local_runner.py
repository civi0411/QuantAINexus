"""
QuantAINexus — _kernel/runtime/local_runner.py

LocalRunner — Phase 1 execution engine (Article VII §7.3).

CRITICAL DESIGN RULES:
  1. LocalRunner is the ONLY place that raises GuardianBlockedError.
  2. Guardian returns HookResult — Runner reads it and decides to raise or not.
  3. post_execute hooks must never block; failures are silently dropped.
  4. Node execution is dispatched via RegistryHub (looked up by node.name).

Import policy: typing + internal modules ONLY. No heavy dependencies.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

from ..contracts.lifecycle_hook import LifecycleHook
from ..domain.context import ResearchContext
from ..errors import GuardianBlockedError
from ..graph.graph import Graph
from ..graph.node import Node
from ..registry.registry import RegistryHub, Category

logger = logging.getLogger(__name__)


class LocalRunner:
    """
    Single-process, sequential DAG executor.

    The runner:
      1. Calls pre_execute on every hook before each node.
      2. If any hook returns a blocking HookResult → raises GuardianBlockedError.
      3. Resolves and executes the node via RegistryHub.
      4. Calls post_execute on every hook (silently drops errors).

    This is the ONLY runner in Phase 1. Distributed runners (Dask, Ray) come
    in Phase 2 in qnx_infrastructure.
    """

    def __init__(
        self,
        hooks: Optional[List[LifecycleHook]] = None,
    ) -> None:
        self._hooks: List[LifecycleHook] = list(hooks or [])

    # ── Factory ──────────────────────────────────────────────────────────

    @classmethod
    def from_config(cls, config: Dict[str, Any]) -> "LocalRunner":
        """
        Build a LocalRunner from a config dict.
        Config shape: {"guardian": "lab" | "research" | "production"}
        """
        from ..governance.lifecycle.guardian import Guardian
        profile = config.get("guardian", "lab")
        guardian = Guardian.from_profile(profile)
        return cls(hooks=[guardian])

    # ── Main entry point ─────────────────────────────────────────────────

    def run(self, graph: Graph, ctx: ResearchContext) -> Dict[str, Any]:
        """
        Execute the graph in topological order.

        Returns:
            dict mapping node_id → result of that node's execution.

        Raises:
            GuardianBlockedError if any hook blocks a node.
            CyclicGraphError if the graph has a cycle (from topological_order).
        """
        ordered_nodes = graph.topological_order()
        results: Dict[str, Any] = {}

        for node in ordered_nodes:
            logger.debug(
                "pre_execute node=%s kind=%s trace_id=%s",
                node.id, node.kind, ctx.trace_id,
            )

            # ── PRE-EXECUTE: Guardian VETO ────────────────────────────
            for hook in self._hooks:
                try:
                    hook_result = hook.pre_execute(node, ctx)
                except Exception as exc:
                    # A hook itself crashed — treat as non-blocking, log only
                    logger.warning("Hook %r raised in pre_execute: %s", hook, exc)
                    continue

                if hook_result and hook_result.blocking:
                    # SOLE raise point for Guardian blocks
                    raise GuardianBlockedError(
                        node=node.id,
                        reasons=list(hook_result.reasons),
                    )

            # ── EXECUTE ───────────────────────────────────────────────
            result = self._execute_node(node, ctx, results)
            results[node.id] = result

            logger.debug(
                "post_execute node=%s trace_id=%s",
                node.id, ctx.trace_id,
            )

            # ── POST-EXECUTE: Audit (never blocks) ────────────────────
            for hook in self._hooks:
                try:
                    hook.post_execute(node, ctx, result)
                except Exception as exc:
                    logger.warning(
                        "Hook %r raised in post_execute (suppressed): %s", hook, exc
                    )

        return results

    # ── Node dispatch ────────────────────────────────────────────────────

    def _execute_node(
        self,
        node: Node,
        ctx: ResearchContext,
        prior_results: Dict[str, Any],
    ) -> Any:
        """
        Resolve the component from RegistryHub and execute it.

        The node.kind drives Category resolution:
          "data"      → Category.DATA_SOURCE  → DataSource.load()
          "transform" → Category.TRANSFORMER  → Transformer.transform()
          "method"    → Category.METHOD        → Method.fit() / predict()
          "evaluate"  → Category.EVALUATOR     → Evaluator.evaluate()
          "execution" → Category.EXECUTION_VENUE → ExecutionVenue.submit()
        """
        _CATEGORY_MAP = {
            "data":      Category.DATA_SOURCE,
            "transform": Category.TRANSFORMER,
            "method":    Category.METHOD,
            "evaluate":  Category.EVALUATOR,
            "execution": Category.EXECUTION_VENUE,
        }

        category = _CATEGORY_MAP.get(node.kind)
        if category is None:
            raise ValueError(f"Unknown node kind: {node.kind!r}")

        # Build the component instance
        component_cls = RegistryHub.get(category, node.name)
        component = component_cls(**node.params)

        # Gather upstream inputs
        inputs = [prior_results[dep] for dep in node.depends_on]

        # Dispatch by kind
        if node.kind == "data":
            return component.load(as_of=ctx.pit_as_of, **node.params)

        elif node.kind == "transform":
            data = inputs[0] if inputs else None
            return component.transform(data, ctx)

        elif node.kind == "method":
            data = inputs[0] if inputs else None
            return component.predict(data)

        elif node.kind == "evaluate":
            return component.evaluate(*inputs, ctx=ctx)

        elif node.kind == "execution":
            return component.submit(*inputs)

        return None
