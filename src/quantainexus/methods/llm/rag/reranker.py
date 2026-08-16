"""
QuantAINexus — methods/llm/rag/reranker.py
Document reranking.
"""
from typing import List, Dict, Any
from .. import LLM

@LLM.register_module(force=True)
class CrossEncoderReranker:
    def rerank(self, query: str, documents: List[Dict]) -> List[Dict]:
        return documents
