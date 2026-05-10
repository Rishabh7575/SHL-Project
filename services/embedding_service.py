import os
from typing import List

# NOTE: This service has been refactored for lightweight deployment.
# Semantic embeddings and FAISS have been replaced by keyword matching 
# to stay within memory limits on free-tier hosting (like Render).

def generate_embeddings(texts: List[str]):
    """
    STUB: No longer generates real embeddings to save RAM.
    Returns a dummy list to avoid breaking legacy code.
    """
    print("Warning: generate_embeddings called in lightweight mode. Returning empty.")
    return []

def create_faiss_index(embeddings):
    """STUB: No longer creates FAISS index."""
    print("Warning: create_faiss_index called in lightweight mode.")
    return None

def save_index(index, filepath: str):
    """STUB: No longer saves FAISS index."""
    print(f"Warning: save_index called for {filepath}. Skipping.")

def load_index(filepath: str):
    """
    STUB: No longer loads FAISS index.
    Returns None to indicate no index is available.
    """
    print(f"Warning: load_index called for {filepath}. Returning None.")
    return None
