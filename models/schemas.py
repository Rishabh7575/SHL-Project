from pydantic import BaseModel, Field
from typing import List, Optional, Any, Generic, TypeVar

T = TypeVar("T")

# -------------------------
# Reusable API Response
# -------------------------
class APIResponse(BaseModel, Generic[T]):
    """
    A standard wrapper for all API responses to maintain consistency across the frontend and backend.
    """
    success: bool
    data: Optional[T] = None
    error: Optional[str] = None
    message: str = ""

# -------------------------
# Chat Models
# -------------------------
class Message(BaseModel):
    """
    Represents a single message in the conversation.
    """
    role: str = Field(..., description="Role of the sender: 'user' or 'assistant'")
    content: str = Field(..., min_length=1, description="The actual message text")

class ChatRequest(BaseModel):
    """
    The incoming request for the /chat endpoint.
    Expects a list of messages representing the conversation history.
    """
    messages: List[Message] = Field(..., min_length=1, description="List of conversation messages")

class ChatResponse(BaseModel):
    """
    The outgoing response data structure for the /chat endpoint.
    """
    reply: str
    recommendations: List[str] = []
    end_of_conversation: bool = False
