"""
QuantAINexus — _kernel/governance/checks/resource.py

ResourceCheck — CPU and memory usage limits.
Blocking: False in research, True in production (set via profile loader).
"""
from __future__ import annotations

import os
from typing import Any

from ..check import CheckResult, GuardianCheck

_DEFAULT_MAX_MEMORY_MB = 8192   # 8 GB
_DEFAULT_MAX_CPU_PERCENT = 95.0


class ResourceCheck(GuardianCheck):
    """
    Checks current process memory and CPU usage against configured limits.
    Requires psutil (optional dependency) — gracefully degrades if not installed.
    """

    def __init__(
        self,
        max_memory_mb: float = _DEFAULT_MAX_MEMORY_MB,
        max_cpu_percent: float = _DEFAULT_MAX_CPU_PERCENT,
    ) -> None:
        self.max_memory_mb = max_memory_mb
        self.max_cpu_percent = max_cpu_percent

    @property
    def name(self) -> str:
        return "resource_limits"

    def evaluate(self, node: Any, ctx: Any) -> CheckResult:
        try:
            import psutil
            proc = psutil.Process(os.getpid())

            mem_mb = proc.memory_info().rss / (1024 * 1024)
            cpu_pct = proc.cpu_percent(interval=0.1)

            if mem_mb > self.max_memory_mb:
                return CheckResult(
                    check_name=self.name,
                    passed=False,
                    blocking=True,
                    message=(
                        f"Memory usage {mem_mb:.1f} MB exceeds limit "
                        f"{self.max_memory_mb:.1f} MB"
                    ),
                )

            if cpu_pct > self.max_cpu_percent:
                return CheckResult(
                    check_name=self.name,
                    passed=False,
                    blocking=False,  # CPU spikes are warnings, not hard blocks
                    message=(
                        f"CPU usage {cpu_pct:.1f}% exceeds threshold "
                        f"{self.max_cpu_percent:.1f}%"
                    ),
                )

            return CheckResult(check_name=self.name, passed=True, blocking=True)

        except ImportError:
            # psutil not installed — skip check with a non-blocking warning
            return CheckResult(
                check_name=self.name,
                passed=False,
                blocking=False,
                message="psutil not installed — resource limits not enforced",
            )
        except Exception as exc:
            return CheckResult(
                check_name=self.name,
                passed=False,
                blocking=False,
                message=f"Resource check raised: {exc!r}",
            )
