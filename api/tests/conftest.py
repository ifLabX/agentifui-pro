"""
Test configuration and fixtures for FastAPI backend tests.

This module provides shared test fixtures and async test configuration.
Database tests use mocks or the actual PostgreSQL 18 database.
"""

import asyncio
import os
import uuid
from collections.abc import AsyncGenerator, Generator
from typing import Any
from unittest.mock import AsyncMock, Mock, patch

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import reset_settings
from core.db import reset_session_factory

# Import application components
from main import app


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """
    Create an instance of the default event loop for the test session.

    This fixture ensures that all async tests run in the same event loop,
    which is important for SQLAlchemy async session management.
    """
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(autouse=True)
def reset_caches() -> Generator[None, None, None]:
    """
    Auto-reset settings and session factory caches between tests.

    This ensures each test starts with clean state and doesn't inherit
    cached settings or database connections from previous tests.
    """
    yield
    # Cleanup after each test
    reset_settings()
    reset_session_factory()


@pytest.fixture
def client() -> TestClient:
    """
    Create a FastAPI test client.

    Returns:
        TestClient instance for making HTTP requests
    """
    return TestClient(app)


@pytest.fixture
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    """
    Create an async HTTP client for testing.

    Yields:
        AsyncClient instance for making async HTTP requests
    """
    from httpx import ASGITransport

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client


@pytest.fixture
def mock_database_health() -> Generator[dict[str, Any], None, None]:
    """
    Mock database health check for testing endpoints without database.

    Returns:
        Mock database health check function
    """
    mock_db_info = {
        "connected": True,
        "version": "PostgreSQL 18.0",
        "database_name": "test_db",
        "connection_count": 5,
        "pool_size": 10,
        "checked_out_connections": 2,
    }

    with patch("core.db.check_database_connection", new_callable=AsyncMock, return_value=True):
        with patch("core.db.get_database_info", new_callable=AsyncMock, return_value=mock_db_info):
            yield mock_db_info


@pytest.fixture
def mock_database_unhealthy() -> Generator[dict[str, Any], None, None]:
    """
    Mock unhealthy database for testing error scenarios.

    Returns:
        Mock unhealthy database state
    """
    mock_db_info = {
        "connected": False,
        "error": "Connection timeout",
    }

    with patch("core.db.check_database_connection", new_callable=AsyncMock, return_value=False):
        with patch("core.db.get_database_info", new_callable=AsyncMock, return_value=mock_db_info):
            yield mock_db_info


@pytest.fixture
def sample_user_data() -> dict[str, Any]:
    """
    Sample user data for testing.

    Returns:
        Dictionary with sample user information
    """
    return {
        "id": uuid.uuid4(),
        "email": "test@example.com",
        "username": "testuser",
        "full_name": "Test User",
        "is_active": True,
        "created_at": "2025-09-23T10:30:00Z",
        "updated_at": "2025-09-23T10:30:00Z",
    }


@pytest.fixture
def sample_error_response() -> dict[str, Any]:
    """
    Sample error response for testing.

    Returns:
        Dictionary with sample error response data
    """
    return {
        "error": "VALIDATION_ERROR",
        "message": "Test validation error",
        "timestamp": "2025-09-23T10:30:00Z",
        "request_id": "550e8400-e29b-41d4-a716-446655440000",
        "detail": "Test error details",
    }


@pytest.fixture
def mock_request_id() -> str:
    """
    Mock request ID for testing.

    Returns:
        Test request ID string
    """
    return "test-request-id-12345"


@pytest.fixture
def mock_environment_production() -> Generator[None, None, None]:
    """
    Mock production environment for testing production-specific behavior.
    """
    with patch.dict(
        os.environ,
        {
            "ENVIRONMENT": "production",
            "DEBUG": "false",
            "LOG_LEVEL": "INFO",
        },
    ):
        yield


@pytest.fixture
def mock_environment_development() -> Generator[None, None, None]:
    """
    Mock development environment for testing development-specific behavior.
    """
    with patch.dict(
        os.environ,
        {
            "ENVIRONMENT": "development",
            "DEBUG": "true",
            "LOG_LEVEL": "DEBUG",
        },
    ):
        yield


@pytest.fixture
def capture_logs(caplog: Any) -> Any:
    """
    Capture logs during testing.

    Args:
        caplog: pytest caplog fixture

    Returns:
        Caplog fixture for log assertions
    """
    return caplog


class MockAsyncContextManager:
    """Mock async context manager for testing."""

    def __init__(self, return_value: Any = None) -> None:
        self.return_value = return_value

    async def __aenter__(self) -> Any:
        return self.return_value

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        pass


@pytest.fixture
def mock_async_session() -> AsyncMock:
    """
    Mock async database session for testing.

    Returns:
        Mock AsyncSession
    """
    session = AsyncMock(spec=AsyncSession)
    session.commit = AsyncMock()
    session.rollback = AsyncMock()
    session.close = AsyncMock()
    session.execute = AsyncMock()
    session.scalar = AsyncMock()
    session.scalars = AsyncMock()

    return session


@pytest.fixture
def mock_database_engine() -> AsyncMock:
    """
    Mock database engine for testing.

    Returns:
        Mock AsyncEngine
    """
    engine = AsyncMock()
    engine.connect = Mock(return_value=MockAsyncContextManager())
    engine.dispose = AsyncMock()

    # Mock pool attributes
    mock_pool = Mock()
    mock_pool.size.return_value = 10
    mock_pool.checkedin.return_value = 8
    mock_pool.checkedout.return_value = 2
    mock_pool.overflow.return_value = 0
    mock_pool.invalidated.return_value = 0

    engine.pool = mock_pool

    return engine


@pytest.fixture
def mock_successful_query_result() -> Mock:
    """
    Mock successful database query result.

    Returns:
        Mock query result
    """
    result = Mock()
    result.scalar.return_value = 1
    result.scalars.return_value = [1, 2, 3]
    result.fetchone.return_value = {"id": 1, "name": "test"}
    result.fetchall.return_value = [{"id": 1, "name": "test"}]

    return result


@pytest.fixture(autouse=True)
def clean_app_state() -> Generator[None, None, None]:
    """
    Clean FastAPI app state between tests.

    This fixture runs automatically and ensures that dependency
    overrides don't leak between tests.
    """
    yield
    app.dependency_overrides.clear()


@pytest.fixture
def temporary_file() -> Generator[str, None, None]:
    """
    Create a temporary file for testing file operations.

    Yields:
        Path to temporary file that gets cleaned up after test
    """
    import tempfile

    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as f:
        temp_path = f.name
        f.write("test content")

    yield temp_path

    # Cleanup
    try:
        os.unlink(temp_path)
    except OSError:
        pass


# Async test utilities
async def async_return(value: Any) -> Any:
    """Helper to return a value from an async function."""
    return value


def async_mock_return(value: Any) -> AsyncMock:
    """Helper to create an AsyncMock that returns a specific value."""
    mock = AsyncMock()
    mock.return_value = value
    return mock


# Test data factories
class TestDataFactory:
    """Factory for creating test data objects."""

    @staticmethod
    def create_health_response(status: str = "healthy", **kwargs: Any) -> dict[str, Any]:
        """Create a health response for testing."""
        default_response: dict[str, Any] = {
            "status": status,
            "timestamp": "2025-09-23T10:30:00Z",
            "version": "0.1.0-test",
        }

        if status == "healthy":
            default_response["uptime_seconds"] = 3600
        else:
            default_response["errors"] = ["Service unavailable"]

        default_response.update(kwargs)
        return default_response

    @staticmethod
    def create_db_health_response(connected: bool = True, **kwargs: Any) -> dict[str, Any]:
        """Create a database health response for testing."""
        default_response: dict[str, Any] = {
            "status": "healthy" if connected else "unhealthy",
            "timestamp": "2025-09-23T10:30:00Z",
            "database_connected": connected,
        }

        if connected:
            default_response.update(
                {
                    "response_time_ms": 15.0,
                    "connection_pool": {"active_connections": 2, "pool_size": 10},
                    "migration_status": "up_to_date",
                }
            )
        else:
            default_response["errors"] = ["Database connection failed"]

        default_response.update(kwargs)
        return default_response


# Make factory available as fixture
@pytest.fixture
def test_data_factory() -> TestDataFactory:
    """Test data factory fixture."""
    return TestDataFactory()


# Performance testing utilities
@pytest.fixture
def performance_timer() -> type:
    """Timer utility for performance testing."""
    import time

    class Timer:
        def __init__(self) -> None:
            self.start_time: float | None = None
            self.end_time: float | None = None

        def start(self) -> None:
            self.start_time = time.time()

        def stop(self) -> None:
            self.end_time = time.time()

        @property
        def elapsed_ms(self) -> float | None:
            if self.start_time and self.end_time:
                return (self.end_time - self.start_time) * 1000
            return None

        def __enter__(self) -> "Timer":
            self.start()
            return self

        def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
            self.stop()

    return Timer
