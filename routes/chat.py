from fastapi import APIRouter
from models.schemas import ChatRequest, ChatResponse, APIResponse
from services.chat_service import process_chat
from utils.logger import logger

router = APIRouter()

@router.post("/chat", response_model=APIResponse[ChatResponse])
async def chat_endpoint(request: ChatRequest):
    logger.info("Handling /chat request")
    
    response_data = process_chat(request)
    
    return APIResponse(
        success=True,
        data=response_data,
        message="Chat processed successfully"
    )
