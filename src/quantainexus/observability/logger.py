"""
QuantAINexus — observability/logger.py
Logging utilities.
"""
import logging
from typing import Optional

def get_logger(name: str, level: Optional[int] = None) -> logging.Logger:
    logger = logging.getLogger(name)
    if level is not None:
        logger.setLevel(level)
    return logger
