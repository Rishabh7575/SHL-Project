import os
# Fix for Windows httpx connection forcibly closed error when downloading models
os.environ["HF_HUB_DISABLE_HTTP2"] = "1"

import time
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List

# Define the model globally so it's only loaded once when the module is imported
MODEL_NAME = "all-MiniLM-L6-v2"
model = None

def get_model(max_retries: int = 3) -> SentenceTransformer:
    """
    Lazy-loads the embedding model so we don't hold it in memory until needed.
    Includes robust retry logic to handle temporary network errors or 'httpx' client crashes
    that sometimes happen when downloading from HuggingFace on Windows.
    Once downloaded, the model is automatically cached locally by sentence-transformers.
    """
    global model
    if model is None:
        print(f"Loading sentence-transformer model: {MODEL_NAME}...")
        
        for attempt in range(max_retries):
            try:
                # This automatically downloads the model and caches it locally
                model = SentenceTransformer(MODEL_NAME)
                print("Model loaded successfully!")
                break
            except Exception as e:
                print(f"Attempt {attempt + 1}/{max_retries} failed: {e}")
                if attempt < max_retries - 1:
                    print("Waiting 3 seconds before retrying...")
                    time.sleep(3)
                else:
                    raise RuntimeError(f"Failed to load model '{MODEL_NAME}' after {max_retries} attempts. Please check your internet connection.")
                    
    return model

def generate_embeddings(texts: List[str]) -> np.ndarray:
    """
    Converts a list of strings into a NumPy array of vector embeddings.
    """
    if not texts:
        return np.array([])
        
    embedder = get_model()
    print(f"Generating embeddings for {len(texts)} texts...")
    # Generate embeddings. The output is a numpy array.
    embeddings = embedder.encode(texts, show_progress_bar=True)
    return embeddings

def create_faiss_index(embeddings: np.ndarray) -> faiss.IndexFlatL2:
    """
    Creates a simple FAISS index based on L2 (Euclidean) distance.
    """
    if embeddings.size == 0:
        raise ValueError("Cannot create index with empty embeddings.")
        
    dimension = embeddings.shape[1]
    
    # IndexFlatL2 is simple, exact (no approximation), and perfect for small datasets
    index = faiss.IndexFlatL2(dimension)
    
    print(f"Creating FAISS index with dimension: {dimension}")
    index.add(embeddings)
    print(f"Index created. Total vectors in index: {index.ntotal}")
    
    return index

def save_index(index: faiss.Index, filepath: str):
    """
    Saves the FAISS index to the local filesystem.
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    faiss.write_index(index, filepath)
    print(f"Successfully saved FAISS index to {filepath}")

def load_index(filepath: str) -> faiss.Index:
    """
    Loads a FAISS index from the local filesystem.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"FAISS index not found at {filepath}")
        
    print(f"Loading FAISS index from {filepath}...")
    return faiss.read_index(filepath)
