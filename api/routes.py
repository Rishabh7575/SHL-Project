from fastapi import APIRouter
from models.schemas import ChatRequest, ChatResponse
from core.logger import logger

# Create a router instance for our endpoints
router = APIRouter()

@router.get("/health")
async def health_check():
    """
    Simple endpoint to check if the server is running.
    """
    logger.info("Health check endpoint called")
    return {"status": "ok", "message": "Server is running"}

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Placeholder endpoint for the AI chat logic.
    """
    logger.info(f"Received chat message from user: {request.user_id}")
    
    # TODO: Implement actual AI logic here later
    dummy_reply = f"Hello {request.user_id}, you said: '{request.message}'"
    
    return ChatResponse(
        reply=dummy_reply,
        status="success"
    )
