from sqlalchemy.orm import Session
from typing import List, Dict, Optional
from datetime import datetime
from app.models.user import User, PlatformType
from app.models.conversation import Conversation
from app.utils.logger import logger
from app.utils.helpers import generate_session_id


class ConversationService:
    """Service for managing conversations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_or_create_user(
        self,
        user_identifier: str,
        platform: str,
        name: Optional[str] = None
    ) -> User:
        """Get existing user or create new one"""
        try:
            # Try to find existing user
            user = self.db.query(User).filter(
                User.user_identifier == user_identifier
            ).first()
            
            if user:
                # Update last active
                user.last_active = datetime.utcnow()
                if name and not user.name:
                    user.name = name
                self.db.commit()
                self.db.refresh(user)
                logger.info(f"Found existing user: {user_identifier}")
                return user
            
            # Create new user
            platform_enum = PlatformType(platform)
            new_user = User(
                user_identifier=user_identifier,
                platform=platform_enum,
                name=name
            )
            self.db.add(new_user)
            self.db.commit()
            self.db.refresh(new_user)
            logger.info(f"Created new user: {user_identifier}")
            return new_user
            
        except Exception as e:
            logger.error(f"Error in get_or_create_user: {e}")
            self.db.rollback()
            raise
    
    def save_conversation(
        self,
        user_id: int,
        user_message: str,
        ai_response: str,
        platform: str,
        model_used: Optional[str] = None
    ) -> Conversation:
        """Save conversation to database"""
        try:
            conversation = Conversation(
                user_id=user_id,
                user_message=user_message,
                ai_response=ai_response,
                platform=platform,
                model_used=model_used
            )
            self.db.add(conversation)
            self.db.commit()
            self.db.refresh(conversation)
            logger.info(f"Saved conversation for user {user_id}")
            return conversation
            
        except Exception as e:
            logger.error(f"Error saving conversation: {e}")
            self.db.rollback()
            raise
    
    def get_user_history(
        self,
        user_identifier: str,
        limit: int = 10
    ) -> List[Dict[str, str]]:
        """
        Get user's conversation history
        Returns in format: [{"role": "user", "content": "..."}, ...]
        """
        try:
            # Find user
            user = self.db.query(User).filter(
                User.user_identifier == user_identifier
            ).first()
            
            if not user:
                return []
            
            # Get conversations
            conversations = self.db.query(Conversation).filter(
                Conversation.user_id == user.id
            ).order_by(
                Conversation.timestamp.desc()
            ).limit(limit).all()
            
            # Convert to chat format (reverse to chronological order)
            history = []
            for conv in reversed(conversations):
                history.append({
                    "role": "user",
                    "content": conv.user_message
                })
                history.append({
                    "role": "assistant",
                    "content": conv.ai_response
                })
            
            return history
            
        except Exception as e:
            logger.error(f"Error getting user history: {e}")
            return []
    
    def get_conversation_by_session(
        self,
        session_id: str,
        limit: int = 50
    ) -> List[Conversation]:
        """Get conversations by session ID (for website)"""
        try:
            user = self.db.query(User).filter(
                User.user_identifier == session_id
            ).first()
            
            if not user:
                return []
            
            conversations = self.db.query(Conversation).filter(
                Conversation.user_id == user.id
            ).order_by(
                Conversation.timestamp.asc()
            ).limit(limit).all()
            
            return conversations
            
        except Exception as e:
            logger.error(f"Error getting conversations by session: {e}")
            return []
    
    def delete_user_history(self, user_identifier: str) -> bool:
        """Delete all user's conversation history"""
        try:
            user = self.db.query(User).filter(
                User.user_identifier == user_identifier
            ).first()
            
            if not user:
                return False
            
            # Delete all conversations
            self.db.query(Conversation).filter(
                Conversation.user_id == user.id
            ).delete()
            
            self.db.commit()
            logger.info(f"Deleted history for user: {user_identifier}")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting user history: {e}")
            self.db.rollback()
            return False
    
    def get_user_stats(self, user_identifier: str) -> Dict:
        """Get user statistics"""
        try:
            user = self.db.query(User).filter(
                User.user_identifier == user_identifier
            ).first()
            
            if not user:
                return {}
            
            total_conversations = self.db.query(Conversation).filter(
                Conversation.user_id == user.id
            ).count()
            
            return {
                "user_id": user.id,
                "user_identifier": user.user_identifier,
                "platform": user.platform.value,
                "total_conversations": total_conversations,
                "created_at": user.created_at,
                "last_active": user.last_active
            }
            
        except Exception as e:
            logger.error(f"Error getting user stats: {e}")
            return {}