from sqlalchemy.orm import Session
from typing import List, Optional
import json
from app.models.knowledge_base import KnowledgeBase
from app.services.ai_service import AIService
from app.utils.logger import logger


class KnowledgeService:
    """Service for managing knowledge base (RAG)"""
    
    def __init__(self, db: Session):
        self.db = db
        self.ai_service = AIService()
    
    async def add_knowledge(
        self,
        title: str,
        content: str,
        category: Optional[str] = None
    ) -> KnowledgeBase:
        """
        Add new knowledge to database with embedding
        
        Args:
            title: Knowledge title
            content: Knowledge content
            category: Optional category
        
        Returns:
            Created KnowledgeBase object
        """
        try:
            # Generate embedding
            embedding = await self.ai_service.get_embedding(content)
            embedding_json = json.dumps(embedding) if embedding else None
            
            # Create knowledge entry
            knowledge = KnowledgeBase(
                title=title,
                content=content,
                category=category,
                embedding=embedding_json
            )
            
            self.db.add(knowledge)
            self.db.commit()
            self.db.refresh(knowledge)
            
            logger.info(f"Added knowledge: {title}")
            return knowledge
            
        except Exception as e:
            logger.error(f"Error adding knowledge: {e}")
            self.db.rollback()
            raise
    
    def get_all_knowledge(
        self,
        category: Optional[str] = None,
        limit: int = 100
    ) -> List[KnowledgeBase]:
        """Get all knowledge entries"""
        try:
            query = self.db.query(KnowledgeBase)
            
            if category:
                query = query.filter(KnowledgeBase.category == category)
            
            knowledge = query.limit(limit).all()
            return knowledge
            
        except Exception as e:
            logger.error(f"Error getting knowledge: {e}")
            return []
    
    async def search_relevant_knowledge(
        self,
        query: str,
        limit: int = 3
    ) -> str:
        """
        Search for relevant knowledge based on query
        Uses simple keyword matching (can be improved with vector search)
        
        Args:
            query: Search query
            limit: Number of results
        
        Returns:
            Concatenated relevant content
        """
        try:
            # Simple keyword search (for production, use vector similarity)
            knowledge_entries = self.db.query(KnowledgeBase).filter(
                KnowledgeBase.content.ilike(f"%{query}%")
            ).limit(limit).all()
            
            if not knowledge_entries:
                return ""
            
            # Concatenate relevant content
            context_parts = []
            for entry in knowledge_entries:
                context_parts.append(f"Title: {entry.title}\n{entry.content}")
            
            return "\n\n".join(context_parts)
            
        except Exception as e:
            logger.error(f"Error searching knowledge: {e}")
            return ""
    
    def delete_knowledge(self, knowledge_id: int) -> bool:
        """Delete knowledge entry"""
        try:
            knowledge = self.db.query(KnowledgeBase).filter(
                KnowledgeBase.id == knowledge_id
            ).first()
            
            if not knowledge:
                return False
            
            self.db.delete(knowledge)
            self.db.commit()
            logger.info(f"Deleted knowledge: {knowledge_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting knowledge: {e}")
            self.db.rollback()
            return False
    
    def update_knowledge(
        self,
        knowledge_id: int,
        title: Optional[str] = None,
        content: Optional[str] = None,
        category: Optional[str] = None
    ) -> Optional[KnowledgeBase]:
        """Update knowledge entry"""
        try:
            knowledge = self.db.query(KnowledgeBase).filter(
                KnowledgeBase.id == knowledge_id
            ).first()
            
            if not knowledge:
                return None
            
            if title:
                knowledge.title = title
            if content:
                knowledge.content = content
            if category:
                knowledge.category = category
            
            self.db.commit()
            self.db.refresh(knowledge)
            logger.info(f"Updated knowledge: {knowledge_id}")
            return knowledge
            
        except Exception as e:
            logger.error(f"Error updating knowledge: {e}")
            self.db.rollback()
            return None