import httpx
from typing import Dict, Optional
from app.core.config import settings
from app.utils.logger import logger


class TelegramService:
    """Service for Telegram Bot integration"""
    
    def __init__(self):
        self.bot_token = settings.TELEGRAM_BOT_TOKEN
        self.webhook_url = settings.TELEGRAM_WEBHOOK_URL
        self.api_url = f"https://api.telegram.org/bot{self.bot_token}"
        
        if self.bot_token:
            logger.info("Telegram bot initialized")
        else:
            logger.warning("Telegram bot token not found. Telegram disabled.")
    
    async def send_message(self, chat_id: str, text: str) -> bool:
        """
        Send message to Telegram chat
        
        Args:
            chat_id: Telegram chat ID
            text: Message text
        
        Returns:
            True if successful, False otherwise
        """
        if not self.bot_token:
            logger.error("Telegram bot token not configured")
            return False
        
        try:
            url = f"{self.api_url}/sendMessage"
            payload = {
                "chat_id": chat_id,
                "text": text,
                "parse_mode": "Markdown"
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=payload)
                response.raise_for_status()
            
            logger.info(f"Telegram message sent to {chat_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error sending Telegram message: {e}")
            return False
    
    async def set_webhook(self, webhook_url: Optional[str] = None) -> bool:
        """
        Set Telegram webhook URL
        
        Args:
            webhook_url: Webhook URL (uses settings if not provided)
        
        Returns:
            True if successful, False otherwise
        """
        if not self.bot_token:
            logger.error("Telegram bot token not configured")
            return False
        
        url_to_set = webhook_url or self.webhook_url
        
        if not url_to_set:
            logger.error("Webhook URL not provided")
            return False
        
        try:
            url = f"{self.api_url}/setWebhook"
            payload = {"url": url_to_set}
            
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=payload)
                response.raise_for_status()
                result = response.json()
            
            if result.get("ok"):
                logger.info(f"Telegram webhook set: {url_to_set}")
                return True
            else:
                logger.error(f"Failed to set webhook: {result}")
                return False
                
        except Exception as e:
            logger.error(f"Error setting Telegram webhook: {e}")
            return False
    
    async def delete_webhook(self) -> bool:
        """Delete Telegram webhook"""
        if not self.bot_token:
            return False
        
        try:
            url = f"{self.api_url}/deleteWebhook"
            
            async with httpx.AsyncClient() as client:
                response = await client.post(url)
                response.raise_for_status()
            
            logger.info("Telegram webhook deleted")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting webhook: {e}")
            return False
    
    async def get_webhook_info(self) -> Dict:
        """Get current webhook information"""
        if not self.bot_token:
            return {}
        
        try:
            url = f"{self.api_url}/getWebhookInfo"
            
            async with httpx.AsyncClient() as client:
                response = await client.get(url)
                response.raise_for_status()
                result = response.json()
            
            return result.get("result", {})
            
        except Exception as e:
            logger.error(f"Error getting webhook info: {e}")
            return {}
    
    def parse_webhook_data(self, data: Dict) -> Dict:
        """
        Parse incoming webhook data from Telegram
        
        Args:
            data: Webhook data
        
        Returns:
            Parsed data dict
        """
        message = data.get("message", {})
        
        return {
            "message_id": message.get("message_id"),
            "chat_id": str(message.get("chat", {}).get("id", "")),
            "user_id": str(message.get("from", {}).get("id", "")),
            "username": message.get("from", {}).get("username", ""),
            "first_name": message.get("from", {}).get("first_name", ""),
            "text": message.get("text", ""),
            "timestamp": message.get("date")
        }
    
    def get_user_identifier(self, user_id: str, username: Optional[str] = None) -> str:
        """Get user identifier for database"""
        if username:
            return f"telegram_{username}"
        return f"telegram_{user_id}"