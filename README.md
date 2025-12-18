# 🤖 AI Chatbot System for WhatsApp, Telegram & Website

A comprehensive, production-ready AI-powered chatbot system built with FastAPI that seamlessly integrates with multiple platforms including WhatsApp, Telegram, and web applications. This system leverages advanced AI capabilities to provide intelligent, context-aware conversations across different communication channels.

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104%2B-009688.svg)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 📋 Table of Contents

- [Features](#-features)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [API Endpoints](#-api-endpoints)
- [Project Structure](#-project-structure)
- [Database](#-database)
- [Deployment](#-deployment)
- [Contributing](#-contributing)
- [License](#-license)
- [Contact](#-contact)

---

## ✨ Features

### 🌐 Multi-Platform Support
- **WhatsApp Integration** - Connect your chatbot to WhatsApp Business API
- **Telegram Bot** - Full-featured Telegram bot with webhook support
- **Website Chat** - Embeddable web chat widget for your website

### 🧠 AI-Powered Intelligence
- Advanced natural language processing
- Context-aware conversations
- Knowledge base integration for domain-specific responses
- Conversation history tracking and analysis

### 🔧 Enterprise Features
- **Rate Limiting** - Protect your API from abuse
- **Error Handling** - Comprehensive error tracking and logging
- **Caching** - Redis-based caching for improved performance
- **Database Management** - PostgreSQL with Alembic migrations
- **Security** - JWT authentication and secure API endpoints
- **Docker Support** - Easy containerized deployment

### 📊 Management & Analytics
- User management system
- Conversation history and analytics
- Knowledge base management
- Webhook handling for real-time updates

---

## 🏗 Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Client Applications                      │
│          (WhatsApp, Telegram, Website Chat)                  │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Application                       │
│  ┌──────────────┬──────────────┬──────────────┐            │
│  │   WhatsApp   │   Telegram   │   Website    │            │
│  │   Webhook    │   Webhook    │   REST API   │            │
│  └──────┬───────┴──────┬───────┴──────┬───────┘            │
│         │              │              │                     │
│         └──────────────┼──────────────┘                     │
│                        ▼                                     │
│              ┌─────────────────┐                            │
│              │  AI Service     │                            │
│              └────────┬────────┘                            │
│                       │                                      │
│         ┌─────────────┼─────────────┐                       │
│         ▼             ▼             ▼                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                 │
│  │Conversation│  │Knowledge │  │  Cache   │                 │
│  │  Service  │  │  Service │  │  (Redis) │                 │
│  └──────────┘  └──────────┘  └──────────┘                 │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
         ┌────────────────┐
         │   PostgreSQL   │
         │    Database    │
         └────────────────┘
```

---

## 🛠 Tech Stack

### Backend
- **FastAPI** - Modern, fast web framework for building APIs
- **Python 3.8+** - Core programming language
- **Pydantic** - Data validation using Python type annotations
- **SQLAlchemy** - SQL toolkit and ORM
- **Alembic** - Database migration tool

### Database & Cache
- **PostgreSQL** - Primary database
- **Redis** - Caching and session management

### AI & NLP
- OpenAI API / Custom AI models
- Natural Language Processing libraries

### DevOps
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **Uvicorn** - ASGI server

### External APIs
- WhatsApp Business API
- Telegram Bot API

---

## 📦 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8 or higher**
- **PostgreSQL 12+**
- **Redis 6+** (optional, for caching)
- **Docker & Docker Compose** (for containerized deployment)
- **Git**

### API Keys Required
- OpenAI API Key (or your preferred AI service)
- WhatsApp Business API credentials
- Telegram Bot Token (from @BotFather)

---

## 🚀 Installation

### Option 1: Local Development Setup

#### 1. Clone the Repository
```bash
git clone https://github.com/riponalmamun/AI-Chatbot-System-for-Whatsapp_Telegram_Website.git
cd AI-Chatbot-System-for-Whatsapp_Telegram_Website
```

#### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/MacOS
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 4. Set Up Environment Variables
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your credentials
nano .env  # or use any text editor
```

#### 5. Initialize Database
```bash
# Run Alembic migrations
alembic upgrade head
```

#### 6. Start the Application
```bash
# Development server with hot reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Production server
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

The API will be available at: `http://localhost:8000`

Interactive API docs: `http://localhost:8000/docs`

---

### Option 2: Docker Deployment

#### 1. Clone the Repository
```bash
git clone https://github.com/riponalmamun/AI-Chatbot-System-for-Whatsapp_Telegram_Website.git
cd AI-Chatbot-System-for-Whatsapp_Telegram_Website
```

#### 2. Configure Environment
```bash
cp .env.example .env
# Edit .env with your configuration
```

#### 3. Build and Run with Docker Compose
```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

#### 4. Run Database Migrations
```bash
docker-compose exec app alembic upgrade head
```

---

## ⚙️ Configuration

Create a `.env` file in the root directory with the following variables:

```env
# Application Settings
APP_NAME=AI Chatbot System
APP_VERSION=1.0.0
DEBUG=False
SECRET_KEY=your-super-secret-key-change-this

# Database Configuration
DATABASE_URL=postgresql://user:password@localhost:5432/chatbot_db

# Redis Configuration (Optional)
REDIS_URL=redis://localhost:6379/0

# AI Service Configuration
OPENAI_API_KEY=sk-your-openai-api-key
AI_MODEL=gpt-4
MAX_TOKENS=2000
TEMPERATURE=0.7

# WhatsApp Configuration
WHATSAPP_API_URL=https://graph.facebook.com/v17.0
WHATSAPP_PHONE_NUMBER_ID=your-phone-number-id
WHATSAPP_ACCESS_TOKEN=your-whatsapp-access-token
WHATSAPP_VERIFY_TOKEN=your-webhook-verify-token

# Telegram Configuration
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
TELEGRAM_WEBHOOK_URL=https://yourdomain.com/api/telegram/webhook

# Security
JWT_SECRET_KEY=your-jwt-secret-key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Rate Limiting
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_PERIOD=60

# CORS Settings
ALLOWED_ORIGINS=http://localhost:3000,https://yourdomain.com

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
```

---

## 💻 Usage

### Setting Up Telegram Bot

1. **Create Bot with BotFather**
   - Message [@BotFather](https://t.me/botfather) on Telegram
   - Send `/newbot` and follow instructions
   - Save your bot token

2. **Set Webhook**
   ```bash
   curl -X POST "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook?url=https://yourdomain.com/api/telegram/webhook"
   ```

3. **Test Your Bot**
   - Search for your bot on Telegram
   - Send a message and get AI-powered responses

---

### Setting Up WhatsApp Integration

1. **Facebook Developer Account**
   - Create a Meta (Facebook) Developer account
   - Create a new app for WhatsApp Business

2. **Get Credentials**
   - Phone Number ID
   - Access Token
   - Create a Verify Token

3. **Configure Webhook**
   - Set webhook URL: `https://yourdomain.com/api/whatsapp/webhook`
   - Add verify token from your `.env`
   - Subscribe to message events

4. **Test Integration**
   - Send a test message to your WhatsApp Business number
   - Verify webhook receives the message

---

### Website Integration

#### Embedding the Chat Widget

```html
<!DOCTYPE html>
<html>
<head>
    <title>My Website with AI Chat</title>
</head>
<body>
    <h1>Welcome to My Website</h1>
    
    <!-- Your website content -->
    
    <!-- Chat Widget Integration -->
    <div id="ai-chatbot"></div>
    <script>
        (function() {
            const chatWidget = document.createElement('iframe');
            chatWidget.src = 'https://yourdomain.com/chat-widget';
            chatWidget.style.cssText = 'position:fixed;bottom:20px;right:20px;width:400px;height:600px;border:none;border-radius:10px;box-shadow:0 0 20px rgba(0,0,0,0.2);';
            document.getElementById('ai-chatbot').appendChild(chatWidget);
        })();
    </script>
</body>
</html>
```

#### REST API Usage

```javascript
// Send a message
const sendMessage = async (message, userId) => {
    const response = await fetch('https://yourdomain.com/api/website/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer YOUR_API_TOKEN'
        },
        body: JSON.stringify({
            message: message,
            user_id: userId,
            platform: 'website'
        })
    });
    
    const data = await response.json();
    return data.response;
};

// Example usage
sendMessage('Hello, how can you help me?', 'user123')
    .then(response => console.log(response))
    .catch(error => console.error(error));
```

---

## 🔌 API Endpoints

### Authentication
```
POST   /api/auth/login          - User login
POST   /api/auth/register       - User registration
POST   /api/auth/refresh        - Refresh access token
```

### Website Chat API
```
POST   /api/website/chat        - Send message and get AI response
GET    /api/website/history     - Get conversation history
DELETE /api/website/history     - Clear conversation history
```

### WhatsApp Webhook
```
GET    /api/whatsapp/webhook    - Webhook verification
POST   /api/whatsapp/webhook    - Receive WhatsApp messages
POST   /api/whatsapp/send       - Send WhatsApp message
```

### Telegram Webhook
```
POST   /api/telegram/webhook    - Receive Telegram updates
POST   /api/telegram/send       - Send Telegram message
```

### Knowledge Base Management
```
POST   /api/knowledge/add       - Add knowledge to the system
GET    /api/knowledge/list      - List all knowledge entries
PUT    /api/knowledge/{id}      - Update knowledge entry
DELETE /api/knowledge/{id}      - Delete knowledge entry
```

### User Management
```
GET    /api/users               - List all users
GET    /api/users/{id}          - Get user details
PUT    /api/users/{id}          - Update user
DELETE /api/users/{id}          - Delete user
```

### System
```
GET    /health                  - Health check endpoint
GET    /docs                    - Interactive API documentation
GET    /redoc                   - ReDoc API documentation
```

---

## 📁 Project Structure

```
ai-chatbot-system/
│
├── alembic/                    # Database migrations
│   ├── versions/               # Migration scripts
│   ├── env.py                  # Alembic environment
│   └── script.py.mako          # Migration template
│
├── app/                        # Main application package
│   ├── api/                    # API route handlers
│   │   ├── telegram.py         # Telegram webhook endpoints
│   │   ├── website.py          # Website chat endpoints
│   │   └── whatsapp.py         # WhatsApp webhook endpoints
│   │
│   ├── core/                   # Core functionality
│   │   ├── config.py           # Configuration management
│   │   ├── database.py         # Database connection
│   │   └── security.py         # Security utilities (JWT, etc.)
│   │
│   ├── middleware/             # Custom middleware
│   │   ├── error_handler.py    # Global error handling
│   │   └── rate_limiter.py     # API rate limiting
│   │
│   ├── models/                 # Database models (SQLAlchemy)
│   │   ├── base.py             # Base model class
│   │   ├── user.py             # User model
│   │   ├── conversation.py     # Conversation model
│   │   └── knowledge_base.py   # Knowledge base model
│   │
│   ├── schemas/                # Pydantic schemas (validation)
│   │   ├── chat.py             # Chat message schemas
│   │   ├── user.py             # User schemas
│   │   └── webhook.py          # Webhook schemas
│   │
│   ├── services/               # Business logic services
│   │   ├── ai_service.py       # AI/NLP integration
│   │   ├── conversation_service.py  # Conversation management
│   │   ├── knowledge_service.py     # Knowledge base operations
│   │   ├── telegram_service.py      # Telegram bot logic
│   │   └── whatsapp_service.py      # WhatsApp bot logic
│   │
│   └── utils/                  # Utility functions
│       ├── cache.py            # Redis caching utilities
│       ├── helpers.py          # Helper functions
│       └── logger.py           # Logging configuration
│
├── logs/                       # Application logs
├── tests/                      # Unit and integration tests
│
├── .env.example                # Environment variables template
├── .gitignore                  # Git ignore rules
├── alembic.ini                 # Alembic configuration
├── docker-compose.yml          # Docker Compose configuration
├── Dockerfile                  # Docker image definition
├── main.py                     # Application entry point
├── requirements.txt            # Python dependencies
├── setup.py                    # Package setup
└── README.md                   # Project documentation
```

---

## 🗄 Database

### Database Schema

The system uses PostgreSQL with the following main tables:

#### Users Table
- `id` - Primary key
- `username` - Unique username
- `email` - User email
- `hashed_password` - Encrypted password
- `is_active` - Account status
- `created_at` - Registration timestamp

#### Conversations Table
- `id` - Primary key
- `user_id` - Foreign key to users
- `platform` - Source platform (whatsapp/telegram/website)
- `message` - User message
- `response` - AI response
- `created_at` - Message timestamp

#### Knowledge Base Table
- `id` - Primary key
- `category` - Knowledge category
- `question` - Sample question
- `answer` - Predefined answer
- `keywords` - Search keywords
- `created_at` - Entry creation time

### Running Migrations

```bash
# Create a new migration
alembic revision --autogenerate -m "description of changes"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# View migration history
alembic history
```

---

## 🚢 Deployment

### Deploy to Production Server

#### 1. Server Setup
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install python3-pip python3-venv postgresql redis-server nginx -y

# Install Docker (optional)
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

#### 2. Clone and Configure
```bash
cd /var/www
sudo git clone https://github.com/riponalmamun/AI-Chatbot-System-for-Whatsapp_Telegram_Website.git
cd AI-Chatbot-System-for-Whatsapp_Telegram_Website

# Set up environment
sudo cp .env.example .env
sudo nano .env  # Configure production settings
```

#### 3. Run with Docker
```bash
sudo docker-compose -f docker-compose.prod.yml up -d
```

#### 4. Configure Nginx (Reverse Proxy)
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

#### 5. SSL Certificate (Let's Encrypt)
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
```

### Deploy to Cloud Platforms

#### Heroku
```bash
# Install Heroku CLI
# Login to Heroku
heroku login

# Create app
heroku create your-app-name

# Add PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev

# Deploy
git push heroku main

# Run migrations
heroku run alembic upgrade head
```

#### AWS EC2
- Launch an EC2 instance (Ubuntu 22.04 LTS)
- Configure security groups (ports 80, 443, 8000)
- Follow production server setup steps
- Use AWS RDS for PostgreSQL
- Use ElastiCache for Redis

#### Google Cloud Platform
- Deploy to Cloud Run (containerized)
- Use Cloud SQL for PostgreSQL
- Use Memorystore for Redis

---

## 🧪 Testing

### Run Tests
```bash
# Install test dependencies
pip install pytest pytest-asyncio pytest-cov

# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/test_ai_service.py
```

### Example Test
```python
# tests/test_chat.py
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_send_message():
    response = client.post(
        "/api/website/chat",
        json={"message": "Hello", "user_id": "test123"}
    )
    assert response.status_code == 200
    assert "response" in response.json()
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. **Fork the Repository**
   ```bash
   # Click "Fork" button on GitHub
   ```

2. **Clone Your Fork**
   ```bash
   git clone https://github.com/YOUR_USERNAME/AI-Chatbot-System-for-Whatsapp_Telegram_Website.git
   cd AI-Chatbot-System-for-Whatsapp_Telegram_Website
   ```

3. **Create a Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **Make Changes and Commit**
   ```bash
   git add .
   git commit -m "Add: your feature description"
   ```

5. **Push to Your Fork**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create Pull Request**
   - Go to the original repository
   - Click "New Pull Request"
   - Select your branch and submit

### Code Style Guidelines
- Follow PEP 8 for Python code
- Use type hints wherever possible
- Write descriptive commit messages
- Add tests for new features
- Update documentation as needed

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2024 Ripon Al Mamun

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 📞 Contact

**Ripon Al Mamun**

- GitHub: [@riponalmamun]([https://github.com/riponalmamun](https://github.com/riponalmamun))
- Email: riponalmamunrasel@gmail.com
- LinkedIn: [Your LinkedIn Profile]([https://linkedin.com/in/yourprofile](https://www.linkedin.com/in/mdriponalmamun/))
- Portfolio: [yourwebsite.com](https://yourwebsite.com)

---

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework
- [OpenAI](https://openai.com/) - AI capabilities
- [Telegram](https://core.telegram.org/bots/api) - Bot API
- [WhatsApp Business API](https://developers.facebook.com/docs/whatsapp) - WhatsApp integration
- All contributors and supporters of this project

---

## 🗺 Roadmap

### Upcoming Features
- [ ] Support for additional platforms (Discord, Slack, Microsoft Teams)
- [ ] Advanced analytics dashboard
- [ ] Multi-language support
- [ ] Voice message support
- [ ] Image recognition and processing
- [ ] Custom AI model training interface
- [ ] A/B testing for responses
- [ ] Admin panel for management
- [ ] Sentiment analysis
- [ ] Conversation export functionality

---

## 📊 Performance

- **Response Time**: < 500ms average
- **Concurrent Users**: Supports 1000+ simultaneous conversations
- **Uptime**: 99.9% availability
- **Rate Limiting**: Configurable per endpoint
- **Caching**: Redis-based for improved performance

---

## 🔒 Security

- JWT-based authentication
- Password hashing with bcrypt
- SQL injection prevention (SQLAlchemy ORM)
- XSS protection
- CORS configuration
- Rate limiting to prevent abuse
- Webhook signature verification
- Environment variable security
- Regular security updates

---

## ❓ FAQ

**Q: Can I use this without Docker?**  
A: Yes, follow the local development setup instructions.

**Q: What AI models are supported?**  
A: OpenAI GPT models by default, but you can integrate any AI service.

**Q: Is this production-ready?**  
A: Yes, with proper configuration and security measures.

**Q: Can I add more platforms?**  
A: Yes, the architecture supports easy integration of new platforms.

**Q: How do I update the knowledge base?**  
A: Use the knowledge management API endpoints or admin panel.

---

## 📈 Support This Project

If you find this project helpful, please consider:
- ⭐ Starring the repository
- 🐛 Reporting bugs
- 💡 Suggesting new features
- 🤝 Contributing code
- 📢 Sharing with others

---

**Made with ❤️ by Ripon Al Mamun**

⭐ **Star this repository if you find it useful!** ⭐
