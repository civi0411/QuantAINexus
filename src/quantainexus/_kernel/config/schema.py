"""
QuantAINexus — _kernel/config/schema.py

QuantAINexusConfig — Single Source of Truth for all runtime configuration
(Article XIV of Architectural Constitution v3.0).

RULES:
  - ALL config comes from this class. No os.getenv() anywhere in business code.
  - Values are injected via constructor or loaded from YAML + env vars.
  - The config is frozen (immutable) once created.
  - Every class that needs config receives it via constructor injection.

Environment variable prefix: QNX_
  QNX_MODE=production
  QNX_GUARDIAN_PROFILE=production
  QNX_METADATA_STORE_URL=postgresql://...
  QNX_ARTIFACT_STORE_PATH=/mnt/artifacts
  QNX_SEED=42
  QNX_TELEMETRY_ENABLED=true
"""
from __future__ import annotations

from pathlib import Path
from typing import Literal, Optional

# Pydantic v2 BaseSettings — optional dependency for the config layer
try:
    from pydantic_settings import BaseSettings, SettingsConfigDict

    class QuantAINexusConfig(BaseSettings):
        """
        Central configuration object for a QuantAINexus runtime.

        Loaded from (in priority order):
          1. Constructor kwargs
          2. Environment variables (prefix QNX_)
          3. Loaded YAML file (via loader.py)
          4. Defaults defined here
        """

        model_config = SettingsConfigDict(
            env_prefix="QNX_",
            frozen=True,
            extra="ignore",
        )

        # Runtime mode
        mode: Literal["research", "validation", "production"] = "research"

        # Guardian profile applied by LocalRunner
        guardian_profile: Literal["lab", "research", "production"] = "lab"

        # Storage
        metadata_store_url:   str  = "sqlite:///./qnx.db"
        artifact_store_path:  Path = Path("./artifacts")

        # Reproducibility
        seed: Optional[int] = None

        # Observability
        telemetry_enabled: bool = True

        # Native acceleration
        native_enabled: bool = True

        @property
        def is_production(self) -> bool:
            return self.mode == "production"

        @property
        def is_research(self) -> bool:
            return self.mode == "research"

except ImportError:
    # Pydantic-settings not installed — provide a minimal dataclass fallback
    import warnings
    warnings.warn(
        "pydantic-settings not installed. QuantAINexusConfig will use a "
        "plain dataclass with no env-var support. "
        "Install with: pip install pydantic-settings",
        ImportWarning,
        stacklevel=1,
    )

    from dataclasses import dataclass, field

    @dataclass(frozen=True)
    class QuantAINexusConfig:  # type: ignore[no-redef]
        mode:                 str            = "research"
        guardian_profile:     str            = "lab"
        metadata_store_url:   str            = "sqlite:///./qnx.db"
        artifact_store_path:  Path           = field(default_factory=lambda: Path("./artifacts"))
        seed:                 Optional[int]  = None
        telemetry_enabled:    bool           = True
        native_enabled:       bool           = True

        @property
        def is_production(self) -> bool:
            return self.mode == "production"

        @property
        def is_research(self) -> bool:
            return self.mode == "research"
