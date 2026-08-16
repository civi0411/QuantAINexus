from typing import Protocol, Any, List

class Agent(Protocol):
    """
    Agent = stateful entity with memory + tool-calling + state transitions.
    """
    def perceive(self, state: Any) -> Any:
        ...
        
    def act(self, observation: Any) -> Any:
        ...
        
    def reflect(self, result: Any) -> None:
        ...
        
    @property
    def memory(self) -> Any:
        ...
        
    @property
    def tools(self) -> List[Any]:
        ...
