"""
Integration tests for complete application startup sequence.

These tests validate that the entire application can start successfully,
all components are properly initialized, and the system is ready to serve requests.
"""

import os
import time
from unittest.mock import AsyncMock, patch

import httpx
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient


def test_application_can_be_imported():
    """Test that the main application can be imported without errors."""
    try:
        from main import app

        assert isinstance(app, FastAPI)
        assert app is not None
    except ImportError as e:
        pytest.fail(f"Failed to import main application: {e}")
    except Exception as e:
        pytest.fail(f"Error during application import: {e}")


def test_application_basic_configuration():
    """Test that application has basic configuration set up correctly."""
    from configs.settings import get_settings
    from main import app

    settings = get_settings()

    # Verify app configuration
    assert app.title == settings.app_name
    assert app.version == settings.app_version

    # Verify essential middleware is configured
    assert len(app.middleware_stack.middleware) > 0

    # Verify routes are registered
    assert len(app.routes) > 0


def test_settings_configuration_startup():
    """Test that settings can be loaded during startup."""
    from configs.settings import get_settings

    # Should be able to get settings without errors
    settings = get_settings()

    # Verify required settings are present
    assert settings.app_name is not None
    assert settings.app_version is not None
    assert settings.database_url is not None
    assert settings.secret_key is not None


def test_database_components_initialization():
    """Test that database components can be initialized."""
    try:
        from database.connection import get_async_engine
        from database.session import get_db_session

        # Should be able to create engine
        engine = get_async_engine()
        assert engine is not None

        # Should be able to get session dependency function
        session_dep = get_db_session()
        assert callable(session_dep.__anext__)

    except Exception as e:
        pytest.fail(f"Database component initialization failed: {e}")


def test_health_endpoints_registration():
    """Test that health endpoints are properly registered during startup."""
    from main import app

    client = TestClient(app)

    # Test that health endpoints exist
    health_response = client.get("/health")
    assert health_response.status_code == 200

    # Test that database health endpoint exists
    db_health_response = client.get("/health/db")
    # Accept both 200 (connected) and 503 (not connected) as valid startup states
    assert db_health_response.status_code in [200, 503]


def test_error_handling_middleware_startup():
    """Test that error handling middleware is properly configured during startup."""
    from main import app

    client = TestClient(app)

    # Test that error handling works
    response = client.get("/nonexistent-endpoint")
    assert response.status_code == 404

    # Should return structured error response
    error_data = response.json()
    assert isinstance(error_data, dict)
    assert "detail" in error_data or "error" in error_data


def test_cors_middleware_startup():
    """Test that CORS middleware is configured during startup."""
    from main import app

    client = TestClient(app)

    # Test CORS preflight request
    headers = {
        "Origin": "http://localhost:3000",
        "Access-Control-Request-Method": "GET",
        "Access-Control-Request-Headers": "Content-Type",
    }

    response = client.options("/health", headers=headers)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_async_application_startup():
    """Test that application starts correctly in async context."""
    from main import app

    # Test async client startup
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/health")
        assert response.status_code == 200

        health_data = response.json()
        assert health_data["status"] == "healthy"


def test_dependency_injection_startup():
    """Test that dependency injection works during startup."""
    from main import app

    # Verify that dependency is registered
    client = TestClient(app)

    # Database-dependent endpoints should work (may fail due to no DB, but shouldn't crash)
    response = client.get("/health/db")
    assert response.status_code in [200, 503]  # Both are valid during startup


@pytest.mark.asyncio
async def test_database_connection_during_startup():
    """Test database connection behavior during startup."""
    with patch("database.connection.get_async_engine") as mock_get_engine:
        mock_engine = AsyncMock()
        mock_get_engine.return_value = mock_engine

        # Should be able to get engine during startup
        from database.connection import get_async_engine

        engine = get_async_engine()

        assert engine is not None
        mock_get_engine.assert_called()


def test_logging_configuration_startup():
    """Test that logging is configured during startup."""
    import logging

    from configs.settings import get_settings

    settings = get_settings()

    # Should be able to get loggers
    logger = logging.getLogger("test")
    assert logger is not None

    # Log level should be configurable
    assert hasattr(settings, "log_level")


def test_startup_performance():
    """Test that application startup is reasonably fast."""
    start_time = time.time()

    # Import and create client (simulates startup)
    from main import app

    client = TestClient(app)

    # Make first request (triggers any lazy initialization)
    response = client.get("/health")

    end_time = time.time()
    startup_time = end_time - start_time

    assert response.status_code == 200
    # Startup should be reasonable (under 5 seconds for tests)
    assert startup_time < 5.0, f"Startup took {startup_time:.2f}s, should be <5s"


def test_environment_variable_handling_startup():
    """Test that environment variables are handled correctly during startup."""
    test_env = {
        "APP_NAME": "Test Startup App",
        "APP_VERSION": "0.1.0-startup-test",
        "DEBUG": "true",
        "ENVIRONMENT": "test",
        "DATABASE_URL": "postgresql+asyncpg://test:test@localhost:5432/test",
        "SECRET_KEY": "test-secret-key-for-startup-testing-32-chars",
        "LOG_LEVEL": "DEBUG",
    }

    with patch.dict(os.environ, test_env, clear=False):
        from configs.settings import get_settings

        settings = get_settings()

        # Settings should reflect environment variables
        assert settings.app_name == "Test Startup App"
        assert settings.app_version == "0.1.0-startup-test"
        assert settings.debug is True
        assert settings.environment == "test"
        assert settings.log_level == "DEBUG"


def test_middleware_stack_startup():
    """Test that middleware stack is properly configured during startup."""
    from main import app

    # Check that middleware is configured
    assert hasattr(app, "middleware_stack")
    assert app.middleware_stack is not None

    # Should have at least CORS and error handling middleware
    middleware_count = len(app.middleware_stack.middleware)
    assert middleware_count > 0, "No middleware configured"


def test_route_registration_startup():
    """Test that all expected routes are registered during startup."""
    from main import app

    # Get all registered routes
    routes = []
    for route in app.routes:
        if hasattr(route, "path"):
            routes.append(route.path)

    # Should have essential routes
    expected_routes = ["/health", "/health/db"]

    for expected_route in expected_routes:
        assert expected_route in routes, f"Route {expected_route} not registered"


def test_openapi_schema_generation_startup():
    """Test that OpenAPI schema can be generated during startup."""
    from main import app

    client = TestClient(app)

    # Should be able to get OpenAPI schema
    response = client.get("/openapi.json")
    assert response.status_code == 200

    schema = response.json()
    assert "openapi" in schema
    assert "info" in schema
    assert "paths" in schema

    # Should have health endpoints in schema
    assert "/health" in schema["paths"]
    assert "/health/db" in schema["paths"]


@pytest.mark.asyncio
async def test_graceful_shutdown_capability():
    """Test that application can handle shutdown gracefully."""
    from database.connection import get_async_engine

    with patch("database.connection.get_async_engine") as mock_get_engine:
        mock_engine = AsyncMock()
        mock_engine.dispose = AsyncMock()
        mock_get_engine.return_value = mock_engine

        # Get engine
        engine = get_async_engine()

        # Should be able to dispose cleanly
        await engine.dispose()
        mock_engine.dispose.assert_called_once()


def test_production_configuration_validation():
    """Test that production configuration is properly validated during startup."""
    production_env = {
        "ENVIRONMENT": "production",
        "DEBUG": "false",
        "SECRET_KEY": "production-secret-key-minimum-32-characters-long-secure",
        "DATABASE_URL": "postgresql+asyncpg://user:pass@db.example.com:5432/prod",
        "LOG_LEVEL": "INFO",
    }

    with patch.dict(os.environ, production_env, clear=False):
        from configs.settings import get_settings

        settings = get_settings()

        # Production settings should be validated
        assert settings.environment == "production"
        assert settings.debug is False
        assert len(settings.secret_key) >= 32
        assert settings.log_level == "INFO"


def test_development_configuration_startup():
    """Test that development configuration works during startup."""
    dev_env = {
        "ENVIRONMENT": "development",
        "DEBUG": "true",
        "SECRET_KEY": "development-secret-key-minimum-32-chars",
        "DATABASE_URL": "postgresql+asyncpg://dev:dev@localhost:5432/dev",
        "LOG_LEVEL": "DEBUG",
    }

    with patch.dict(os.environ, dev_env, clear=False):
        from configs.settings import get_settings

        settings = get_settings()

        # Development settings should work
        assert settings.environment == "development"
        assert settings.debug is True
        assert settings.log_level == "DEBUG"


def test_startup_with_missing_optional_config():
    """Test that startup works even with missing optional configuration."""
    minimal_env = {
        "DATABASE_URL": "postgresql+asyncpg://user:pass@localhost:5432/test",
        "SECRET_KEY": "test-secret-key-minimum-32-characters",
    }

    with patch.dict(os.environ, minimal_env, clear=True):
        from configs.settings import get_settings

        # Should still work with minimal configuration
        settings = get_settings()

        assert settings.database_url is not None
        assert settings.secret_key is not None
        # Optional fields should have defaults
        assert settings.app_name is not None
        assert settings.app_version is not None


def test_concurrent_startup_requests():
    """Test that application can handle concurrent requests during startup."""
    from main import app

    def make_request():
        client = TestClient(app)
        return client.get("/health")

    # Make multiple concurrent requests
    from concurrent.futures import ThreadPoolExecutor

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(make_request) for _ in range(5)]
        responses = [future.result() for future in futures]

    # All requests should succeed
    for response in responses:
        assert response.status_code == 200

    # All should return valid health data
    for response in responses:
        data = response.json()
        assert data["status"] == "healthy"


def test_startup_error_recovery():
    """Test that startup can recover from transient errors."""
    from main import app

    # Even if some components fail during startup, basic app should work
    client = TestClient(app)

    # Basic health check should always work
    response = client.get("/health")
    assert response.status_code == 200

    # App should be functional for basic operations
    assert app.title is not None
    assert app.version is not None
