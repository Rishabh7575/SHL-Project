import json
import os
from typing import List, Dict, Any
from services.embedding_service import generate_embeddings, load_index

FAISS_INDEX_PATH = "data/shl_catalog.faiss"
METADATA_PATH = "data/cleaned_catalog.json"

class CatalogRetriever:
    def __init__(self):
        self.index = None
        self.metadata = []
        self._load_data()

    def _load_data(self):
        if not os.path.exists(FAISS_INDEX_PATH) or not os.path.exists(METADATA_PATH):
            print("Database missing. Run scraper and vector builder.")
            return

        self.index = load_index(FAISS_INDEX_PATH)
        with open(METADATA_PATH, "r", encoding="utf-8") as f:
            self.metadata = json.load(f)

    def search(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        if not self.index or not self.metadata:
            return []

        query_embedding = generate_embeddings([query])
        distances, indices = self.index.search(query_embedding, k=top_k)

        results = []
        for rank, idx in enumerate(indices[0]):
            if idx == -1:
                break
                
            match = self.metadata[idx]
            score = max(0.0, 100.0 - float(distances[0][rank]))
            
            results.append({
                "assessment_name": match.get("assessment_name", "Unknown"),
                "similarity_score": round(score, 2),
                "url": match.get("url", ""),
                "description": match.get("description", "")
            })
            
        return results

_retriever = None

def search_catalog(query: str, top_k: int = 3) -> List[Dict[str, Any]]:
    global _retriever
    if _retriever is None:
        _retriever = CatalogRetriever()
    return _retriever.search(query, top_k)
