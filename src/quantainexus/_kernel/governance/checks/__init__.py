"""
QuantAINexus — _kernel/governance/checks/__init__.py

System-level Guardian checks (Article VII §7.3 + Article XII §12.D).

Profile → checks mapping:
  "lab":        no checks (maximum speed for quick experiments)
  "research":   schema + pit + determinism
  "production": schema + pit + determinism + resource + security

RULE: Checks here are system-level ONLY.
      Domain-specific checks (e.g. leakage detection) live in qnx_data.quality
      and are called via a thin wrapper in checks/leakage.py.
"""
from __future__ import annotations

from typing import List

from ..check import GuardianCheck
from .schema import SchemaCheck
from .pit import PITCheck
from .determinism import DeterminismCheck
from .resource import ResourceCheck
from .security import SecurityCheck


def load_checks_for_profile(profile: str) -> List[GuardianCheck]:
    """
    Return the list of GuardianChecks appropriate for a named profile.

    Args:
        profile: "lab" | "research" | "production"

    Returns:
        List of instantiated GuardianCheck objects.
    """
    if profile == "lab":
        return []

    if profile == "research":
        return [
            SchemaCheck(),
            PITCheck(),
            DeterminismCheck(),
        ]

    if profile == "production":
        return [
            SchemaCheck(),
            PITCheck(),
            DeterminismCheck(),
            ResourceCheck(),
            SecurityCheck(),
        ]

    # Unknown profile → fall back to lab (no checks) with a warning
    import logging
    logging.getLogger(__name__).warning(
        "Unknown guardian profile %r — defaulting to 'lab' (no checks). "
        "Valid profiles: lab, research, production",
        profile,
    )
    return []


__all__ = [
    "load_checks_for_profile",
    "SchemaCheck",
    "PITCheck",
    "DeterminismCheck",
    "ResourceCheck",
    "SecurityCheck",
]
