"""
QuantAINexus — _kernel/config/loader.py

Config loader: YAML + env var merge → QuantAINexusConfig (Article XIV).
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional

from .schema import QuantAINexusConfig


def load_config(
    yaml_path: Optional[Path] = None,
    overrides: Optional[Dict[str, Any]] = None,
) -> QuantAINexusConfig:
    """
    Build a QuantAINexusConfig by merging (in priority order):
      1. overrides dict (highest priority)
      2. YAML file at yaml_path
      3. Environment variables (QNX_ prefix)
      4. Defaults

    Args:
        yaml_path: Optional path to a YAML config file.
        overrides: Optional dict of key→value to override after loading.

    Returns:
        Frozen QuantAINexusConfig instance.
    """
    base: Dict[str, Any] = {}

    # Load YAML if provided
    if yaml_path is not None and yaml_path.exists():
        try:
            import yaml
            with yaml_path.open("r", encoding="utf-8") as fh:
                loaded = yaml.safe_load(fh) or {}
            base.update(loaded)
        except ImportError:
            pass  # yaml not installed — skip file loading

    # Apply explicit overrides
    if overrides:
        base.update(overrides)

    try:
        # Pydantic-settings path — env vars are loaded automatically
        return QuantAINexusConfig(**base)
    except TypeError:
        # Plain dataclass fallback — filter to known fields only
        from dataclasses import fields
        known = {f.name for f in fields(QuantAINexusConfig)}  # type: ignore
        return QuantAINexusConfig(**{k: v for k, v in base.items() if k in known})
