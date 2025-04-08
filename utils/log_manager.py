from loguru import logger
import sys
import os

logger.remove()

# Environment-based config
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
ENV = os.getenv("ENVIRONMENT", "development")

LOGS_DIR = "logs"
os.makedirs(LOGS_DIR, exist_ok=True)

LOG_FILE_PATH = os.path.join(LOGS_DIR, f"{ENV}.log")

logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    colorize=True,
    level="DEBUG" if DEBUG else "INFO"
)

logger.add(
    LOG_FILE_PATH,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} - {message}",
    level="DEBUG",
    rotation=None,
    retention=None,
    compression=None
)

logger.configure()