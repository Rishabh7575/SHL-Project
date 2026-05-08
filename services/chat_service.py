from models.schemas import ChatRequest, ChatResponse
from utils.logger import logger

def process_chat(request: ChatRequest) -> ChatResponse:
    """
    Handles the business logic for the chat.
    Currently, this just returns a dummy response as requested, 
    but later it will integrate with our AI models.
    """
    logger.info(f"Processing chat with {len(request.messages)} messages.")
    
    # Return the exact dummy structure requested
    return ChatResponse(
        reply="Backend working",
        recommendations=[],
        end_of_conversation=False
    )
