import hashlib
import uuid
from datetime import datetime
from typing import Optional


def generate_session_id() -> str:
    """Generate unique session ID"""
    return str(uuid.uuid4())


def get_cache_key(prefix: str, identifier: str) -> str:
    """Generate cache key"""
    return f"{prefix}:{identifier}"


def hash_string(text: str) -> str:
    """Generate SHA256 hash of string"""
    return hashlib.sha256(text.encode()).hexdigest()


def format_timestamp(dt: Optional[datetime] = None) -> str:
    """Format datetime to ISO string"""
    if dt is None:
        dt = datetime.utcnow()
    return dt.isoformat()


def clean_phone_number(phone: str) -> str:
    """Clean and format phone number"""
    # Remove whatsapp: prefix if exists
    phone = phone.replace("whatsapp:", "")
    # Remove all non-numeric characters except +
    return ''.join(c for c in phone if c.isdigit() or c == '+')


def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text to max length"""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."