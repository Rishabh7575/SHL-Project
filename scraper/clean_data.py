import json
import os

INPUT_FILE = "data/shl_catalog.json"
OUTPUT_FILE = "data/cleaned_catalog.json"

def clean_text(text: str) -> str:
    """Fix encoding issues and remove extra whitespace."""
    if not text:
        return ""
    
    text = text.replace("â€™", "'").replace("â€“", "-").replace("â€œ", '"').replace("â€", '"')
    return " ".join(text.split()).strip()

def process_dataset():
    """Clean the raw catalog and save the results."""
    if not os.path.exists(INPUT_FILE):
        print(f"Error: {INPUT_FILE} not found.")
        return

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    results = []
    seen = set()

    for item in raw_data:
        name = clean_text(item.get("assessment_name", ""))
        url = item.get("url", "").strip()
        desc = clean_text(item.get("description", ""))
        types = item.get("test_types", [])

        if not name or not url or name == "Unknown Assessment":
            continue

        if url in seen:
            continue
        seen.add(url)

        types_str = " ".join(types)
        searchable = clean_text(f"{name}. {desc}. Types: {types_str}")

        results.append({
            "assessment_name": name,
            "url": url,
            "description": desc,
            "test_types": types,
            "remote_testing_support": item.get("remote_testing_support", False),
            "adaptive_support": item.get("adaptive_support", False),
            "searchable_text": searchable
        })

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)

    print(f"Saved {len(results)} cleaned items to {OUTPUT_FILE}.")

if __name__ == "__main__":
    process_dataset()
