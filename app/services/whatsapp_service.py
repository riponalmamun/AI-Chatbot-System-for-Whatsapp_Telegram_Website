from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from typing import Dict
from app.core.config import settings
from app.utils.logger import logger


class WhatsAppService:
    """Service for WhatsApp integration via Twilio"""
    
    def __init__(self):
        if settings.TWILIO_ACCOUNT_SID and settings.TWILIO_AUTH_TOKEN:
            self.client = Client(
                settings.TWILIO_ACCOUNT_SID,
                settings.TWILIO_AUTH_TOKEN
            )
            self.from_number = settings.TWILIO_WHATSAPP_NUMBER
            logger.info("Twilio WhatsApp client initialized")
        else:
            self.client = None
            logger.warning("Twilio credentials not found. WhatsApp disabled.")
    
    def send_message(self, to_number: str, message: str) -> bool:
        """
        Send WhatsApp message via Twilio
        
        Args:
            to_number: Recipient's phone number (with whatsapp: prefix)
            message: Message to send
        
        Returns:
            True if successful, False otherwise
        """
        if not self.client:
            logger.error("Twilio client not initialized")
            return False
        
        try:
            # Ensure number has whatsapp: prefix
            if not to_number.startswith("whatsapp:"):
                to_number = f"whatsapp:{to_number}"
            
            message = self.client.messages.create(
                from_=self.from_number,
                body=message,
                to=to_number
            )
            
            logger.info(f"WhatsApp message sent: {message.sid}")
            return True
            
        except Exception as e:
            logger.error(f"Error sending WhatsApp message: {e}")
            return False
    
    def create_response(self, message: str) -> str:
        """
        Create TwiML response for webhook
        
        Args:
            message: Response message
        
        Returns:
            TwiML XML string
        """
        response = MessagingResponse()
        response.message(message)
        return str(response)
    
    def parse_webhook_data(self, form_data: Dict) -> Dict:
        """
        Parse incoming webhook data from Twilio
        
        Args:
            form_data: Form data from webhook
        
        Returns:
            Parsed data dict
        """
        return {
            "message": form_data.get("Body", ""),
            "from": form_data.get("From", ""),
            "to": form_data.get("To", ""),
            "message_sid": form_data.get("MessageSid", ""),
            "account_sid": form_data.get("AccountSid", "")
        }
    
    def get_user_identifier(self, phone_number: str) -> str:
        """
        Get clean user identifier from phone number
        Removes 'whatsapp:' prefix
        """
        return phone_number.replace("whatsapp:", "").strip()