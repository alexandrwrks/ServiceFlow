from sqlalchemy import text

from cache.redis import redis
from database.config import new_session
from utils.logger import logger


async def check_database_conn() -> bool:
    try:
        async with new_session as session:
            await session.execute(text("SELECT 1"))
            return True
    except Exception:
        logger.exception("Database connection failed")
        return False


async def check_redis_conn() -> bool:
    try:
        await redis.ping()
        return True
    except Exception:
        logger.exception("Redis connection failed")
        return False