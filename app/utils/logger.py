from loguru import logger

logger.remove()

logger.add(
    "/app/logs/api.log",
    level="INFO",
    format="{time} {level} {message}",
    rotation="10 MB",
    retention="30 days",
    compression="zip",
    enqueue=True,
)