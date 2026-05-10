from google import genai
from config.settings import settings
from typing import List, Dict, Any
from utils.logger import logger

client = genai.Client(api_key=settings.gemini_api_key) if settings.gemini_api_key else None
MODEL_NAME = 'gemini-2.5-flash' if client else None

if not client:
    logger.warning("GEMINI_API_KEY missing. Using fallback mode.")

def generate_search_query(history: str) -> str:
    if not client:
        return "NO_SEARCH"
        
    prompt = (
        "You're a recruiter AI assistant. Based on this chat history, "
        "write a short search query (max 5 words) to find assessments.\n"
        "If they're just saying hi or want to compare existing results, return 'NO_SEARCH'.\n\n"
        f"--- CHAT HISTORY ---\n{history}\n\nQuery:"
    )
    
    try:
        response = client.models.generate_content(model=MODEL_NAME, contents=prompt)
        return response.text.strip()
    except Exception as e:
        logger.error(f"Search query error: {e}")
        return "NO_SEARCH"

def generate_chat_response(history: str, recs: List[Dict[str, Any]] = None) -> str:
    if not client:
        return "Based on your requirements, here are the top assessments." if recs else "Could you provide more details about the role?"

    instructions = (
        "You're an expert recruiter. Be professional and concise.\n"
        "1. ONLY discuss assessments from the RETRIEVED section or HISTORY.\n"
        "2. Don't output JSON.\n"
    )

    recs_text = "None."
    if recs:
        recs_text = "\n".join([f"{i+1}. {r.get('assessment_name')}: {r.get('description')}" for i, r in enumerate(recs)])

    prompt = (
        f"{instructions}\n\n"
        f"--- HISTORY ---\n{history}\n\n"
        f"--- RETRIEVED ASSESSMENTS ---\n{recs_text}\n\nResponse:"
    )

    try:
        response = client.models.generate_content(model=MODEL_NAME, contents=prompt)
        return response.text.strip()
    except Exception as e:
        logger.error(f"Response error: {e}")
        return "Error generating response. Try again."
