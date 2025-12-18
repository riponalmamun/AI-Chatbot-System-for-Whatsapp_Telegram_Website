from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Dict
from datetime import datetime, timedelta
from collections import defaultdict
from app.core.config import settings
from app.utils.logger import logger


class RateLimiter(BaseHTTPMiddleware):
    """
    Simple in-memory rate limiter middleware
    For production, use Redis-based rate limiting
    """
    
    def __init__(self, app, calls: int = None, period: int = 60):
        super().__init__(app)
        self.calls = calls or settings.RATE_LIMIT_PER_MINUTE
        self.period = period  # seconds
        self.clients: Dict[str, list] = defaultdict(list)
    
    async def dispatch(self, request: Request, call_next):
        # Get client identifier (IP address)
        client_ip = request.client.host
        
        # Skip rate limiting for health check
        if request.url.path == "/health":
            return await call_next(request)
        
        # Get current timestamp
        now = datetime.utcnow()
        
        # Clean old timestamps
        cutoff = now - timedelta(seconds=self.period)
        self.clients[client_ip] = [
            timestamp for timestamp in self.clients[client_ip]
            if timestamp > cutoff
        ]
        
        # Check rate limit
        if len(self.clients[client_ip]) >= self.calls:
            logger.warning(f"Rate limit exceeded for {client_ip}")
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={
                    "detail": "Rate limit exceeded. Please try again later.",
                    "retry_after": self.period
                }
            )
        
        # Add current request timestamp
        self.clients[client_ip].append(now)
        
        # Process request
        response = await call_next(request)
        
        # Add rate limit headers
        remaining = self.calls - len(self.clients[client_ip])
        response.headers["X-RateLimit-Limit"] = str(self.calls)
        response.headers["X-RateLimit-Remaining"] = str(max(0, remaining))
        response.headers["X-RateLimit-Reset"] = str(int((now + timedelta(seconds=self.period)).timestamp()))
        
        return response