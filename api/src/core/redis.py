"""
Redis client management and key utilities.

This module centralizes Redis connection pooling, lifecycle management,
and key construction helpers for multi-tenant workloads.
"""

from __future__ import annotations

import asyncio
import logging
from typing import Optional, cast

import redis.asyncio as redis
from redis.asyncio import Redis
from redis.exceptions import RedisError
from src.core.config import get_settings

logger = logging.getLogger(__name__)

# Cached Redis client instance
_redis_client: Redis | None = None


def _create_redis_client() -> Redis:
    """
    Create a configured Redis client using application settings.

    Returns:
        Redis client with connection pooling

    """
    settings = get_settings()

    client: Redis = cast(
        Redis,
        redis.from_url(  # type: ignore[no-untyped-call]
            settings.redis_url,
            max_connections=settings.redis_pool_max_connections,
            socket_connect_timeout=settings.redis_socket_connect_timeout,
            socket_timeout=settings.redis_socket_timeout,
            health_check_interval=settings.redis_health_check_interval,
        ),
    )
    return client


def get_redis() -> Redis:
    """
    Get or create the shared Redis client.

    Returns:
        Redis client instance

    Raises:
        ValueError: If Redis URL is not configured
    """
    global _redis_client

    if _redis_client is None:
        _redis_client = _create_redis_client()

    return _redis_client


async def ping_redis(timeout_seconds: float | None = None) -> bool:
    """
    Perform a health check against Redis with an optional timeout.

    Args:
        timeout_seconds: Optional timeout in seconds

    Returns:
        True if Redis responds to PING, False otherwise
    """
    client = get_redis()
    timeout = timeout_seconds or get_settings().redis_health_check_timeout

    try:
        ping_result = client.ping()
        if asyncio.iscoroutine(ping_result):
            return bool(await asyncio.wait_for(ping_result, timeout=timeout))
        return bool(ping_result)
    except (TimeoutError, RedisError):
        return False


async def close_redis() -> None:
    """
    Gracefully close the Redis client and its underlying connection pool.
    """
    global _redis_client
    if _redis_client is None:
        return

    client = _redis_client
    try:
        await _shutdown_client(client)
    finally:
        _redis_client = None


async def _shutdown_client(client: Redis) -> None:
    """
    Close a Redis client and disconnect its pool.
    """
    close_callable = getattr(client, "aclose", None) or getattr(client, "close", None)
    try:
        if close_callable is not None:
            result = close_callable()
            if asyncio.iscoroutine(result):
                await result
    finally:
        await _disconnect_pool(client)


async def _disconnect_pool(client: Redis) -> None:
    """
    Disconnect the Redis connection pool, awaiting async implementations.
    """
    try:
        disconnect_callable = client.connection_pool.disconnect(inuse_connections=True)
        if asyncio.iscoroutine(disconnect_callable):
            await disconnect_callable
    except Exception as exc:
        logger.warning("Failed to disconnect Redis connection pool: %s", exc)


async def reset_redis_client() -> None:
    """
    Reset the cached Redis client (useful for tests or config reloads).
    """
    global _redis_client
    if _redis_client is None:
        return

    client = _redis_client
    try:
        await _shutdown_client(client)
    finally:
        _redis_client = None


def reset_redis_client_blocking() -> None:
    """
    Blocking helper to reset the Redis client outside of an event loop.
    """
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        asyncio.run(reset_redis_client())
        return

    raise RuntimeError("reset_redis_client_blocking cannot run inside an active event loop; await reset_redis_client.")


def build_redis_key(*parts: str, tenant_id: str | None = None, user_id: str | None = None) -> str:
    """
    Build a namespaced Redis key with the configured prefix.

    Args:
        parts: Key segments in order of specificity
        tenant_id: Optional tenant identifier to include
        user_id: Optional user identifier to include

    Returns:
        Fully qualified Redis key string
    """
    settings = get_settings()
    segments: list[str] = [settings.redis_key_prefix]

    if tenant_id:
        segments.append(f"tenant:{tenant_id}")
    if user_id:
        segments.append(f"user:{user_id}")

    segments.extend(part for part in parts if part)

    return ":".join(segments)


def ttl_or_default(ttl: Optional[int] = None) -> int:
    """
    Resolve a TTL, falling back to the configured default.

    Args:
        ttl: Optional TTL in seconds

    Returns:
        TTL in seconds
    """
    return ttl if ttl is not None else get_settings().redis_default_ttl_seconds


__all__ = [
    "build_redis_key",
    "close_redis",
    "get_redis",
    "ping_redis",
    "reset_redis_client",
    "reset_redis_client_blocking",
    "ttl_or_default",
]
