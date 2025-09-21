"""
Integration tests for application startup and initialization.
Tests the complete application lifecycle and configuration loading.
"""

from fastapi import FastAPI
from fastapi.testclient import TestClient


def test_fastapi_application_can_be_created():
    """Test that FastAPI application instance can be created."""
    # This will fail until we implement the main app
    from app.main import app

    assert isinstance(app, FastAPI)
    assert app.title is not None


def test_application_configuration_loading():
    """Test that application configuration is loaded correctly."""
    # This will fail until we implement configuration
    from app.core.config.settings import get_settings

    settings = get_settings()

    # Check that essential configuration is loaded
    assert settings.project_name is not None
    assert settings.project_version is not None
    assert settings.database_url is not None


def test_application_startup_event():
    """Test application startup event handling."""
    # This will fail until we implement startup events
    from app.main import app

    # Application should have startup event handlers
    assert len(app.router.on_startup) > 0


def test_application_shutdown_event():
    """Test application shutdown event handling."""
    # This will fail until we implement shutdown events
    from app.main import app

    # Application should have shutdown event handlers for cleanup
    assert len(app.router.on_shutdown) > 0


def test_application_middleware_configuration():
    """Test that middleware is properly configured."""
    # This will fail until we implement middleware
    from app.main import app

    # Check that CORS middleware is configured
    middleware_types = [type(middleware.cls) for middleware in app.user_middleware]
    middleware_names = [str(middleware_type) for middleware_type in middleware_types]

    # Should have CORS middleware for frontend integration
    assert any("CORS" in name for name in middleware_names)


def test_application_routes_registration():
    """Test that routes are properly registered."""
    # This will fail until we implement routes
    from app.main import app

    routes = [route.path for route in app.routes]

    # Check that essential routes are registered
    assert "/health" in routes
    assert "/health/ready" in routes
    assert "/info" in routes


def test_application_exception_handlers():
    """Test that exception handlers are configured."""
    # This will fail until we implement exception handlers
    from app.main import app

    # Should have custom exception handlers
    assert len(app.exception_handlers) > 0


def test_application_openapi_documentation():
    """Test that OpenAPI documentation is accessible."""
    # This will fail until we implement the main app
    from app.main import app

    client = TestClient(app)

    # OpenAPI schema should be accessible
    response = client.get("/openapi.json")
    assert response.status_code == 200

    schema = response.json()
    assert "openapi" in schema
    assert "info" in schema
    assert schema["info"]["title"] is not None


def test_application_development_mode_features():
    """Test development mode specific features."""
    # This will fail until we implement configuration
    from app.core.config.settings import get_settings

    settings = get_settings()

    if settings.debug:
        from app.main import app

        client = TestClient(app)

        # Docs should be available in development mode
        docs_response = client.get("/docs")
        assert docs_response.status_code == 200

        redoc_response = client.get("/redoc")
        assert redoc_response.status_code == 200
