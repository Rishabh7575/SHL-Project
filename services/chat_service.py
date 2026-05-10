from models.schemas import ChatRequest, ChatResponse
from utils.logger import logger
from services.retrieval_service import search_catalog
from services.gemini_service import generate_chat_response, generate_search_query

def process_chat(request: ChatRequest) -> ChatResponse:
    """Process the chat request and return a response with optional recommendations."""
    logger.info(f"Processing chat with {len(request.messages)} messages.")
    
    history = "\n".join([f"{msg.role.capitalize()}: {msg.content.strip()}" for msg in request.messages])
    recs = []
    
    query = generate_search_query(history)
    logger.info(f"Search query: '{query}'")
    
    raw_recs = []
    
    if query != "NO_SEARCH" and len(query) >= 3:
        logger.info("Running semantic search...")
        try:
            raw_recs = search_catalog(query, top_k=3)
            
            for r in raw_recs:
                recs.append({
                    "assessment_name": r["assessment_name"],
                    "url": r["url"],
                    "reason": f"Matching score: {r['similarity_score']:.1f}/100"
                })
        except Exception as e:
            logger.error(f"Search error: {e}")
    else:
        logger.info("Skipping search.")

    try:
        reply = generate_chat_response(history, retrieved_assessments=raw_recs)
    except Exception as e:
        logger.error(f"Generation error: {e}")
        reply = "I ran into an error. Please try again later."
    
    return ChatResponse(
        reply=reply,
        recommendations=recs,
        end_of_conversation=False
    )
