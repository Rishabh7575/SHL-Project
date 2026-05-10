import json
import os

INPUT_FILE = "data/cleaned_catalog.json"

def build_vector_database():
    """
    Lightweight version: Validates the JSON catalog instead of building a FAISS index.
    """
    if not os.path.exists(INPUT_FILE):
        print(f"Error: {INPUT_FILE} not found. Run the scraper first.")
        return

    print("Validating dataset for lightweight retrieval...")
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not data:
        print("Dataset empty. Exiting.")
        return

    print(f"Dataset valid! {len(data)} documents found.")
    print("Vector database generation skipped (Using lightweight keyword matching).")

if __name__ == "__main__":
    build_vector_database()
