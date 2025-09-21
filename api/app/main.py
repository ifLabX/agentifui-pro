"""
Main FastAPI application factory and configuration.
Entry point for the AgentifUI-Pro backend foundation.
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config.database import close_database_connections
from app.core.config.settings import get_settings
from app.core.exceptions.handlers import add_exception_handlers
from app.core.middleware.security import SecurityHeadersMiddleware, TrustedHostMiddleware

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan events.

    Handles startup and shutdown tasks for the application.
    """
    # Startup
    settings = get_settings()

    # Initialize database connection (lazy initialization)
    from app.core.config.database import get_engine

    get_engine()  # Initialize engine for lazy loading

    # Log startup information
    logger.info("🚀 Starting %s v%s", settings.project_name, settings.project_version)
    logger.info("📊 Debug mode: %s", settings.debug)
    logger.info("🔗 Database: %s://...", settings.database_url.split("://")[0])

    if settings.debug:
        logger.warning("⚠️  DEBUG mode is enabled - do not use in production!")

    yield

    # Shutdown
    logger.info("🛑 Shutting down application...")
    await close_database_connections()
    logger.info("✅ Database connections closed")


def create_application() -> FastAPI:
    """
    Create and configure the FastAPI application.

    Returns:
        Configured FastAPI application instance
    """
    settings = get_settings()

    # Create FastAPI application
    app = FastAPI(
        title=settings.project_name,
        version=settings.project_version,
        description="Enterprise AI platform backend foundation",
        docs_url="/docs" if settings.enable_docs else None,
        redoc_url="/redoc" if settings.enable_redoc else None,
        openapi_url="/openapi.json",
        lifespan=lifespan,
    )

    # Add security middleware (order matters!)
    if settings.enable_security_headers:
        app.add_middleware(SecurityHeadersMiddleware, enable_security_headers=True)

    # Add trusted host validation (disabled in debug mode for testing)
    if not settings.debug:
        app.add_middleware(TrustedHostMiddleware, trusted_hosts=settings.trusted_hosts)

    # Add CORS middleware with security considerations
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=[
            "Accept",
            "Accept-Language",
            "Content-Language",
            "Content-Type",
            "Authorization",
            "X-Requested-With",
        ],  # Restrict headers for security
        max_age=600,  # Cache preflight requests for 10 minutes
    )

    # Include API routes
    app.include_router(api_router, prefix=settings.api_v1_prefix)

    # Add exception handlers
    add_exception_handlers(app)

    return app


# Create the application instance
app = create_application()


if __name__ == "__main__":
    # This is used for development only
    import uvicorn

    settings = get_settings()

    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower(),
    )
