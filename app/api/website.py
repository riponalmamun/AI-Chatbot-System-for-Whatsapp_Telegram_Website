from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.chat import (
    ChatRequest,
    ChatResponse,
    ConversationHistoryResponse,
    ConversationHistoryItem
)
from app.services.ai_service import AIService
from app.services.conversation_service import ConversationService
from app.services.knowledge_service import KnowledgeService
from app.utils.helpers import generate_session_id
from app.utils.logger import logger
from datetime import datetime

router = APIRouter()


@router.post("/send", response_model=ChatResponse)
async def send_message(
    request: ChatRequest,
    db: Session = Depends(get_db)
):
    """
    Handle website chat messages
    
    - **message**: User's message
    - **session_id**: Optional session ID (will be generated if not provided)
    - **user_name**: Optional user name
    """
    try:
        # Generate or use provided session_id
        session_id = request.session_id or generate_session_id()
        
        # Initialize services
        ai_service = AIService()
        conv_service = ConversationService(db)
        knowledge_service = KnowledgeService(db)
        
        # Get or create user
        user = conv_service.get_or_create_user(
            user_identifier=session_id,
            platform="website",
            name=request.user_name
        )
        
        # Get conversation history
        history = conv_service.get_user_history(
            user_identifier=session_id,
            limit=10
        )
        
        # Search for relevant knowledge (RAG)
        custom_context = await knowledge_service.search_relevant_knowledge(
            query=request.message,
            limit=3
        )
        
        # Generate AI response
        ai_response = await ai_service.generate_response(
            user_message=request.message,
            conversation_history=history,
            system_prompt="You are a helpful AI assistant for a website chatbot. Be friendly and concise.",
            custom_context=custom_context if custom_context else None
        )
        
        # Save conversation
        conv_service.save_conversation(
            user_id=user.id,
            user_message=request.message,
            ai_response=ai_response,
            platform="website",
            model_used=ai_service.model
        )
        
        logger.info(f"Website chat processed for session: {session_id}")
        
        return ChatResponse(
            message=ai_response,
            session_id=session_id,
            timestamp=datetime.utcnow()
        )
        
    except Exception as e:
        logger.error(f"Error in send_message: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process message"
        )


@router.get("/history/{session_id}", response_model=ConversationHistoryResponse)
async def get_chat_history(
    session_id: str,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """
    Get chat history for a session
    
    - **session_id**: Session identifier
    - **limit**: Maximum number of messages to return (default: 50)
    """
    try:
        conv_service = ConversationService(db)
        
        # Get conversations
        conversations = conv_service.get_conversation_by_session(
            session_id=session_id,
            limit=limit
        )
        
        # Convert to response format
        history_items = []
        for conv in conversations:
            # Add user message
            history_items.append(
                ConversationHistoryItem(
                    role="user",
                    content=conv.user_message,
                    timestamp=conv.timestamp
                )
            )
            # Add AI response
            history_items.append(
                ConversationHistoryItem(
                    role="assistant",
                    content=conv.ai_response,
                    timestamp=conv.timestamp
                )
            )
        
        return ConversationHistoryResponse(
            session_id=session_id,
            conversations=history_items,
            total=len(history_items)
        )
        
    except Exception as e:
        logger.error(f"Error getting chat history: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get chat history"
        )


@router.delete("/history/{session_id}")
async def delete_chat_history(
    session_id: str,
    db: Session = Depends(get_db)
):
    """
    Delete chat history for a session
    
    - **session_id**: Session identifier
    """
    try:
        conv_service = ConversationService(db)
        
        success = conv_service.delete_user_history(
            user_identifier=session_id
        )
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found"
            )
        
        return {"message": "Chat history deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting chat history: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete chat history"
        )


@router.get("/stats/{session_id}")
async def get_session_stats(
    session_id: str,
    db: Session = Depends(get_db)
):
    """
    Get statistics for a session
    
    - **session_id**: Session identifier
    """
    try:
        conv_service = ConversationService(db)
        
        stats = conv_service.get_user_stats(
            user_identifier=session_id
        )
        
        if not stats:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found"
            )
        
        return stats
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting session stats: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get session stats"
        )