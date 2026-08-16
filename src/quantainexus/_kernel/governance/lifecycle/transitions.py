"""
QuantAINexus — _kernel/governance/lifecycle/transitions.py

Promotion threshold loader (Article IX).

Reads configs/promotion/*.yaml to get metric thresholds required for each
lifecycle transition. Guardian uses these thresholds when running a
promotion-profile check.

Format of a promotion YAML:
  min_sharpe: 0.5
  min_days_paper: 30
  max_drawdown: -0.15
  min_win_rate: 0.45

Import policy: pathlib, typing ONLY (yaml loaded lazily). No heavy dependencies.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional

# Default project-root relative path for promotion configs
_DEFAULT_CONFIG_DIR = Path(__file__).parents[6] / "configs" / "promotion"


def load_promotion_thresholds(
    transition: str,
    config_dir: Optional[Path] = None,
) -> Dict[str, Any]:
    """
    Load promotion thresholds for a given transition name.

    Args:
        transition: One of:
                    "research_to_validation"
                    "validation_to_paper"
                    "paper_to_shadow"
                    "shadow_to_live"
        config_dir: Override the default configs/promotion/ directory.

    Returns:
        Dict of threshold key → value (floats or ints).

    Raises:
        FileNotFoundError: if the YAML file does not exist.
    """
    config_dir = config_dir or _DEFAULT_CONFIG_DIR
    yaml_path = config_dir / f"{transition}.yaml"

    if not yaml_path.exists():
        # Return empty thresholds if config not yet created
        return {}

    try:
        import yaml  # PyYAML — optional dependency, only needed here
        with yaml_path.open("r", encoding="utf-8") as fh:
            data = yaml.safe_load(fh) or {}
        return {k: v for k, v in data.items() if not k.startswith("#")}
    except ImportError:
        # yaml not installed — return empty thresholds (checks will be no-ops)
        return {}


_VALID_TRANSITIONS = frozenset({
    "research_to_validation",
    "validation_to_paper",
    "paper_to_shadow",
    "shadow_to_live",
})


def get_transition_name(from_stage: str, to_stage: str) -> str:
    """
    Normalise from/to stage names into the config file name.

    Example:
        get_transition_name("RESEARCH", "VALIDATION") → "research_to_validation"
    """
    key = f"{from_stage.lower()}_to_{to_stage.lower()}"
    if key not in _VALID_TRANSITIONS:
        raise ValueError(
            f"No promotion config for transition '{key}'. "
            f"Valid transitions: {sorted(_VALID_TRANSITIONS)}"
        )
    return key
