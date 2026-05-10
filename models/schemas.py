from pydantic import BaseModel, Field
from typing import List, Optional, Any, Generic, TypeVar, Dict

T = TypeVar("T")

class APIResponse(BaseModel, Generic[T]):
    success: bool
    data: Optional[T] = None
    error: Optional[str] = None
    message: str = ""

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]

class ChatResponse(BaseModel):
    reply: str
    recommendations: List[Dict[str, Any]] = []
    end_of_conversation: bool = False
