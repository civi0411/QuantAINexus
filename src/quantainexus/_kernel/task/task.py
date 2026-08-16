from dataclasses import dataclass, field
from typing import Any, Dict, List
from .types import TaskType
from ..domain.context import ResearchContext

@dataclass
class Task:
    """
    Task = mục đích + graph + context + validation profile.
    Đây là unit of work chuẩn trong QNX.
    """
    id: str
    task_type: TaskType
    graph: Any                      # DAG của pipeline (sẽ type là Graph sau khi implement DAG)
    context: ResearchContext           # PIT, seed, determinism
    guardian_profile: str              # "lab" | "experimentation" | "production"
    config: Dict[str, Any] = field(default_factory=dict) # Full config dict (Hydra-style)
    
    def validate(self) -> List[Any]:
        """Validate task configuration before execution."""
        return []
