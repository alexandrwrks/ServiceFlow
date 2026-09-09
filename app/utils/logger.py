from pathlib import Path
from loguru import logger

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / "logs"

LOG_DIR.mkdir(parents=True, exist_ok=True)

logger.remove()

logger.add(
    LOG_DIR / "api.log",
    level="DEBUG",
    format="{time} | {level} | {message}",
    rotation="10 MB",
    retention="30 days",
    compression="zip",
    enqueue=True,
)