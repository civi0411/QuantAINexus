"""
QuantAINexus — agents/a2a/task.py
Agent task lifecycle.
"""
from typing import Dict, Any

class A2ATask:
    def __init__(self, task_id: str, description: str):
        self.task_id = task_id
        self.description = description
        self.status = "submitted" # submitted -> working -> done
        self.messages = []
        
    def update_status(self, new_status: str):
        self.status = new_status
