"""
QuantAINexus — _kernel/domain/time.py

Time value objects (Article IV §4.1).

KnowledgeTime: the moment a piece of data became KNOWN to the system.
This is different from EventTime (when the event occurred).
Using KnowledgeTime as the PIT boundary prevents look-ahead bias.

Import policy: ONLY dataclasses, datetime. No heavy dependencies.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass(frozen=True)
class KnowledgeTime:
    """
    Point-in-Time boundary.

    All data fetched in a ResearchContext must have a knowledge_time <= pit_as_of.
    This prevents accidentally using data that was not yet available at the
    time the decision would have been made.
    """
    value: datetime

    def __post_init__(self) -> None:
        if not isinstance(self.value, datetime):
            raise TypeError(f"KnowledgeTime.value must be datetime, got {type(self.value)}")

    @classmethod
    def now(cls) -> "KnowledgeTime":
        """Current UTC time as a KnowledgeTime."""
        return cls(datetime.now(tz=timezone.utc))

    @classmethod
    def of(cls, year: int, month: int, day: int, hour: int = 0,
           minute: int = 0, second: int = 0) -> "KnowledgeTime":
        """Convenience constructor for a UTC datetime."""
        return cls(datetime(year, month, day, hour, minute, second,
                            tzinfo=timezone.utc))

    def __le__(self, other: "KnowledgeTime") -> bool:
        return self.value <= other.value

    def __lt__(self, other: "KnowledgeTime") -> bool:
        return self.value < other.value

    def __ge__(self, other: "KnowledgeTime") -> bool:
        return self.value >= other.value

    def __gt__(self, other: "KnowledgeTime") -> bool:
        return self.value > other.value

    def __str__(self) -> str:
        return self.value.isoformat()
