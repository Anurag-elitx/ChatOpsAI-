"""
Custom logging configuration for the ChatOps platform.

Sets up structured logging with loguru, directing output
to both console and a rotating log file. All modules should
import `logger` from here instead of using print().
"""

import sys
from loguru import logger

from app.config import APP_ENV, DEBUG

# Remove default handler so we can configure our own
logger.remove()

# Console output — show DEBUG level in dev, INFO in production
_console_level = "DEBUG" if DEBUG else "INFO"
logger.add(
    sys.stderr,
    level=_console_level,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
           "<level>{level: <8}</level> | "
           "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> — "
           "<level>{message}</level>",
    colorize=True,
)

# File output — rotating daily, kept for 14 days
logger.add(
    "logs/chatops_{time:YYYY-MM-DD}.log",
    rotation="1 day",
    retention="14 days",
    level="DEBUG",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} — {message}",
    enqueue=True,
)

logger.info(f"Logger initialised — env={APP_ENV}")
