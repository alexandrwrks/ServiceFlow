from redis.asyncio import Redis

from cache.cache_service import CacheService
from utils.settings import settings

redis = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, decode_responses=True)


async def get_cache_service() -> CacheService:
    return CacheService(redis)