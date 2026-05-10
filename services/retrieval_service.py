import json
import os
import numpy as np
from typing import List, Dict, Any
from services.embedding_service import generate_embeddings, load_index

# Configuration paths
FAISS_INDEX_PATH = "data/shl_catalog.faiss"
METADATA_PATH = "data/cleaned_catalog.json"

class CatalogRetriever:
    """
    A simple class to handle loading the database once and running searches.
    """
    def __init__(self):
        self.index = None
        self.metadata = []
        self._load_data()

    def _load_data(self):
        """
        Loads the FAISS index and the JSON metadata into memory.
        """
        if not os.path.exists(FAISS_INDEX_PATH):
            raise FileNotFoundError(f"FAISS index missing at {FAISS_INDEX_PATH}. Run build_vector_db.py first.")
        if not os.path.exists(METADATA_PATH):
            raise FileNotFoundError(f"Metadata missing at {METADATA_PATH}. Run data cleaning script first.")

        print("Loading FAISS index...")
        self.index = load_index(FAISS_INDEX_PATH)
        
        print("Loading catalog metadata...")
        with open(METADATA_PATH, "r", encoding="utf-8") as f:
            self.metadata = json.load(f)
            
        # Quick validation
        if self.index.ntotal != len(self.metadata):
            print(f"Warning: Index size ({self.index.ntotal}) doesn't match metadata size ({len(self.metadata)})")

    def search(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Takes a natural language query, converts it to a vector, and finds the closest matches in the database.
        Returns a list of dictionaries containing the assessment details and similarity scores.
        """
        if not self.index or not self.metadata:
            print("Error: Database not loaded.")
            return []

        # 1. Convert the user's text query into a vector embedding
        # We put it in a list because the function expects a list of texts
        query_embedding = generate_embeddings([query])

        # 2. Search the FAISS index
        # D contains the distances (lower is better for L2 distance)
        # I contains the indexes of the matching items in our metadata array
        distances, indices = self.index.search(query_embedding, k=top_k)

        # 3. Format the results
        results = []
        for rank, metadata_idx in enumerate(indices[0]):
            # If we don't have enough data, FAISS returns -1
            if metadata_idx == -1:
                break
                
            match = self.metadata[metadata_idx]
            # Convert L2 distance to a simple "similarity score" (smaller distance = higher score)
            # We invert it simply for human readability
            raw_distance = float(distances[0][rank])
            similarity_score = max(0.0, 100.0 - raw_distance)
            
            results.append({
                "assessment_name": match.get("assessment_name", "Unknown"),
                "similarity_score": round(similarity_score, 2),
                "url": match.get("url", ""),
                "description": match.get("description", "")
            })
            
        return results

# Expose a simple function for ease of use
_retriever_instance = None

def search_catalog(query: str, top_k: int = 3) -> List[Dict[str, Any]]:
    """
    Helper function that lazy-loads the retriever and runs a search.
    """
    global _retriever_instance
    if _retriever_instance is None:
        _retriever_instance = CatalogRetriever()
        
    return _retriever_instance.search(query, top_k)
