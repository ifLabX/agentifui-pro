"""
Database connection factory with async engine.

This module provides async SQLAlchemy engine configuration and connection management
for PostgreSQL using asyncpg driver.
"""

from typing import Optional

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy.pool import NullPool

from config.settings import get_settings

# Global engine instance
_engine: Optional[AsyncEngine] = None


def get_async_engine() -> AsyncEngine:
    """
    Get or create async SQLAlchemy engine.

    Creates a singleton async engine instance with connection pooling
    configured for optimal performance and resource usage.

    Returns:
        AsyncEngine: Configured async SQLAlchemy engine
    """
    global _engine

    if _engine is None:
        settings = get_settings()

        # Create async engine with connection pooling
        _engine = create_async_engine(
            settings.database_url,
            # Connection pool configuration
            pool_size=settings.database_pool_size,
            max_overflow=settings.database_pool_max_overflow,
            pool_timeout=settings.database_pool_timeout,
            pool_recycle=settings.database_pool_recycle,
            # Async configuration
            echo=settings.debug,  # Log SQL queries in debug mode
            future=True,  # Use SQLAlchemy 2.0 style
            # Connection arguments for asyncpg
            connect_args={
                "server_settings": {
                    "application_name": settings.app_name,
                }
            },
        )

    return _engine


async def dispose_engine() -> None:
    """
    Dispose of the global engine instance.

    This should be called during application shutdown to properly
    close all database connections.
    """
    global _engine

    if _engine is not None:
        await _engine.dispose()
        _engine = None


def get_async_engine_for_testing() -> AsyncEngine:
    """
    Get async engine configured for testing.

    Uses NullPool to avoid connection sharing issues in tests.
    Each test gets a fresh connection.

    Returns:
        AsyncEngine: Engine configured for testing
    """
    settings = get_settings()

    return create_async_engine(
        settings.database_url,
        poolclass=NullPool,  # No connection pooling for tests
        echo=False,  # Disable SQL logging in tests
        future=True,
    )


async def check_database_connection() -> bool:
    """
    Check if database connection is working.

    Attempts to execute a simple query to verify connectivity.

    Returns:
        bool: True if connection is working, False otherwise
    """
    try:
        engine = get_async_engine()
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        return True
    except Exception:
        return False


async def get_database_info() -> dict:
    """
    Get database information and connection status.

    Returns:
        dict: Database information including version, connection status, etc.
    """
    try:
        engine = get_async_engine()
        async with engine.connect() as conn:
            # Get PostgreSQL version
            result = await conn.execute(text("SELECT version()"))
            version = result.scalar()

            # Get current database name
            result = await conn.execute(text("SELECT current_database()"))
            database_name = result.scalar()

            # Get connection count
            result = await conn.execute(
                text("SELECT count(*) FROM pg_stat_activity WHERE datname = current_database()")
            )
            connection_count = result.scalar()

            return {
                "connected": True,
                "version": version,
                "database_name": database_name,
                "connection_count": connection_count,
                "pool_size": engine.pool.size() if engine.pool else None,
                "checked_out_connections": (engine.pool.checkedout() if engine.pool else None),
            }
    except Exception as e:
        return {
            "connected": False,
            "error": str(e),
        }
