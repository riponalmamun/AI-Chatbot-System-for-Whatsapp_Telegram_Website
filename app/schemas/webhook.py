from pydantic import BaseModel
from typing import Optional, Dict, Any


class WhatsAppWebhook(BaseModel):
    """WhatsApp webhook data schema"""
    Body: str
    From: str
    To: Optional[str] = None
    MessageSid: Optional[str] = None
    AccountSid: Optional[str] = None


class TelegramMessage(BaseModel):
    """Telegram message schema"""
    message_id: int
    text: Optional[str] = None
    chat: Dict[str, Any]
    from_user: Optional[Dict[str, Any]] = None
    
    class Config:
        fields = {'from_user': 'from'}


class TelegramWebhook(BaseModel):
    """Telegram webhook data schema"""
    update_id: int
    message: Optional[TelegramMessage] = None