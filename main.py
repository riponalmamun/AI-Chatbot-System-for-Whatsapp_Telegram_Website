from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.api import website, whatsapp, telegram
from app.core.config import settings
from app.core.database import init_db
from app.middleware.rate_limiter import RateLimiter
from app.middleware.error_handler import setup_exception_handlers
from app.utils.logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events
    """
    # Startup
    logger.info("=" * 50)
    logger.info("Starting AI Chatbot System...")
    logger.info(f"AI Provider: {settings.AI_PROVIDER}")
    logger.info(f"AI Model: {settings.AI_MODEL}")
    logger.info(f"Debug Mode: {settings.DEBUG}")
    logger.info("=" * 50)
    
    # Initialize database
    try:
        init_db()
        logger.info("✅ Database initialized successfully")
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")
        logger.warning("⚠️  Continuing without database...")
    
    yield
    
    # Shutdown
    logger.info("=" * 50)
    logger.info("Shutting down AI Chatbot System...")
    logger.info("=" * 50)


# Create FastAPI app
app = FastAPI(
    title="AI Chatbot System",
    description="""
    Multi-platform AI chatbot with FastAPI supporting Website, WhatsApp, and Telegram.
    
    ## Features
    * 🤖 Multiple AI providers (Gemini, OpenAI, Groq)
    * 💬 Multi-platform support (Website, WhatsApp, Telegram)
    * 📝 Conversation history management
    * 🧠 Knowledge base (RAG) support
    * ⚡ Redis caching
    * 🔒 Rate limiting
    """,
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    contact={
        "name": "Support",
        "email": "support@example.com",
    },
    license_info={
        "name": "MIT",
    }
)

# Setup exception handlers
setup_exception_handlers(app)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-RateLimit-Limit", "X-RateLimit-Remaining", "X-RateLimit-Reset"]
)

# Rate Limiting Middleware
app.add_middleware(RateLimiter)

# Include API routers
app.include_router(
    website.router,
    prefix="/api/chat",
    tags=["Website Chat"]
)

app.include_router(
    whatsapp.router,
    prefix="/whatsapp",
    tags=["WhatsApp"]
)

app.include_router(
    telegram.router,
    prefix="/telegram",
    tags=["Telegram"]
)


@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint - API information
    """
    return {
        "message": "🤖 AI Chatbot System API",
        "version": "1.0.0",
        "status": "running",
        "ai_provider": settings.AI_PROVIDER,
        "ai_model": settings.AI_MODEL,
        "documentation": {
            "swagger": "/docs",
            "redoc": "/redoc"
        },
        "endpoints": {
            "website_chat": {
                "send_message": "POST /api/chat/send",
                "get_history": "GET /api/chat/history/{session_id}",
                "delete_history": "DELETE /api/chat/history/{session_id}"
            },
            "whatsapp": {
                "webhook": "POST /whatsapp/webhook",
                "status": "GET /whatsapp/status",
                "test": "POST /whatsapp/send-test"
            },
            "telegram": {
                "webhook": "POST /telegram/webhook",
                "setup": "GET /telegram/setup",
                "status": "GET /telegram/status",
                "test": "POST /telegram/send-test"
            }
        }
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint
    """
    return {
        "status": "healthy",
        "service": "ai-chatbot-system",
        "version": "1.0.0",
        "ai_provider": settings.AI_PROVIDER,
        "ai_model": settings.AI_MODEL,
        "debug_mode": settings.DEBUG
    }


@app.get("/info", tags=["Info"])
async def system_info():
    """
    Get detailed system information
    """
    return {
        "app_name": "AI Chatbot System",
        "version": "1.0.0",
        "description": "Multi-platform AI chatbot with FastAPI",
        "ai_config": {
            "provider": settings.AI_PROVIDER,
            "model": settings.AI_MODEL,
            "max_history": settings.MAX_CONVERSATION_HISTORY,
            "temperature": settings.TEMPERATURE
        },
        "platforms": [
            {
                "name": "Website",
                "status": "active",
                "endpoint": "/api/chat/send"
            },
            {
                "name": "WhatsApp",
                "status": "active" if settings.TWILIO_ACCOUNT_SID else "inactive",
                "endpoint": "/whatsapp/webhook"
            },
            {
                "name": "Telegram",
                "status": "active" if settings.TELEGRAM_BOT_TOKEN else "inactive",
                "endpoint": "/telegram/webhook"
            }
        ],
        "features": [
            "Multi-platform support",
            "Conversation history",
            "Knowledge base (RAG)",
            "Rate limiting",
            "Redis caching",
            "PostgreSQL database"
        ]
    }


@app.get("/config", tags=["Config"])
async def get_config():
    """
    Get current configuration (non-sensitive)
    """
    return {
        "ai_provider": settings.AI_PROVIDER,
        "ai_model": settings.AI_MODEL,
        "max_conversation_history": settings.MAX_CONVERSATION_HISTORY,
        "temperature": settings.TEMPERATURE,
        "max_tokens": settings.MAX_TOKENS,
        "rate_limit_per_minute": settings.RATE_LIMIT_PER_MINUTE,
        "debug_mode": settings.DEBUG,
        "whatsapp_configured": bool(settings.TWILIO_ACCOUNT_SID),
        "telegram_configured": bool(settings.TELEGRAM_BOT_TOKEN),
        "redis_configured": bool(settings.REDIS_URL)
    }


if __name__ == "__main__":
    import uvicorn
    
    logger.info("Starting server directly...")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="info"
    )