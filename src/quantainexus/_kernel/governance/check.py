"""
QuantAINexus — _kernel/governance/check.py

Core governance data structures (Article VII §7.1).

CheckResult:   The output of a single GuardianCheck.evaluate() call.
HookResult:    The aggregated output of Guardian.pre_execute() — what Runner reads.
GuardianCheck: Abstract base for every check plugged into Guardian.

RULE: GuardianCheck.evaluate() NEVER raises.
      It always returns a CheckResult with passed=False if something is wrong.

Import policy: dataclasses, abc, typing ONLY. No heavy dependencies.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class CheckResult:
    """
    Result of a single guard check evaluation.

    Attributes:
        check_name: Human-readable name of the check (e.g. "pit_integrity").
        passed:     True if the check passed; False otherwise.
        blocking:   True means Guardian will VETO execution (hard block).
                    False means it's a warning only (soft, non-blocking).
        message:    Descriptive message, especially when passed=False.
    """
    check_name: str
    passed:     bool
    blocking:   bool
    message:    str = ""

    def __str__(self) -> str:
        status = "PASS" if self.passed else ("BLOCK" if self.blocking else "WARN")
        return f"[{status}] {self.check_name}: {self.message}"


@dataclass(frozen=True)
class HookResult:
    """
    Aggregated result returned by Guardian.pre_execute() to LocalRunner.

    Attributes:
        blocking: True means LocalRunner MUST raise GuardianBlockedError.
        reasons:  Tuple of all CheckResults that caused a block.
    """
    blocking: bool
    reasons:  tuple[CheckResult, ...] = field(default_factory=tuple)

    @classmethod
    def allow(cls) -> "HookResult":
        """Convenience constructor for a passing result."""
        return cls(blocking=False)

    @classmethod
    def block(cls, reasons: list[CheckResult]) -> "HookResult":
        """Convenience constructor for a blocking result."""
        return cls(blocking=True, reasons=tuple(reasons))


class GuardianCheck(ABC):
    """
    Abstract base class for a single governance rule.

    Subclass this and implement evaluate() to create a check.
    The check MUST NOT raise — return CheckResult(passed=False) instead.
    """

    @property
    def name(self) -> str:
        """Override to customise the check name. Defaults to class name."""
        return self.__class__.__name__

    @abstractmethod
    def evaluate(self, node: Any, ctx: Any) -> CheckResult:
        """
        Evaluate whether the node is safe to execute in this context.

        Args:
            node: The DAG Node about to be executed.
            ctx:  The ResearchContext for this run.

        Returns:
            CheckResult — NEVER raises.
        """
