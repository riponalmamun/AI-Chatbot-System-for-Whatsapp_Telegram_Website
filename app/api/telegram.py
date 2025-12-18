from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.ai_service import AIService
from app.services.conversation_service import ConversationService
from app.services.telegram_service import TelegramService
from app.services.knowledge_service import KnowledgeService
from app.utils.logger import logger

router = APIRouter()


@router.post("/webhook")
async def telegram_webhook(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Telegram webhook endpoint for receiving messages
    
    Telegram sends data as JSON
    """
    try:
        # Get JSON data
        data = await request.json()
        logger.info(f"Received Telegram webhook: {data}")
        
        # Check if it's a message update
        if "message" not in data:
            return {"ok": True}
        
        # Initialize services
        ai_service = AIService()
        conv_service = ConversationService(db)
        telegram_service = TelegramService()
        knowledge_service = KnowledgeService(db)
        
        # Parse webhook data
        parsed_data = telegram_service.parse_webhook_data(data)
        
        chat_id = parsed_data["chat_id"]
        user_text = parsed_data["text"]
        username = parsed_data["username"]
        user_id = parsed_data["user_id"]
        
        # Handle empty message
        if not user_text:
            return {"ok": True}
        
        # Get user identifier
        user_identifier = telegram_service.get_user_identifier(user_id, username)
        
        # Get or create user
        user = conv_service.get_or_create_user(
            user_identifier=user_identifier,
            platform="telegram",
            name=parsed_data["first_name"]
        )
        
        # Get conversation history
        history = conv_service.get_user_history(
            user_identifier=user_identifier,
            limit=10
        )
        
        # Search for relevant knowledge
        custom_context = await knowledge_service.search_relevant_knowledge(
            query=user_text,
            limit=3
        )
        
        # Generate AI response
        ai_response = await ai_service.generate_response(
            user_message=user_text,
            conversation_history=history,
            system_prompt="You are a helpful Telegram bot assistant. Be friendly and use emojis when appropriate.",
            custom_context=custom_context if custom_context else None
        )
        
        # Save conversation
        conv_service.save_conversation(
            user_id=user.id,
            user_message=user_text,
            ai_response=ai_response,
            platform="telegram",
            model_used=ai_service.model
        )
        
        # Send response back to Telegram
        await telegram_service.send_message(chat_id, ai_response)
        
        logger.info(f"Telegram response sent to chat_id: {chat_id}")
        
        return {"ok": True}
        
    except Exception as e:
        logger.error(f"Error in Telegram webhook: {e}")
        return {"ok": False, "error": str(e)}


@router.get("/setup")
async def setup_telegram_webhook():
    """
    Setup Telegram webhook (one-time setup)
    
    Call this endpoint once to register your webhook URL with Telegram
    """
    try:
        telegram_service = TelegramService()
        
        success = await telegram_service.set_webhook()
        
        if success:
            return {
                "success": True,
                "message": "Telegram webhook setup successfully",
                "webhook_url": telegram_service.webhook_url
            }
        else:
            raise HTTPException(
                status_code=500,
                detail="Failed to setup Telegram webhook"
            )
            
    except Exception as e:
        logger.error(f"Error setting up Telegram webhook: {e}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@router.get("/webhook-info")
async def get_webhook_info():
    """
    Get current Telegram webhook information
    """
    try:
        telegram_service = TelegramService()
        
        info = await telegram_service.get_webhook_info()
        
        return {
            "success": True,
            "webhook_info": info
        }
        
    except Exception as e:
        logger.error(f"Error getting webhook info: {e}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@router.delete("/webhook")
async def delete_telegram_webhook():
    """
    Delete Telegram webhook
    """
    try:
        telegram_service = TelegramService()
        
        success = await telegram_service.delete_webhook()
        
        if success:
            return {
                "success": True,
                "message": "Telegram webhook deleted successfully"
            }
        else:
            raise HTTPException(
                status_code=500,
                detail="Failed to delete Telegram webhook"
            )
            
    except Exception as e:
        logger.error(f"Error deleting webhook: {e}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@router.post("/send-test")
async def send_test_telegram_message(
    chat_id: str,
    message: str = "Hello! This is a test message from your AI chatbot."
):
    """
    Send a test Telegram message
    
    - **chat_id**: Telegram chat ID
    - **message**: Test message to send
    """
    try:
        telegram_service = TelegramService()
        
        success = await telegram_service.send_message(chat_id, message)
        
        if success:
            return {
                "success": True,
                "message": f"Test message sent to chat_id: {chat_id}"
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


@router.get("/status")
async def telegram_status():
    """
    Check Telegram integration status
    """
    try:
        telegram_service = TelegramService()
        
        if telegram_service.bot_token:
            webhook_info = await telegram_service.get_webhook_info()
            
            return {
                "status": "active",
                "message": "Telegram integration is active",
                "webhook_set": bool(webhook_info.get("url")),
                "webhook_url": webhook_info.get("url", "Not set")
            }
        else:
            return {
                "status": "inactive",
                "message": "Telegram integration is not configured"
            }
            
    except Exception as e:
        logger.error(f"Error checking Telegram status: {e}")
        return {
            "status": "error",
            "message": str(e)
        }