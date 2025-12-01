"""Redis connection and token storage."""

import secrets
import threading
from typing import Optional

import redis

from app.config import get_settings

settings = get_settings()

# Redis client (singleton) with thread-safe initialization
_redis_client = None
_redis_client_lock = threading.Lock()


def get_redis_client() -> redis.Redis:
    """Get Redis client (singleton, thread-safe)."""
    global _redis_client
    if _redis_client is None:
        with _redis_client_lock:
            if _redis_client is None:
                _redis_client = redis.Redis(
                    host=settings.redis_host,
                    port=settings.redis_port,
                    db=settings.redis_db,
                    password=settings.redis_password if settings.redis_password else None,
                    decode_responses=True,
                )
    return _redis_client


def _get_token_key(user_id: int) -> str:
    """Generate Redis key for user token."""
    return f"user_token:{user_id}"


def store_token(user_id: int, token: str, expire_seconds: int) -> bool:
    """Store token in Redis with expiration."""
    client = get_redis_client()
    try:
        key = _get_token_key(user_id)
        client.setex(key, expire_seconds, token)
        return True
    except redis.RedisError:
        return False


def get_stored_token(user_id: int) -> Optional[str]:
    """Get stored token for user from Redis."""
    client = get_redis_client()
    try:
        key = _get_token_key(user_id)
        return client.get(key)
    except redis.RedisError:
        return None


def delete_token(user_id: int) -> bool:
    """Delete token from Redis."""
    client = get_redis_client()
    try:
        key = _get_token_key(user_id)
        client.delete(key)
        return True
    except redis.RedisError:
        return False


def is_token_valid(user_id: int, token: str) -> bool:
    """Check if the provided token matches the stored token."""
    stored_token = get_stored_token(user_id)
    if stored_token is None:
        return False
    return secrets.compare_digest(stored_token, token)
