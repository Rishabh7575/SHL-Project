from fastapi import APIRouter
from models.schemas import ChatRequest, ChatResponse, APIResponse
from services.chat_service import process_chat
from utils.logger import logger

router = APIRouter()

@router.post("/chat", response_model=APIResponse[ChatResponse])
async def chat_endpoint(request: ChatRequest):
    """
    Receives the chat request, validates it using our Pydantic schema,
    passes it to the service layer for processing, and returns a standardized response.
    """
    logger.info("Received request at /chat endpoint")
    
    # The service layer handles the actual logic
    chat_response_data = process_chat(request)
    
    # Wrap the response in our reusable APIResponse format
    return APIResponse(
        success=True,
        data=chat_response_data,
        message="Chat processed successfully"
    )
