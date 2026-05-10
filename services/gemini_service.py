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
        "write a short search query (max 5 words) to find relevant SHL assessments.\n"
        "Produce a search query if the user mentions a role, skill, or asks for recommendations.\n"
        "Return 'NO_SEARCH' only if they are just greeting you, saying thanks, or comparing items already in the chat.\n\n"
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
        "You are a professional technical recruiter assistant. Your goal is to help find the best SHL assessments.\n\n"
        "RULES:\n"
        "1. If assessments are provided in the RETRIEVED section, recommend the best matches naturally. Explain briefly why they fit.\n"
        "2. If the RETRIEVED section is empty or no good matches exist, do NOT mention 'retrieval', 'database', or 'history'. "
        "Instead, ask a smart follow-up question to understand the role better (e.g., seniority, specific skills, or team context).\n"
        "3. Maintain a helpful, recruiter-friendly tone. Avoid technical or robotic internal language.\n"
        "4. Never hallucinate assessment names. Only use what is provided or discussed.\n"
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
