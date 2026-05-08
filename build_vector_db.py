import json
import os
from services.embedding_service import generate_embeddings, create_faiss_index, save_index

# Configuration
INPUT_FILE = "data/cleaned_catalog.json"
OUTPUT_FAISS_FILE = "data/shl_catalog.faiss"

def build_vector_database():
    """
    Reads the cleaned catalog, generates embeddings for the searchable text,
    and saves the resulting FAISS index.
    """
    if not os.path.exists(INPUT_FILE):
        print(f"Error: {INPUT_FILE} not found. Please run the cleaning script first.")
        return

    print("Loading cleaned dataset...")
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        catalog_data = json.load(f)

    if not catalog_data:
        print("Dataset is empty. Exiting.")
        return

    # Extract the combined searchable text we created earlier
    texts_to_embed = [item["searchable_text"] for item in catalog_data]
    
    # 1. Generate the embeddings
    embeddings = generate_embeddings(texts_to_embed)
    
    # 2. Create the FAISS Vector Database index
    index = create_faiss_index(embeddings)
    
    # 3. Save the index to disk
    save_index(index, OUTPUT_FAISS_FILE)
    
    print("\nVector database build complete!")
    print(f"Number of documents indexed: {len(catalog_data)}")

if __name__ == "__main__":
    build_vector_database()
