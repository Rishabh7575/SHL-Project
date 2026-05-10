import os
import json
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.shl.com/products/product-catalog/"
OUTPUT_FILE = "data/shl_catalog.json"
HEADERS = {"User-Agent": "Mozilla/5.0"}

def fetch_html(url: str):
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        res.raise_for_status()
        return BeautifulSoup(res.text, "html.parser")
    except Exception as e:
        print(f"Fetch error: {e}")
        return None

def extract_data(row: BeautifulSoup):
    link = row.find("a")
    name = link.get_text(strip=True) if link else "Unknown Assessment"
    
    url = link.get("href", "") if link else ""
    if url.startswith("/"):
        url = "https://www.shl.com" + url

    text = row.get_text(strip=True).lower()
    types = []
    
    if "c" in text.split(): types.append("Cognitive")
    if "p" in text.split(): types.append("Personality")
    if "behavior" in text: types.append("Behavioral")
    if "skill" in text: types.append("Skills")
    if not types: types.append("General Assessment")

    return {
        "assessment_name": name,
        "url": url,
        "description": "Description available on details page.",
        "remote_testing_support": "remote" in text or "online" in text or "virtual" in text,
        "adaptive_support": "adaptive" in text,
        "test_types": types
    }

def main():
    soup = fetch_html(BASE_URL)
    if not soup: return
    
    rows = [r for r in soup.find_all("tr") if r.find("a") and ("/view/" in r.find("a").get("href", "") or "/products/" in r.find("a").get("href", ""))]
    
    seen = set()
    results = []
    
    for row in rows:
        data = extract_data(row)
        if data["url"] not in seen:
            results.append(data)
            if data["url"]: seen.add(data["url"])
            
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)
        
    print(f"Saved {len(results)} assessments to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
