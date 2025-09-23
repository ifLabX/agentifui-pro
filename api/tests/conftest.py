"""
Test configuration and fixtures for FastAPI backend tests.

This module provides shared test fixtures, database mocking utilities,
and async test configuration for the test suite.
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
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.pool import StaticPool

from config.settings import Settings, get_settings
from database.session import get_db_session

# Import application components
from main import app
from models.base import Base

# Configure pytest-asyncio (older version compatibility)
# pytest_asyncio.Config.default_fixture_loop_scope = "function"


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


@pytest.fixture
def mock_settings() -> Settings:
    """
    Mock settings for testing with safe defaults.

    Returns:
        Settings object configured for testing environment
    """
    with patch.dict(
        os.environ,
        {
            "APP_NAME": "Test API",
            "APP_VERSION": "0.1.0-test",
            "DEBUG": "true",
            "ENVIRONMENT": "test",
            "DATABASE_URL": "sqlite+aiosqlite:///:memory:",
            "SECRET_KEY": "test-secret-key-minimum-32-characters-long",
            "LOG_LEVEL": "DEBUG",
            "CORS_ORIGINS": '["http://localhost:3000"]',
            "HEALTH_CHECK_TIMEOUT": "1",
            "DATABASE_HEALTH_CHECK_TIMEOUT": "2",
        },
        clear=False,
    ):
        return get_settings()


@pytest.fixture
async def test_engine(mock_settings: Settings) -> AsyncGenerator[AsyncEngine, None]:
    """
    Create a test database engine using SQLite in-memory database.

    Args:
        mock_settings: Test settings fixture

    Yields:
        Async SQLAlchemy engine for testing
    """
    # Create in-memory SQLite database for testing
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        poolclass=StaticPool,
        connect_args={
            "check_same_thread": False,
        },
        echo=mock_settings.debug,
    )

    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    # Cleanup
    await engine.dispose()


@pytest.fixture
async def test_session(test_engine: AsyncEngine) -> AsyncGenerator[AsyncSession, None]:
    """
    Create a test database session.

    Args:
        test_engine: Test database engine

    Yields:
        Async SQLAlchemy session for testing
    """
    async with AsyncSession(test_engine, expire_on_commit=False) as session:
        yield session


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
def override_get_db_session(test_session: AsyncSession):
    """
    Override the database session dependency for testing.

    Args:
        test_session: Test database session

    Returns:
        Dependency override function
    """

    async def _override_get_db_session():
        yield test_session

    return _override_get_db_session


@pytest.fixture
def client_with_db(client: TestClient, override_get_db_session) -> TestClient:
    """
    Create a test client with database session override.

    Args:
        client: FastAPI test client
        override_get_db_session: Database session override

    Returns:
        TestClient with mocked database session
    """
    app.dependency_overrides[get_db_session] = override_get_db_session
    yield client
    app.dependency_overrides.clear()


@pytest.fixture
async def async_client_with_db(async_client: AsyncClient, override_get_db_session) -> AsyncGenerator[AsyncClient, None]:
    """
    Create an async client with database session override.

    Args:
        async_client: Async HTTP client
        override_get_db_session: Database session override

    Yields:
        AsyncClient with mocked database session
    """
    app.dependency_overrides[get_db_session] = override_get_db_session
    yield async_client
    app.dependency_overrides.clear()


@pytest.fixture
def mock_database_health():
    """
    Mock database health check for testing endpoints without database.

    Returns:
        Mock database health check function
    """
    mock_health = {
        "connected": True,
        "response_time_ms": 10.5,
        "connection_pool": {
            "pool_size": 10,
            "active_connections": 2,
            "checked_out_connections": 0,
            "overflow_connections": 0,
            "invalid_connections": 0,
        },
        "database_info": {"version": "PostgreSQL 14.0", "driver": "asyncpg"},
        "errors": [],
    }

    with patch("database.health.check_database_health", return_value=mock_health):
        with patch("database.health.check_database_connectivity", return_value=True):
            yield mock_health


@pytest.fixture
def mock_database_unhealthy():
    """
    Mock unhealthy database for testing error scenarios.

    Returns:
        Mock unhealthy database state
    """
    mock_health = {
        "connected": False,
        "response_time_ms": None,
        "connection_pool": None,
        "database_info": None,
        "errors": ["Connection timeout", "Database unreachable"],
    }

    with patch("database.health.check_database_health", return_value=mock_health):
        with patch("database.health.check_database_connectivity", return_value=False):
            yield mock_health


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
def mock_environment_production():
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
def mock_environment_development():
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
def capture_logs(caplog):
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

    def __init__(self, return_value=None):
        self.return_value = return_value

    async def __aenter__(self):
        return self.return_value

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass


@pytest.fixture
def mock_async_session():
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
def mock_database_engine():
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
def mock_successful_query_result():
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
def clean_app_state():
    """
    Clean FastAPI app state between tests.

    This fixture runs automatically and ensures that dependency
    overrides don't leak between tests.
    """
    yield
    app.dependency_overrides.clear()


@pytest.fixture
def temporary_file():
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
async def async_return(value):
    """Helper to return a value from an async function."""
    return value


def async_mock_return(value):
    """Helper to create an AsyncMock that returns a specific value."""
    mock = AsyncMock()
    mock.return_value = value
    return mock


# Test data factories
class TestDataFactory:
    """Factory for creating test data objects."""

    @staticmethod
    def create_health_response(status: str = "healthy", **kwargs) -> dict[str, Any]:
        """Create a health response for testing."""
        default_response = {
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
    def create_db_health_response(connected: bool = True, **kwargs) -> dict[str, Any]:
        """Create a database health response for testing."""
        default_response = {
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
def performance_timer():
    """Timer utility for performance testing."""
    import time

    class Timer:
        def __init__(self):
            self.start_time = None
            self.end_time = None

        def start(self):
            self.start_time = time.time()

        def stop(self):
            self.end_time = time.time()

        @property
        def elapsed_ms(self):
            if self.start_time and self.end_time:
                return (self.end_time - self.start_time) * 1000
            return None

        def __enter__(self):
            self.start()
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            self.stop()

    return Timer
