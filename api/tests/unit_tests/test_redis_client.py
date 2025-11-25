"""
Unit tests for Redis client utilities.
"""

import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from src.core.config import Settings
from src.core.redis import (
    build_redis_key,
    close_redis,
    get_redis,
    ping_redis,
    reset_redis_client,
    ttl_or_default,
)


def _settings(redis_url: str = "redis://localhost:6379/0", **overrides: object) -> Settings:
    """Helper to create a Settings instance for Redis tests."""
    return Settings(
        database_url="postgresql+asyncpg://user:pass@localhost:5432/test",
        redis_url=redis_url,
        **overrides,
    )


@pytest.fixture(autouse=True)
def reset_client() -> None:
    """Ensure Redis client cache is cleared before and after each test."""
    reset_redis_client()
    yield
    reset_redis_client()


def test_build_redis_key_includes_prefix_and_scopes() -> None:
    settings = _settings(redis_key_prefix="prefix")
    with patch("src.core.redis.get_settings", return_value=settings):
        key = build_redis_key("session", tenant_id="t1", user_id="u1")
    assert key == "prefix:tenant:t1:user:u1:session"


def test_ttl_or_default_uses_configured_default() -> None:
    settings = _settings(redis_default_ttl_seconds=120)
    with patch("src.core.redis.get_settings", return_value=settings):
        assert ttl_or_default() == 120
        assert ttl_or_default(30) == 30


@pytest.mark.asyncio
async def test_get_redis_reuses_singleton_and_closes_pool() -> None:
    settings = _settings()
    mock_client = AsyncMock()
    mock_client.connection_pool = MagicMock()
    mock_client.aclose = AsyncMock()
    mock_client_recreated = AsyncMock()
    mock_client_recreated.connection_pool = MagicMock()
    mock_client_recreated.aclose = AsyncMock()

    with (
        patch("src.core.redis.get_settings", return_value=settings),
        patch("src.core.redis.redis.from_url", side_effect=[mock_client, mock_client_recreated]),
    ):
        first = get_redis()
        second = get_redis()
        assert first is second

        await close_redis()
        mock_client.aclose.assert_awaited()
        mock_client.connection_pool.disconnect.assert_called_with(inuse_connections=True)

        # Recreate after close
        third = get_redis()
        assert third is mock_client_recreated


@pytest.mark.asyncio
async def test_reset_redis_client_disconnects_pool() -> None:
    settings = _settings()
    mock_client = AsyncMock()
    mock_client.connection_pool = MagicMock()
    mock_client.aclose = AsyncMock()

    with (
        patch("src.core.redis.get_settings", return_value=settings),
        patch("src.core.redis.redis.from_url", return_value=mock_client),
    ):
        _ = get_redis()
        reset_redis_client()
        mock_client.connection_pool.disconnect.assert_called_with(inuse_connections=True)


@pytest.mark.asyncio
async def test_ping_redis_respects_timeout() -> None:
    mock_client = AsyncMock()
    mock_client.ping = AsyncMock(return_value=True)

    with patch("src.core.redis.get_redis", return_value=mock_client):
        assert await ping_redis(timeout_seconds=0.1) is True
        mock_client.ping.assert_awaited()


@pytest.mark.asyncio
async def test_ping_redis_handles_timeout() -> None:
    mock_client = AsyncMock()
    mock_client.ping = AsyncMock(side_effect=asyncio.TimeoutError)

    with patch("src.core.redis.get_redis", return_value=mock_client):
        assert await ping_redis(timeout_seconds=0.01) is False
