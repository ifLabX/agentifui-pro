"""
Contract tests for GET /health/redis endpoint.

These tests validate the Redis health endpoint behavior.
"""

from datetime import datetime
from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient
from src.core.config import Settings


def _settings_with_redis() -> Settings:
    """Create settings stub with Redis configured for tests."""
    return Settings(
        database_url="postgresql+asyncpg://user:pass@localhost:5432/test",
        redis_url="redis://localhost:6379/0",
    )


def test_health_redis_endpoint_exists() -> None:
    """Test that /health/redis endpoint exists and is accessible."""
    from src.main import app

    client = TestClient(app)
    with patch("src.api.endpoints.health.ping_redis", new_callable=AsyncMock, return_value=True):
        with patch("src.api.endpoints.health.get_settings", return_value=_settings_with_redis()):
            response = client.get("/health/redis")

    assert response.status_code != 404, "Redis health endpoint /health/redis must exist"


def test_health_redis_endpoint_healthy_response_schema() -> None:
    """Test /health/redis endpoint returns correct schema for healthy Redis."""
    from src.main import app

    client = TestClient(app)
    with patch("src.api.endpoints.health.ping_redis", new_callable=AsyncMock, return_value=True):
        with patch("src.api.endpoints.health.get_settings", return_value=_settings_with_redis()):
            response = client.get("/health/redis")

    # Should return 200 for healthy Redis
    assert response.status_code == 200

    data = response.json()

    # Required fields according to RedisHealthResponse schema
    assert "status" in data
    assert "timestamp" in data
    assert "redis_connected" in data

    # Status should be one of the allowed enum values
    assert data["status"] in ["healthy", "degraded", "unhealthy"]

    # redis_connected should be boolean
    assert isinstance(data["redis_connected"], bool)
    assert data["redis_connected"] is True  # for 200 response

    # Timestamp should be valid ISO 8601 format
    timestamp = data["timestamp"]
    try:
        datetime.fromisoformat(timestamp)
    except ValueError:
        pytest.fail(f"Invalid timestamp format: {timestamp}")


def test_health_redis_endpoint_unhealthy_response_schema() -> None:
    """Test /health/redis endpoint error response format."""
    from src.main import app

    client = TestClient(app)
    with patch("src.api.endpoints.health.ping_redis", new_callable=AsyncMock, return_value=False):
        with patch("src.api.endpoints.health.get_settings", return_value=_settings_with_redis()):
            response = client.get("/health/redis")

    assert response.status_code == 503

    data = response.json()

    assert data["status"] in ["unhealthy", "degraded"]
    assert data["redis_connected"] is False
    assert "errors" in data
    assert isinstance(data["errors"], list)
    for error in data["errors"]:
        assert isinstance(error, str)


def test_health_redis_endpoint_handles_exceptions() -> None:
    """Test /health/redis endpoint handles Redis errors gracefully."""
    from src.main import app

    client = TestClient(app)
    with patch(
        "src.api.endpoints.health.ping_redis",
        new_callable=AsyncMock,
        side_effect=Exception("boom"),
    ):
        with patch("src.api.endpoints.health.get_settings", return_value=_settings_with_redis()):
            response = client.get("/health/redis")

    assert response.status_code == 503
    data = response.json()
    assert "errors" in data
    assert any("boom" in error for error in data["errors"])
