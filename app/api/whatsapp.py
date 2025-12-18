from fastapi import APIRouter, Form, Depends, Response
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.ai_service import AIService
from app.services.conversation_service import ConversationService
from app.services.whatsapp_service import WhatsAppService
from app.services.knowledge_service import KnowledgeService
from app.utils.logger import logger
from app.utils.helpers import clean_phone_number

router = APIRouter()


@router.post("/webhook")
async def whatsapp_webhook(
    Body: str = Form(...),
    From: str = Form(...),
    To: str = Form(None),
    MessageSid: str = Form(None),
    AccountSid: str = Form(None),
    db: Session = Depends(get_db)
):
    """
    WhatsApp webhook endpoint for receiving messages from Twilio
    
    Twilio sends data as form-encoded, not JSON
    """
    try:
        logger.info(f"Received WhatsApp message from {From}: {Body}")
        
        # Initialize services
        ai_service = AIService()
        conv_service = ConversationService(db)
        whatsapp_service = WhatsAppService()
        knowledge_service = KnowledgeService(db)
        
        # Clean phone number
        user_phone = clean_phone_number(From)
        
        # Get or create user
        user = conv_service.get_or_create_user(
            user_identifier=user_phone,
            platform="whatsapp"
        )
        
        # Get conversation history
        history = conv_service.get_user_history(
            user_identifier=user_phone,
            limit=10
        )
        
        # Search for relevant knowledge
        custom_context = await knowledge_service.search_relevant_knowledge(
            query=Body,
            limit=3
        )
        
        # Generate AI response
        ai_response = await ai_service.generate_response(
            user_message=Body,
            conversation_history=history,
            system_prompt="You are a helpful WhatsApp assistant. Keep responses concise and friendly.",
            custom_context=custom_context if custom_context else None
        )
        
        # Save conversation
        conv_service.save_conversation(
            user_id=user.id,
            user_message=Body,
            ai_response=ai_response,
            platform="whatsapp",
            model_used=ai_service.model
        )
        
        # Create TwiML response
        twiml_response = whatsapp_service.create_response(ai_response)
        
        logger.info(f"WhatsApp response sent to {From}")
        
        return Response(
            content=twiml_response,
            media_type="application/xml"
        )
        
    except Exception as e:
        logger.error(f"Error in WhatsApp webhook: {e}")
        
        # Return error message to user
        whatsapp_service = WhatsAppService()
        error_response = whatsapp_service.create_response(
            "Sorry, I encountered an error. Please try again later."
        )
        
        return Response(
            content=error_response,
            media_type="application/xml"
        )


@router.get("/status")
async def whatsapp_status():
    """
    Check WhatsApp integration status
    """
    try:
        whatsapp_service = WhatsAppService()
        
        if whatsapp_service.client:
            return {
                "status": "active",
                "message": "WhatsApp integration is active",
                "from_number": whatsapp_service.from_number
            }
        else:
            return {
                "status": "inactive",
                "message": "WhatsApp integration is not configured"
            }
            
    except Exception as e:
        logger.error(f"Error checking WhatsApp status: {e}")
        return {
            "status": "error",
            "message": str(e)
        }


@router.post("/send-test")
async def send_test_message(
    to_number: str,
    message: str = "Hello! This is a test message from your AI chatbot."
):
    """
    Send a test WhatsApp message
    
    - **to_number**: Recipient phone number (include country code, e.g., +8801712345678)
    - **message**: Test message to send
    """
    try:
        whatsapp_service = WhatsAppService()
        
        # Add whatsapp: prefix if not present
        if not to_number.startswith("whatsapp:"):
            to_number = f"whatsapp:{to_number}"
        
        success = whatsapp_service.send_message(to_number, message)
        
        if success:
            return {
                "success": True,
                "message": f"Test message sent to {to_number}"
            }
        else:
            return {
                "success": False,
                "message": "Failed to send test message"
            }
            
    except Exception as e:
        logger.error(f"Error sending test message: {e}")
        return {
            "success": False,
            "message": str(e)
        }