"""
production/collaboration/feedback.py — Feedback Loop for continuous improvement.
"""
from typing import Dict, Any, List
from datetime import datetime
from dataclasses import dataclass, field

@dataclass
class Feedback:
    strategy_id: str
    user: str
    message: str
    metrics: Dict[str, Any]
    timestamp: datetime = field(default_factory=datetime.now)

class FeedbackLoop:
    _store: List[Feedback] = []

    @classmethod
    def submit_feedback(cls, strategy_id: str, user: str, message: str, metrics: Dict[str, Any]) -> None:
        feedback = Feedback(
            strategy_id=strategy_id,
            user=user,
            message=message,
            metrics=metrics
        )
        cls._store.append(feedback)
        cls._notify_author(strategy_id, feedback)

    @classmethod
    def get_feedback_for_strategy(cls, strategy_id: str) -> List[Feedback]:
        return [f for f in cls._store if f.strategy_id == strategy_id]

    @classmethod
    def _notify_author(cls, strategy_id: str, feedback: Feedback) -> None:
        # Dummy notification logic
        print(f"🔔 Notification sent to author of {strategy_id}: Feedback received from {feedback.user}")
