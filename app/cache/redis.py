from redis.asyncio import Redis

from app.utils.settings import settings

redis = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, decode_responses=True)