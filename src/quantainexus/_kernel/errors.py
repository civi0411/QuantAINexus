"""
QuantAINexus — _kernel/errors.py

Exception Hierarchy (Article XV of Architectural Constitution v3.0).
ALL exceptions in the system MUST descend from QuantAINexusError.

Ownership:
  - DomainError: raised by domain models (invariant violations).
  - RegistryError: raised by RegistryHub (lookup failures, duplicates).
  - GuardianBlockedError: raised ONLY by LocalRunner (never by Guardian itself).
  - PromotionBlockedError: raised by LifecycleState.promote().
  - AgentBreakerTripped: raised by AgentBreaker circuit breaker.
  - CyclicGraphError: raised by Graph.topological_order().
"""


class QuantAINexusError(Exception):
    """Root exception. All framework errors descend from this."""


# ── Domain errors ────────────────────────────────────────────────────────────

class DomainError(QuantAINexusError):
    """Business-rule violation inside a domain model."""


class InvalidTransitionError(DomainError):
    """Attempted an illegal AssetStage transition."""

    def __init__(self, from_stage: object, to_stage: object) -> None:
        self.from_stage = from_stage
        self.to_stage = to_stage
        super().__init__(
            f"Invalid lifecycle transition: {from_stage!r} → {to_stage!r}"
        )


class InvariantViolationError(DomainError):
    """A domain invariant was broken (e.g., negative quantity)."""


class LeverageExceededError(DomainError):
    """Portfolio leverage exceeded the allowed maximum."""

    def __init__(self, actual: float, maximum: float) -> None:
        self.actual = actual
        self.maximum = maximum
        super().__init__(
            f"Leverage {actual:.4f}x exceeds maximum {maximum:.4f}x"
        )


# ── Registry errors ──────────────────────────────────────────────────────────

class RegistryError(QuantAINexusError):
    """Base for all RegistryHub errors."""


class UnknownComponentError(RegistryError):
    """Requested component name/category does not exist in the registry."""

    def __init__(self, category: object, name: str) -> None:
        self.category = category
        self.name = name
        super().__init__(f"No component '{name}' registered under category {category!r}")


class DuplicateRegistrationError(RegistryError):
    """Attempted to register a name that already exists (without overwrite=True)."""

    def __init__(self, category: object, name: str) -> None:
        self.category = category
        self.name = name
        super().__init__(
            f"Component '{name}' is already registered under category {category!r}"
        )


# ── Execution / Governance errors ─────────────────────────────────────────────

class GuardianBlockedError(QuantAINexusError):
    """
    Raised ONLY by LocalRunner when Guardian returns a blocking HookResult.
    Guardian itself MUST NOT raise — it returns HookResult instead.
    """

    def __init__(self, node: object, reasons: list) -> None:
        self.node = node
        self.reasons = reasons
        formatted = "; ".join(str(r) for r in reasons)
        super().__init__(f"Guardian blocked node {node!r}: {formatted}")


class PromotionBlockedError(QuantAINexusError):
    """Lifecycle promotion was rejected by the Guardian profile check."""

    def __init__(self, report: object) -> None:
        self.report = report
        super().__init__(f"Promotion blocked: {report}")


# ── Agent errors ──────────────────────────────────────────────────────────────

class AgentBreakerTripped(QuantAINexusError):
    """AgentBreaker circuit tripped — halting agent loop."""

    def __init__(self, reason: str) -> None:
        self.reason = reason
        super().__init__(f"AgentBreaker tripped: {reason}")


# ── Graph errors ──────────────────────────────────────────────────────────────

class CyclicGraphError(QuantAINexusError):
    """Detected a cycle during DAG topological sort."""

    def __init__(self, cycle_hint: str = "") -> None:
        self.cycle_hint = cycle_hint
        msg = "DAG contains a cycle"
        if cycle_hint:
            msg += f": {cycle_hint}"
        super().__init__(msg)
