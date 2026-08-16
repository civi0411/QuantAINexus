"""
QuantAINexus — agents/a2a/card.py
Agent capabilities card.
"""
from typing import List, Dict

class AgentCard:
    def __init__(self, agent_id: str, capabilities: List[str], endpoint: str):
        self.agent_id = agent_id
        self.capabilities = capabilities
        self.endpoint = endpoint
