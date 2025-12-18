from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.core.database import Base


class PlatformType(str, enum.Enum):
    """Platform types"""
    WEBSITE = "website"
    WHATSAPP = "whatsapp"
    TELEGRAM = "telegram"


class User(Base):
    """User model"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    user_identifier = Column(String, unique=True, index=True, nullable=False)
    platform = Column(Enum(PlatformType), nullable=False)
    name = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_active = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    conversations = relationship("Conversation", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User {self.user_identifier} ({self.platform})>"