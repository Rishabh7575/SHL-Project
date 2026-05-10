import json
import os
import re
from typing import List, Dict, Any

METADATA_PATH = "data/cleaned_catalog.json"

class KeywordRetriever:
    def __init__(self):
        self.metadata = []
        self._load_data()

    def _load_data(self):
        if not os.path.exists(METADATA_PATH):
            print(f"Metadata missing at {METADATA_PATH}. Run scraper.")
            return

        with open(METADATA_PATH, "r", encoding="utf-8") as f:
            self.metadata = json.load(f)
            
    def _get_tokens(self, text: str) -> set:
        """Simple tokenizer that lowercases and removes non-alphanumeric chars."""
        return set(re.findall(r'\w+', text.lower()))

    def search(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        if not self.metadata:
            return []

        query_tokens = self._get_tokens(query)
        if not query_tokens:
            return []

        results = []
        for item in self.metadata:
            # Calculate scores
            name_tokens = self._get_tokens(item.get("assessment_name", ""))
            desc_tokens = self._get_tokens(item.get("description", ""))
            
            # Intersection of sets gives us match count
            name_matches = len(query_tokens.intersection(name_tokens))
            desc_matches = len(query_tokens.intersection(desc_tokens))
            
            # Weight name matches more heavily
            score = (name_matches * 3.0) + (desc_matches * 1.0)
            
            if score > 0:
                # Normalize score to a 0-100 range (approximate for similarity feel)
                # max possible matches is query_tokens * weight
                max_score = len(query_tokens) * 3.0
                similarity_score = min(100.0, (score / max_score) * 100.0)
                
                results.append({
                    "assessment_name": item.get("assessment_name", "Unknown"),
                    "similarity_score": round(similarity_score, 2),
                    "url": item.get("url", ""),
                    "description": item.get("description", "")
                })

        # Sort by score descending
        results.sort(key=lambda x: x["similarity_score"], reverse=True)
        
        return results[:top_k]

_retriever = None

def search_catalog(query: str, top_k: int = 3) -> List[Dict[str, Any]]:
    global _retriever
    if _retriever is None:
        _retriever = KeywordRetriever()
    return _retriever.search(query, top_k)
