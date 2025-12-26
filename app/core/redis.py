"""Redis client configuration and management."""
import redis.asyncio as redis

from app.core.config import settings

# Global Redis client instance (Singleton pattern)
redis_client: redis.Redis | None = None


async def get_redis_client() -> redis.Redis:
    """
    Get or create the Redis client instance.

    Returns:
        Redis client instance configured with application settings.
    """
    global redis_client
    if redis_client is None:
        redis_client = redis.from_url(
            settings.REDIS_URL,
            encoding="utf-8",
            decode_responses=True,
        )
    return redis_client


async def close_redis_client() -> None:
    """
    Close the Redis client connection.

    Should be called during application shutdown.
    """
    global redis_client
    if redis_client:
        await redis_client.close()
        redis_client = None
