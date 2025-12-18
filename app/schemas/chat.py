from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class ChatRequest(BaseModel):
    """Chat request schema"""
    message: str = Field(..., min_length=1, max_length=4000)
    session_id: Optional[str] = None
    user_name: Optional[str] = None


class ChatResponse(BaseModel):
    """Chat response schema"""
    message: str
    session_id: str
    timestamp: datetime
    
    class Config:
        from_attributes = True


class ConversationHistoryItem(BaseModel):
    """Single conversation item"""
    role: str  # "user" or "assistant"
    content: str
    timestamp: datetime
    
    class Config:
        from_attributes = True


class ConversationHistoryResponse(BaseModel):
    """Conversation history response"""
    session_id: str
    conversations: List[ConversationHistoryItem]
    total: int