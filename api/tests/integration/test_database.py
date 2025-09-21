"""
Integration tests for database connection functionality.
Tests the database configuration and connection management.
"""

import pytest
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.asyncio
async def test_database_connection_can_be_established():
    """Test that database connection can be established."""
    # This will fail until we implement database configuration
    from app.core.config.database import create_engine, get_database_url

    database_url = get_database_url()
    assert database_url is not None
    assert isinstance(database_url, str)

    # Test engine creation
    engine = create_engine(database_url)
    assert engine is not None


@pytest.mark.asyncio
async def test_database_session_creation():
    """Test that database sessions can be created and closed."""
    # This will fail until we implement session management
    from app.db.session import get_async_session

    async with get_async_session() as session:
        assert isinstance(session, AsyncSession)
        assert not session.is_active  # Session should not be in transaction initially


@pytest.mark.asyncio
async def test_database_session_dependency():
    """Test database session dependency injection."""
    # This will fail until we implement dependency injection
    from app.db.session import get_db_session

    session_gen = get_db_session()
    session = await anext(session_gen)

    try:
        assert isinstance(session, AsyncSession)
    finally:
        # Cleanup session
        try:
            await anext(session_gen)
        except StopAsyncIteration:
            pass  # Expected when generator finishes


@pytest.mark.asyncio
async def test_database_connection_with_invalid_url():
    """Test handling of invalid database URLs."""
    # This will fail until we implement error handling
    from app.core.config.database import create_engine

    invalid_url = "invalid://not-a-real-url"

    # Should raise a ValueError for invalid URL format
    with pytest.raises(ValueError, match="database_url scheme must be"):
        create_engine(invalid_url)


@pytest.mark.asyncio
async def test_database_connection_health_check():
    """Test database health check functionality."""
    # This will fail until we implement health check
    from app.core.config.database import check_database_health

    is_healthy = await check_database_health()
    assert isinstance(is_healthy, bool)


@pytest.mark.asyncio
async def test_database_connection_pooling():
    """Test that connection pooling is properly configured."""
    # This will fail until we implement connection pooling
    from app.core.config.database import get_engine

    engine = get_engine()

    # Check pool configuration
    pool = engine.pool
    assert pool is not None
    assert pool.size() > 0  # Should have pool size configured
