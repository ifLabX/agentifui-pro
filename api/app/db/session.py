"""
Database session management for FastAPI dependency injection.
Provides session lifecycle management for request/response cycle.
"""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config.database import get_async_session


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency for database sessions.

    This dependency provides database sessions for request handlers.
    The session is automatically closed after the request completes.

    Yields:
        AsyncSession: Database session for the request

    Example:
        ```python
        @app.get("/users")
        async def get_users(db: AsyncSession = Depends(get_db_session)):
            result = await db.execute(select(User))
            return result.scalars().all()
        ```
    """
    async for session in get_async_session():
        yield session


# Alias for backward compatibility and convenience
get_db = get_db_session
