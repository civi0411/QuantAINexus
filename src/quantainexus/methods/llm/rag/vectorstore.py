"""
QuantAINexus — methods/llm/rag/vectorstore.py
Vector database interface.
"""
from typing import List, Dict, Any
from .. import LLM

@LLM.register_module(force=True)
class VectorStore:
    def add(self, embeddings: Any, metadata: List[Dict]):
        pass
        
    def search(self, query_embedding: Any, top_k: int = 5) -> List[Dict]:
        return []
