from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    """Base user schema"""
    user_identifier: str
    platform: str
    name: Optional[str] = None


class UserCreate(UserBase):
    """User creation schema"""
    pass


class UserResponse(UserBase):
    """User response schema"""
    id: int
    created_at: datetime
    last_active: datetime
    
    class Config:
        from_attributes = True