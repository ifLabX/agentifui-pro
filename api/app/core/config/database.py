"""
Database configuration and connection management.
Handles SQLAlchemy 2.0 async engine and session configuration.
"""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import StaticPool

from app.core.config.settings import get_settings


class DatabaseConfig:
    """Database configuration and connection management."""

    def __init__(self) -> None:
        """Initialize database configuration."""
        self.settings = get_settings()
        self._engine: AsyncEngine | None = None
        self._session_factory: async_sessionmaker[AsyncSession] | None = None

    @property
    def engine(self) -> AsyncEngine:
        """Get or create the database engine."""
        if self._engine is None:
            self._engine = self._create_engine()
        return self._engine

    @property
    def session_factory(self) -> async_sessionmaker[AsyncSession]:
        """Get or create the session factory."""
        if self._session_factory is None:
            self._session_factory = async_sessionmaker(
                bind=self.engine,
                class_=AsyncSession,
                expire_on_commit=False,
                autoflush=True,
                autocommit=False,
            )
        return self._session_factory

    def _create_engine(self) -> AsyncEngine:
        """Create the SQLAlchemy async engine."""
        db_config = self.settings.get_database_config()
        url = db_config.pop("url")

        # Special configuration for SQLite
        if "sqlite" in url:
            db_config.update(
                {
                    "poolclass": StaticPool,
                    "connect_args": {
                        "check_same_thread": False,
                    },
                }
            )
            # Remove PostgreSQL-specific config for SQLite
            db_config.pop("pool_size", None)
            db_config.pop("max_overflow", None)
            db_config.pop("pool_timeout", None)
            db_config.pop("pool_recycle", None)
            db_config.pop("pool_pre_ping", None)

        return create_async_engine(url, **db_config)

    async def close(self) -> None:
        """Close the database engine and connections."""
        if self._engine is not None:
            await self._engine.dispose()
            self._engine = None
            self._session_factory = None


# Global database configuration instance
_db_config: DatabaseConfig | None = None


def get_database_config() -> DatabaseConfig:
    """Get the global database configuration instance."""
    global _db_config
    if _db_config is None:
        _db_config = DatabaseConfig()
    return _db_config


def get_engine() -> AsyncEngine:
    """Get the database engine."""
    return get_database_config().engine


def get_session_factory() -> async_sessionmaker[AsyncSession]:
    """Get the session factory."""
    return get_database_config().session_factory


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Get an async database session.

    Use this for manual session management in services.
    """
    session_factory = get_session_factory()
    async with session_factory() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency injection for database sessions.

    Use this as a FastAPI dependency to get database sessions.
    """
    async for session in get_async_session():
        yield session


async def check_database_health() -> bool:
    """
    Check database connectivity for health checks.

    Returns True if database is accessible, False otherwise.
    """
    try:
        engine = get_engine()
        async with engine.begin() as conn:
            # Simple query to test connectivity
            await conn.execute("SELECT 1")
        return True
    except Exception:
        return False


def get_database_url() -> str:
    """Get the configured database URL."""
    return get_settings().database_url


def create_engine(database_url: str) -> AsyncEngine:
    """
    Create an async engine with the given database URL.

    Used for testing and custom configurations.
    """
    if "sqlite" in database_url:
        return create_async_engine(
            database_url,
            poolclass=StaticPool,
            connect_args={"check_same_thread": False},
            echo=get_settings().debug,
        )
    else:
        return create_async_engine(
            database_url,
            pool_size=20,
            max_overflow=30,
            pool_timeout=30,
            pool_recycle=1800,
            pool_pre_ping=True,
            echo=get_settings().debug,
        )


async def close_database_connections() -> None:
    """Close all database connections."""
    db_config = get_database_config()
    await db_config.close()
