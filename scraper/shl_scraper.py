import os
import json
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any

# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------
TARGET_URL = "https://www.shl.com/en/assessments/"
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

def extract_assessment_data(card_soup: BeautifulSoup) -> Dict[str, Any]:
    """
    Extracts individual assessment fields from a single HTML 'card'.
    Updated with the actual SHL HTML structure.
    """
    # 1. Assessment Name
    name_elem = card_soup.find("h3", class_="content-card__title")
    name = name_elem.get_text(strip=True) if name_elem else "Unknown Assessment"

    # 2. URL (the card itself is an <a> tag)
    url = card_soup.get("href", "")
    # Ensure it's a full URL
    if url and url.startswith("/"):
        url = "https://www.shl.com" + url

    # 3. Description
    desc_elem = card_soup.find("div", class_="content-card__content")
    description = desc_elem.get_text(strip=True) if desc_elem else "No description available."

    # SHL page combines features in the description, so we search the entire card text
    features_text = card_soup.get_text(strip=True).lower()

    # 4. Remote Testing Support
    remote_testing_support = "remote" in features_text or "online" in features_text or "virtual" in features_text

    # 5. Adaptive Support
    adaptive_support = "adaptive" in features_text

    # 6. Test Types
    # SHL doesn't use standard badges on this page, we infer test type from the name/description
    test_types = []
    if "cognitive" in features_text: test_types.append("Cognitive")
    if "personality" in features_text: test_types.append("Personality")
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
    soup = fetch_html(TARGET_URL)
    if not soup:
        print("Failed to retrieve the webpage. Exiting.")
        return
    
    # 2. Find all assessment cards
    # On SHL, the assessment cards are <a> tags with class 'content-card__full-width-link'
    card_elements = soup.find_all("a", class_="content-card__full-width-link") 
    # Filter to ensure they are assessment links
    card_elements = [c for c in card_elements if "/assessments/" in c.get("href", "")]
    
    if not card_elements:
        print("No assessment cards found. You may need to update the CSS selector in the script.")
        return

    print(f"Found {len(card_elements)} raw assessment cards. Extracting data...")
    
    # 3. Extract data
    assessments = []
    for card in card_elements:
        data = extract_assessment_data(card)
        assessments.append(data)
        
    # 4. Remove duplicates
    unique_assessments = remove_duplicates(assessments)
    print(f"Removed {len(assessments) - len(unique_assessments)} duplicates.")
    
    # 5. Save to structured JSON
    save_to_json(unique_assessments, OUTPUT_FILE)
    print("Scraping completed.")

if __name__ == "__main__":
    main()
