import json
import os
import re

# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------
INPUT_FILE = "data/shl_catalog.json"
OUTPUT_FILE = "data/cleaned_catalog.json"

def clean_text(text: str) -> str:
    """
    Cleans excessive whitespace and fixes common encoding artifacts.
    """
    if not text:
        return ""
    
    # Fix common encoding artifacts from web scraping (e.g., "candidateâ€™s" -> "candidate's")
    text = text.replace("â€™", "'").replace("â€“", "-").replace("â€œ", '"').replace("â€", '"')
    
    # Remove excessive whitespace, newlines, and tabs
    text = " ".join(text.split())
    return text.strip()

def process_dataset():
    """
    Reads the raw catalog, cleans it according to requirements, and saves it.
    """
    if not os.path.exists(INPUT_FILE):
        print(f"Error: {INPUT_FILE} not found. Please run the scraper first.")
        return

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    cleaned_data = []
    seen_urls = set()

    for item in raw_data:
        # Extract fields
        name = clean_text(item.get("assessment_name", ""))
        url = item.get("url", "").strip()
        description = clean_text(item.get("description", ""))
        test_types = item.get("test_types", [])
        remote_support = item.get("remote_testing_support", False)
        adaptive_support = item.get("adaptive_support", False)

        # 1. Remove empty/null entries (must have name and url)
        if not name or not url or name == "Unknown Assessment":
            continue

        # 2. Remove duplicates
        if url in seen_urls:
            continue
        seen_urls.add(url)

        # 3. Create searchable combined text field
        # Combine all textual information into one string to make AI embedding or basic search easy
        types_str = " ".join(test_types)
        searchable_text = clean_text(f"{name}. {description}. Types: {types_str}")

        # Assemble the clean item
        clean_item = {
            "assessment_name": name,
            "url": url,
            "description": description,
            "test_types": test_types,
            "remote_testing_support": remote_support,
            "adaptive_support": adaptive_support,
            "searchable_text": searchable_text
        }

        cleaned_data.append(clean_item)

    # Save the cleaned dataset
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(cleaned_data, f, indent=4, ensure_ascii=False)

    print(f"Cleaned dataset saved to {OUTPUT_FILE}.")
    print(f"Original entries: {len(raw_data)}")
    print(f"Cleaned entries: {len(cleaned_data)}")

if __name__ == "__main__":
    print("Starting dataset cleaning...")
    process_dataset()
