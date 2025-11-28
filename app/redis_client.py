"""Redis connection and token storage."""

from typing import Optional

import redis

from app.config import get_settings

settings = get_settings()

# Redis connection pool for better performance
_redis_pool: Optional[redis.ConnectionPool] = None


def get_redis_pool() -> redis.ConnectionPool:
    """Get Redis connection pool (singleton)."""
    global _redis_pool
    if _redis_pool is None:
        _redis_pool = redis.ConnectionPool(
            host=settings.redis_host,
            port=settings.redis_port,
            db=settings.redis_db,
            password=settings.redis_password if settings.redis_password else None,
            decode_responses=True,
        )
    return _redis_pool


def get_redis_client() -> redis.Redis:
    """Get Redis client instance with connection pooling."""
    return redis.Redis(connection_pool=get_redis_pool())


def store_token(user_id: int, token: str, expire_seconds: int) -> bool:
    """Store token in Redis with expiration."""
    client = get_redis_client()
    key = f"token:{user_id}"
    client.set(key, token, ex=expire_seconds)
    return True


def get_stored_token(user_id: int) -> Optional[str]:
    """Get stored token for user from Redis."""
    client = get_redis_client()
    key = f"token:{user_id}"
    return client.get(key)


def delete_token(user_id: int) -> bool:
    """Delete token from Redis."""
    client = get_redis_client()
    key = f"token:{user_id}"
    client.delete(key)
    return True


def is_token_valid(user_id: int, token: str) -> bool:
    """Check if the provided token matches the stored token."""
    stored_token = get_stored_token(user_id)
    return stored_token == token
