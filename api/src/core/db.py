"""
Database connection and session management.

This module provides async SQLAlchemy engine configuration, connection management,
and session dependency injection for FastAPI using PostgreSQL with asyncpg driver.
It also enforces multi-tenant and soft-delete policies at the ORM layer.
"""

from collections.abc import AsyncGenerator
from typing import Any, Optional

from sqlalchemy import event, text
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import Mapper, Session, with_loader_criteria
from sqlalchemy.pool import NullPool
from src.core.config import get_settings
from src.core.context import get_request_context
from src.core.exceptions import TenantContextError
from src.models.base import Base, SoftDeleteMixin, TenantAwareMixin, VersionedAuditMixin

# Global engine and session factory instances
_engine: Optional[AsyncEngine] = None
_session_local: Optional[async_sessionmaker[AsyncSession]] = None


# ============================================================================
# Engine Management
# ============================================================================


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


def reset_engine() -> None:
    """
    Reset the global engine instance without disposing.

    Use this in tests when switching database connections.
    The engine will be recreated on next get_async_engine() call.

    For proper cleanup (e.g., shutdown), use dispose_engine() instead.
    """
    global _engine
    _engine = None


async def dispose_engine() -> None:
    """
    Dispose of the global engine instance and close all connections.

    This should be called during application shutdown to properly
    close all database connections and clean up resources.
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


async def get_database_info() -> dict[str, Any]:
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

            pool_size = None
            checked_out = None
            if engine.pool:
                pool_size = engine.pool.size() if hasattr(engine.pool, "size") else None
                checked_out = engine.pool.checkedout() if hasattr(engine.pool, "checkedout") else None

            return {
                "connected": True,
                "version": version,
                "database_name": database_name,
                "connection_count": connection_count,
                "pool_size": pool_size,
                "checked_out_connections": checked_out,
            }
    except Exception as e:
        return {
            "connected": False,
            "error": str(e),
        }


# ============================================================================
# Session Management
# ============================================================================


def get_session_factory() -> async_sessionmaker[AsyncSession]:
    """
    Get or create async session factory.

    Creates a session factory bound to the async engine with proper
    configuration for request-scoped sessions. Uses lazy initialization
    to allow settings changes in tests.

    Returns:
        async_sessionmaker: Session factory for creating async sessions
    """
    global _session_local

    if _session_local is None:
        engine = get_async_engine()
        _session_local = async_sessionmaker(
            engine,
            class_=AsyncSession,
            expire_on_commit=False,  # Keep objects usable after commit
            autoflush=True,  # Auto-flush changes before queries
            autocommit=False,  # Explicit transaction control
        )

    return _session_local


def reset_session_factory() -> None:
    """
    Reset session factory and engine for testing or configuration reload.

    This resets both the session factory and the underlying engine,
    ensuring that the next session will use a fresh engine with
    new settings (e.g., after calling reset_settings()).

    Use this in tests when switching database connections.
    Must be called after reset_settings() from config module.

    Example:
        >>> from core.config import reset_settings
        >>> from core.db import reset_session_factory
        >>> reset_settings()  # Clear settings cache first
        >>> reset_session_factory()  # Reset both factory and engine
    """
    global _session_local
    _session_local = None
    reset_engine()  # Also reset the cached engine


def _collect_tenant_selectables() -> set[Any]:
    """
    Gather all mapped selectables associated with tenant-aware entities.
    """
    selectables: set[Any] = set()
    tenant_mappers: list[Mapper[Any]] = [
        mapper for mapper in Base.registry.mappers if issubclass(mapper.class_, TenantAwareMixin)
    ]

    for mapper in tenant_mappers:
        selectable = getattr(mapper, "persist_selectable", None)
        if selectable is not None:
            selectables.add(selectable)

        selectable_attr = getattr(mapper, "selectable", None)
        if selectable_attr is not None:
            selectables.add(selectable_attr)

        local_table = getattr(mapper, "local_table", None)
        if local_table is not None:
            selectables.add(local_table)

    return selectables


def _iter_selectable_family(selectable: Any) -> list[Any]:
    """
    Yield a selectable and all related children (aliases, joins, etc.).
    """
    stack = [selectable]
    seen: set[Any] = set()

    results: list[Any] = []
    while stack:
        current = stack.pop()
        if current in seen:
            continue
        seen.add(current)
        results.append(current)

        for attr in ("element", "original", "left", "right"):
            child = getattr(current, attr, None)
            if child is not None and child is not current:
                stack.append(child)

    return results


def _statement_targets_tenant_entities(statement: Any) -> bool:
    """
    Determine whether the given statement references tenant-aware entities.
    """
    if not hasattr(statement, "get_final_froms"):
        return False

    tenant_selectables = _collect_tenant_selectables()
    if not tenant_selectables:
        return False

    try:
        from_clauses = statement.get_final_froms()
    except Exception:  # pragma: no cover - defensive against SQLAlchemy internals
        return False

    for from_clause in from_clauses:
        for candidate in _iter_selectable_family(from_clause):
            if candidate in tenant_selectables:
                return True

    return False


@event.listens_for(Session, "do_orm_execute")
def _inject_default_orm_filters(orm_execute_state: Any) -> None:
    """
    Apply soft-delete and tenant-aware filters to ORM SELECT statements.
    """
    if not orm_execute_state.is_select:
        return

    context = get_request_context()
    statement = orm_execute_state.statement

    if not context.include_deleted:
        statement = statement.options(
            with_loader_criteria(
                SoftDeleteMixin,
                lambda cls: cls.deleted_at.is_(None),
                include_aliases=True,
            )
        )

    targets_tenant_entities = _statement_targets_tenant_entities(statement)

    if targets_tenant_entities and not context.allow_global_access:
        tenant_id = context.tenant_id
        if tenant_id is None:
            raise TenantContextError("Tenant context is required for tenant-scoped queries")

        statement = statement.options(
            with_loader_criteria(
                TenantAwareMixin,
                lambda cls, tenant_id=tenant_id: cls.tenant_id == tenant_id,
                include_aliases=True,
            )
        )

    orm_execute_state.statement = statement


@event.listens_for(Session, "before_flush")
def _apply_audit_and_soft_delete_metadata(session: Session, flush_context: Any, instances: Any) -> None:
    """
    Populate audit metadata, enforce tenant scoping, and convert deletes to soft deletes.
    """
    context = get_request_context()
    user_id = context.user_id
    tenant_id = context.tenant_id

    # Convert hard deletes into soft deletes
    for instance in list(session.deleted):
        if isinstance(instance, SoftDeleteMixin):
            session.add(instance)
            instance.soft_delete(deleted_by=user_id)

    # Populate metadata for new instances
    for instance in session.new:
        if isinstance(instance, VersionedAuditMixin):
            if instance.created_by is None:
                instance.created_by = user_id
            instance.updated_by = user_id if user_id is not None else instance.updated_by

        if isinstance(instance, TenantAwareMixin):
            if instance.tenant_id is None:
                if tenant_id is None and not context.allow_global_access:
                    raise TenantContextError(f"Tenant context is required to create {instance.__class__.__name__}")
                if tenant_id is not None:
                    instance.tenant_id = tenant_id

            # Ensure tenant context matches when provided
            if tenant_id is not None and not context.allow_global_access and instance.tenant_id != tenant_id:
                raise TenantContextError(f"Tenant identifier mismatch for {instance.__class__.__name__}")

    # Track updater metadata for modified instances
    for instance in session.dirty:
        if isinstance(instance, VersionedAuditMixin) and session.is_modified(instance, include_collections=False):
            instance.updated_by = user_id if user_id is not None else instance.updated_by


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
    session_factory = get_session_factory()  # Get factory dynamically
    async with session_factory() as session:
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
