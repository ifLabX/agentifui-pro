"""
Session dependency injection for FastAPI.

This module provides async session management with dependency injection
for FastAPI endpoints following session-per-request pattern.
"""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from database.connection import get_async_engine


# Create session factory
def get_session_factory() -> async_sessionmaker[AsyncSession]:
    """
    Get async session factory.

    Creates a session factory bound to the async engine with proper
    configuration for request-scoped sessions.

    Returns:
        async_sessionmaker: Session factory for creating async sessions
    """
    engine = get_async_engine()

    return async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,  # Keep objects usable after commit
        autoflush=True,  # Auto-flush changes before queries
        autocommit=False,  # Explicit transaction control
    )


# Global session factory instance
SessionLocal = get_session_factory()


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency for getting database session.

    Provides an async database session for each request with proper
    lifecycle management including automatic rollback on errors.

    Yields:
        AsyncSession: Database session for the request

    Example:
        @app.get("/users/")
        async def get_users(db: AsyncSession = Depends(get_db_session)):
            result = await db.execute(select(User))
            return result.scalars().all()
    """
    async with SessionLocal() as session:
        try:
            yield session
            # Commit is handled explicitly by the endpoint if needed
        except Exception:
            # Rollback on any exception
            await session.rollback()
            raise
        finally:
            # Session is automatically closed by context manager
            pass


async def get_db_session_for_testing() -> AsyncGenerator[AsyncSession, None]:
    """
    Get database session for testing with transaction rollback.

    Each test gets a session within a transaction that is rolled back
    at the end, ensuring test isolation.

    Yields:
        AsyncSession: Database session for testing
    """
    from database.connection import get_async_engine_for_testing

    engine = get_async_engine_for_testing()
    session_factory = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with session_factory() as session:
        # Start a transaction
        transaction = await session.begin()
        try:
            yield session
        finally:
            # Always rollback in tests
            await transaction.rollback()


async def create_all_tables() -> None:
    """
    Create all database tables.

    This function should be called during application startup
    if auto-creation of tables is desired.

    Note: In production, use Alembic migrations instead.
    """

    engine = get_async_engine()

    # Import all models here to ensure they are registered
    # This will be updated when models are implemented

    async with engine.begin() as conn:
        # Create all tables defined in metadata
        # await conn.run_sync(MetaData().create_all)
        pass  # Tables will be created via Alembic migrations


async def drop_all_tables() -> None:
    """
    Drop all database tables.

    This function is useful for testing cleanup.
    Should NEVER be called in production.
    """

    engine = get_async_engine()

    async with engine.begin() as conn:
        # Drop all tables
        # await conn.run_sync(MetaData().drop_all)
        pass  # Tables will be managed via Alembic migrations
