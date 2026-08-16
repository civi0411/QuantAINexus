"""
QuantAINexus — agents/mcp/tools.py
MCP Tool definitions.
"""
from typing import Dict, Any

class ToolDef:
    def __init__(self, name: str, description: str, input_schema: Dict):
        self.name = name
        self.description = description
        self.input_schema = input_schema
