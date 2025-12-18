import logging
import sys
from pythonjsonlogger import jsonlogger
from app.core.config import settings

# Create logger
logger = logging.getLogger("chatbot")
logger.setLevel(logging.DEBUG if settings.DEBUG else logging.INFO)

# Create console handler
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG if settings.DEBUG else logging.INFO)

# Create formatter
if settings.DEBUG:
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
else:
    formatter = jsonlogger.JsonFormatter(
        '%(asctime)s %(name)s %(levelname)s %(message)s'
    )

console_handler.setFormatter(formatter)
logger.addHandler(console_handler)