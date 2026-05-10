import json
import os
from services.embedding_service import generate_embeddings, create_faiss_index, save_index

INPUT_FILE = "data/cleaned_catalog.json"
OUTPUT_FAISS_FILE = "data/shl_catalog.faiss"

def build_vector_database():
    """Build and save the FAISS vector database from the cleaned catalog."""
    if not os.path.exists(INPUT_FILE):
        print(f"Error: {INPUT_FILE} not found. Run the cleaning script first.")
        return

    print("Loading dataset...")
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not data:
        print("Dataset empty. Exiting.")
        return

    texts = [item["searchable_text"] for item in data]
    
    embeddings = generate_embeddings(texts)
    index = create_faiss_index(embeddings)
    save_index(index, OUTPUT_FAISS_FILE)
    
    print("\nVector database built!")
    print(f"Indexed {len(data)} documents.")

if __name__ == "__main__":
    build_vector_database()
