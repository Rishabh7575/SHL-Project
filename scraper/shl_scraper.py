import os
import json
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any

# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------
BASE_URL = "https://www.shl.com/products/product-catalog/"
OUTPUT_FILE = "data/shl_catalog.json"

# We use headers so the server doesn't block us for looking like a standard bot
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# ---------------------------------------------------------
# Core Functions
# ---------------------------------------------------------

def fetch_html(url: str) -> BeautifulSoup | None:
    """
    Fetches the HTML content of the given URL.
    Returns a BeautifulSoup object, or None if the request fails.
    """
    try:
        print(f"Fetching URL: {url}")
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()  # Raises an error for bad HTTP status codes (e.g., 404, 500)
        return BeautifulSoup(response.text, "html.parser")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return None

def extract_assessment_data(row_soup: BeautifulSoup) -> Dict[str, Any]:
    """
    Extracts individual assessment fields from a single HTML table row.
    """
    link_elem = row_soup.find("a")
    
    # 1. Assessment Name
    name = link_elem.get_text(strip=True) if link_elem else "Unknown Assessment"

    # 2. URL
    url = link_elem.get("href", "") if link_elem else ""
    if url and url.startswith("/"):
        url = "https://www.shl.com" + url

    # 3. Description
    # The table view does not contain descriptions, so we add a placeholder.
    description = "Description available on details page."

    # SHL page combines features in the table columns
    features_text = row_soup.get_text(strip=True).lower()

    # 4. Remote Testing Support
    remote_testing_support = "remote" in features_text or "online" in features_text or "virtual" in features_text

    # 5. Adaptive Support
    adaptive_support = "adaptive" in features_text

    # 6. Test Types
    # SHL uses keys like C, P, A, B in the table columns
    test_types = []
    if "c" in features_text.split(): test_types.append("Cognitive")
    if "p" in features_text.split(): test_types.append("Personality")
    if "behavior" in features_text: test_types.append("Behavioral")
    if "skill" in features_text: test_types.append("Skills")
    
    # Fallback if empty
    if not test_types:
        test_types.append("General Assessment")

    return {
        "assessment_name": name,
        "url": url,
        "description": description,
        "remote_testing_support": remote_testing_support,
        "adaptive_support": adaptive_support,
        "test_types": test_types
    }

def remove_duplicates(assessments: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Removes duplicate assessments by keeping track of seen URLs.
    """
    seen_urls = set()
    unique_assessments = []
    
    for assessment in assessments:
        url = assessment.get("url")
        if url not in seen_urls:
            unique_assessments.append(assessment)
            if url: # Only add to seen if url actually exists
                seen_urls.add(url)
                
    return unique_assessments

def save_to_json(data: List[Dict[str, Any]], filepath: str):
    """
    Saves the extracted data to a JSON file.
    Automatically creates the necessary directories if they don't exist.
    """
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"Successfully saved {len(data)} assessments to {filepath}")
    except IOError as e:
        print(f"Error saving file: {e}")

# ---------------------------------------------------------
# Main Execution
# ---------------------------------------------------------

def main():
    print("Starting SHL Scraper...")
    
    # 1. Fetch the page
    soup = fetch_html(BASE_URL)
    if not soup:
        print("Failed to retrieve the webpage. Exiting.")
        return
    
    # 2. Find all assessment cards
    # On SHL Product Catalog, assessments are stored in a table row <tr> with product links
    rows = soup.find_all("tr")
    
    # Filter to ensure they contain actual assessment links (exclude headers)
    card_elements = []
    for row in rows:
        link = row.find("a")
        if link and ("/view/" in link.get("href", "") or "/products/" in link.get("href", "")):
            card_elements.append(row)
    
    if not card_elements:
        print("No assessment cards found. You may need to update the CSS selector in the script.")
        return

    print(f"DEBUG: Found {len(card_elements)} matching cards (table rows).")
    
    # 3. Extract data
    assessments = []
    for i, card in enumerate(card_elements):
        data = extract_assessment_data(card)
        assessments.append(data)
        
        # Temporary debugging prints for sample titles
        if i < 3:
            print(f"DEBUG: Sample extracted title: '{data['assessment_name']}'")
        
    # 4. Remove duplicates
    unique_assessments = remove_duplicates(assessments)
    print(f"Removed {len(assessments) - len(unique_assessments)} duplicates.")
    
    # 5. Save to structured JSON
    save_to_json(unique_assessments, OUTPUT_FILE)
    print("Scraping completed.")

if __name__ == "__main__":
    main()
