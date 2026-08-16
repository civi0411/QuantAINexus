"""
QuantAINexus — _kernel/registry/registry.py

RegistryHub — the ONE global registry (Article VI).

Design rules:
  1. ONE RegistryHub in the entire system. No local registries anywhere.
  2. Keys are (Category, name) tuples — not raw strings.
  3. @register decorator is the only public registration API.
  4. Every @register must have a corresponding Contract Test in tests/contract/.
  5. get() raises UnknownComponentError (from _kernel/errors.py), not KeyError.
  6. Duplicate names raise DuplicateRegistrationError unless overwrite=True.

Import policy: enum, typing ONLY. No heavy dependencies.
"""
from __future__ import annotations

import inspect
from enum import Enum, auto
from typing import Any, Callable, Dict, List, Optional, Tuple, Type

from ..errors import DuplicateRegistrationError, UnknownComponentError


class Category(Enum):
    """
    All recognised component categories in QuantAINexus.
    Adding a new Category requires an ADR (Architecture Decision Record).
    """
    DATA_SOURCE      = auto()   # implements DataSource contract
    TRANSFORMER      = auto()   # implements Transformer contract
    METHOD           = auto()   # implements Method contract (ML, DL, TS, LLM)
    TRAINER          = auto()   # implements Trainer contract
    OPTIMIZER        = auto()   # implements Optimizer contract
    EXEC_ALGO        = auto()   # implements ExecAlgo contract (TWAP, VWAP)
    EXECUTION_VENUE  = auto()   # implements ExecutionVenue contract
    EVALUATOR        = auto()   # implements Evaluator contract
    AGENT            = auto()   # implements Agent contract
    ARTIFACT_STORE   = auto()   # implements ArtifactStore contract
    LABELER          = auto()   # implements Labeler contract
    FACTOR           = auto()   # implements Factor/feature computation
    BACKTEST_ENGINE  = auto()   # implements BacktestEngine contract
    METRIC           = auto()   # standalone metric functions
    PROCESSOR        = auto()   # implements Processor (data cleaning)


# Internal store type: {Category: {name: (class, metadata_dict)}}
_Store = Dict[Category, Dict[str, Tuple[Type[Any], dict]]]


class RegistryHub:
    """
    Global singleton registry.

    Usage:
        # Registration (via decorator):
        @RegistryHub.register(Category.METHOD, "lightgbm")
        class LightGBMMethod: ...

        # Retrieval:
        cls = RegistryHub.get(Category.METHOD, "lightgbm")
        instance = cls(**params)

        # Listing:
        RegistryHub.list_category(Category.METHOD)
    """

    _store: _Store = {}

    # ── Registration ─────────────────────────────────────────────────────

    @classmethod
    def register(
        cls,
        category: Category,
        name: str,
        *,
        description: str = "",
        tags: Optional[List[str]] = None,
        overwrite: bool = False,
    ) -> Callable[[Type[Any]], Type[Any]]:
        """
        Class decorator that registers the decorated class into this category.

        Raises:
            DuplicateRegistrationError if name already exists and overwrite=False.
        """
        def decorator(klass: Type[Any]) -> Type[Any]:
            cls._add(
                category,
                name,
                klass,
                description=description,
                tags=tags or [],
                overwrite=overwrite,
            )
            return klass

        return decorator

    @classmethod
    def _add(
        cls,
        category: Category,
        name: str,
        klass: Type[Any],
        *,
        description: str = "",
        tags: Optional[List[str]] = None,
        overwrite: bool = False,
    ) -> None:
        """Internal: add a class directly (for programmatic registration)."""
        if category not in cls._store:
            cls._store[category] = {}

        if name in cls._store[category] and not overwrite:
            raise DuplicateRegistrationError(category, name)

        docstring = inspect.getdoc(klass) or ""
        meta: dict = {
            "name":        name,
            "category":    category,
            "class":       klass.__qualname__,
            "module":      klass.__module__,
            "description": description or (docstring.strip().splitlines()[0] if docstring else ""),
            "tags":        tags or [],
        }
        cls._store[category][name] = (klass, meta)

    # ── Retrieval ────────────────────────────────────────────────────────

    @classmethod
    def get(cls, category: Category, name: str) -> Type[Any]:
        """
        Return the registered class for (category, name).

        Raises:
            UnknownComponentError if not found.
        """
        try:
            klass, _meta = cls._store[category][name]
            return klass
        except KeyError:
            raise UnknownComponentError(category, name)

    @classmethod
    def build(
        cls,
        category: Category,
        name: str,
        **kwargs: Any,
    ) -> Any:
        """Convenience: get the class and instantiate it with kwargs."""
        klass = cls.get(category, name)
        return klass(**kwargs)

    # ── Inspection ───────────────────────────────────────────────────────

    @classmethod
    def list_category(cls, category: Category) -> Dict[str, dict]:
        """Return metadata for all registered components in a category."""
        return {name: meta for name, (_klass, meta) in cls._store.get(category, {}).items()}

    @classmethod
    def list_all(cls) -> Dict[Category, Dict[str, dict]]:
        """Return metadata for every registered component."""
        return {
            cat: {name: meta for name, (_klass, meta) in names.items()}
            for cat, names in cls._store.items()
        }

    @classmethod
    def categories(cls) -> List[Category]:
        """Return all categories that have at least one registered component."""
        return list(cls._store.keys())

    @classmethod
    def contains(cls, category: Category, name: str) -> bool:
        """Check membership without raising."""
        return name in cls._store.get(category, {})

    # ── Test utilities ───────────────────────────────────────────────────

    @classmethod
    def clear(cls) -> None:
        """
        Reset the registry. Use ONLY in tests (conftest.py teardown).
        Never call in production code.
        """
        cls._store.clear()


# ── Backward-compat shim ─────────────────────────────────────────────────────
# The old Registry + register() function API is kept so existing adapter code
# that uses @FACTOR.register_module() or @register("factor", "rsi") continues
# to work during Phase 1. It will be removed in Phase 2.

class _LegacyRegistryShim:
    """
    Shim that makes the old string-based registry calls delegate to RegistryHub.
    Each module-level registry (FACTOR, BACKTEST, etc.) is one of these shims.
    """
    def __init__(self, category: Category) -> None:
        self._category = category

    def register_module(
        self,
        name: Optional[str] = None,
        *,
        force: bool = False,
        **kwargs: Any,
    ) -> Callable[[Type[Any]], Type[Any]]:
        """mmengine-style @registry.register_module() decorator."""
        def decorator(klass: Type[Any]) -> Type[Any]:
            component_name = name or klass.__name__.lower()
            RegistryHub._add(
                self._category,
                component_name,
                klass,
                overwrite=force,
            )
            return klass
        return decorator

    def build(self, cfg: dict, **kwargs: Any) -> Any:
        name = cfg.get("name") or cfg.get("type", "")
        params = {k: v for k, v in cfg.items() if k not in ("name", "type")}
        params.update(kwargs)
        return RegistryHub.build(self._category, name, **params)


# Module-level legacy singletons (used by existing adapters)
FACTOR          = _LegacyRegistryShim(Category.FACTOR)
BACKTEST        = _LegacyRegistryShim(Category.BACKTEST_ENGINE)
EXEC_ALGO       = _LegacyRegistryShim(Category.EXEC_ALGO)
PROCESSOR       = _LegacyRegistryShim(Category.PROCESSOR)
LABELER         = _LegacyRegistryShim(Category.LABELER)
METRIC          = _LegacyRegistryShim(Category.METRIC)
QUANT           = _LegacyRegistryShim(Category.METHOD)

# Legacy top-level aliases
registry  = RegistryHub
Registry  = RegistryHub


def register(
    plugin_type: str,
    name: str,
    *,
    description: str = "",
    tags: Optional[List[str]] = None,
    overwrite: bool = False,
) -> Callable[[Type[Any]], Type[Any]]:
    """
    Backward-compat string-based decorator.
    Maps plugin_type string → Category enum via _LEGACY_TYPE_MAP.
    """
    _LEGACY_TYPE_MAP: Dict[str, Category] = {
        "data_source":     Category.DATA_SOURCE,
        "transformer":     Category.TRANSFORMER,
        "method":          Category.METHOD,
        "trainer":         Category.TRAINER,
        "optimizer":       Category.OPTIMIZER,
        "exec_algo":       Category.EXEC_ALGO,
        "execution_venue": Category.EXECUTION_VENUE,
        "evaluator":       Category.EVALUATOR,
        "agent":           Category.AGENT,
        "artifact_store":  Category.ARTIFACT_STORE,
        "labeler":         Category.LABELER,
        "factor":          Category.FACTOR,
        "backtest":        Category.BACKTEST_ENGINE,
        "metric":          Category.METRIC,
        "processor":       Category.PROCESSOR,
    }

    category = _LEGACY_TYPE_MAP.get(plugin_type)
    if category is None:
        raise ValueError(
            f"Unknown plugin_type '{plugin_type}'. "
            f"Valid types: {sorted(_LEGACY_TYPE_MAP)}"
        )

    return RegistryHub.register(
        category,
        name,
        description=description,
        tags=tags,
        overwrite=overwrite,
    )
