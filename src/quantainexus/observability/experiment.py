"""
QuantAINexus — observability/experiment.py
Experiment tracker (similar to MLflow/WandB).
"""
from typing import Dict, Any
from . import OBSERVABILITY

@OBSERVABILITY.register_module(force=True)
class ExperimentTracker:
    def log_metric(self, name: str, value: float, step: int = None):
        pass
        
    def log_param(self, name: str, value: Any):
        pass
        
    def log_artifact(self, path: str):
        pass
