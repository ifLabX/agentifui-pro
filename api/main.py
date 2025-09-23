"""
FastAPI application entry point.

This module sets up the FastAPI application with middleware, routers,
and dependency injection for the Agentifui Pro API.
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config.settings import get_settings
from database.connection import dispose_engine
from health.endpoints import router as health_router
from middleware.error_handler import setup_error_handling


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.

    Handles startup and shutdown events for proper resource management.
    """
    # Startup
    yield
    # Shutdown
    await dispose_engine()


def create_app() -> FastAPI:
    """
    Create FastAPI application with deferred settings loading.

    This factory function ensures settings are only loaded when the app
    is actually created, preventing import-time configuration errors.

    Returns:
        FastAPI: Configured application instance
    """
    # Load settings only when creating the app
    settings = get_settings()

    # Create FastAPI application with lifespan management
    app = FastAPI(
        title=settings.app_name,
        description=settings.app_description,
        version=settings.app_version,
        docs_url="/docs" if settings.enable_docs else None,
        redoc_url="/redoc" if settings.enable_redoc else None,
        lifespan=lifespan,
    )

    # CORS middleware with settings-based configuration
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=settings.cors_allow_credentials,
        allow_methods=settings.cors_allow_methods,
        allow_headers=settings.cors_allow_headers,
    )

    # Setup error handling middleware
    setup_error_handling(app)

    # Include routers
    app.include_router(health_router)

    return app


# Create application instance
app = create_app()


@app.get("/")
async def root():
    """Root endpoint returning basic API information."""
    settings = get_settings()
    return {
        "message": f"{settings.app_name} is running",
        "version": settings.app_version,
        "environment": settings.environment,
    }
