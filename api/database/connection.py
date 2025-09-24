"""
Enhanced database connection management with connection pooling and lifecycle management.

This module provides the ConnectionManager class with comprehensive connection pooling,
health monitoring, error recovery, and metrics collection capabilities.
"""

import asyncio
import time
import weakref
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from typing import Any, Optional

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncEngine, create_async_engine
from sqlalchemy.pool import NullPool

from configs.database import DatabaseConfig
from configs.settings import get_settings


@dataclass
class ConnectionMetrics:
    """Connection pool metrics tracking."""

    total_connections_created: int = 0
    total_connections_closed: int = 0
    active_connections: int = 0
    failed_connections: int = 0
    average_connection_time_ms: float = 0.0
    connection_times: list = field(default_factory=list)


class ConnectionManager:
    """
    Enhanced connection manager with pooling, health monitoring, and error recovery.

    Provides comprehensive database connection lifecycle management with detailed
    metrics, health checks, and graceful error handling.
    """

    def __init__(self, config: DatabaseConfig):
        """Initialize connection manager with database configuration."""
        self.config = config
        self.pool: Optional[AsyncEngine] = None
        self.is_initialized = False
        self.is_closed = False
        self.metrics = ConnectionMetrics()
        self._lock = asyncio.Lock()
        self._active_connections = weakref.WeakSet()

    async def initialize(self) -> None:
        """Initialize the connection pool and prepare for connections."""
        async with self._lock:
            if self.is_initialized:
                return

            try:
                # Create SQLAlchemy async engine with connection pooling
                self.pool = create_async_engine(
                    self.config.database_url,
                    # Pool configuration
                    pool_size=self.config.min_pool_size,
                    max_overflow=self.config.max_pool_size - self.config.min_pool_size,
                    pool_timeout=self.config.timeout_seconds,
                    pool_recycle=3600,  # Recycle connections after 1 hour
                    # Performance settings
                    echo=False,  # Set to True for SQL debugging
                    future=True,  # Use SQLAlchemy 2.0 style
                    # Connection arguments for asyncpg
                    connect_args={
                        "server_settings": {
                            "application_name": "Agentifui Pro API",
                        },
                        "command_timeout": self.config.timeout_seconds,
                    },
                )

                # Test the connection
                await self._test_connection()
                self.is_initialized = True

            except Exception as e:
                if self.pool:
                    await self.pool.dispose()
                    self.pool = None
                raise ConnectionError(f"Failed to initialize connection pool: {e}")

    async def close(self) -> None:
        """Gracefully close the connection manager and all connections."""
        async with self._lock:
            if self.is_closed:
                return

            # Wait for active connections to be returned
            max_wait_time = 30  # seconds
            start_time = time.time()

            while len(self._active_connections) > 0 and (time.time() - start_time) < max_wait_time:
                await asyncio.sleep(0.1)

            # Force close remaining connections and dispose pool
            if self.pool:
                await self.pool.dispose()
                self.pool = None

            self.is_closed = True
            self.is_initialized = False

    @asynccontextmanager
    async def get_connection(self) -> AsyncGenerator[AsyncConnection, None]:
        """
        Get a database connection from the pool.

        Returns:
            AsyncConnection: Database connection from pool
        """
        if not self.is_initialized:
            raise RuntimeError("Connection manager not initialized")

        if self.is_closed:
            raise RuntimeError("Connection manager is closed")

        start_time = time.time()
        connection = None

        try:
            # Get connection from pool
            connection = await self.pool.connect().__aenter__()
            self._active_connections.add(connection)

            # Update metrics
            connection_time = (time.time() - start_time) * 1000
            self.metrics.total_connections_created += 1
            self.metrics.active_connections = len(self._active_connections)
            self.metrics.connection_times.append(connection_time)

            # Keep only last 100 connection times for average calculation
            if len(self.metrics.connection_times) > 100:
                self.metrics.connection_times = self.metrics.connection_times[-100:]

            self.metrics.average_connection_time_ms = sum(self.metrics.connection_times) / len(
                self.metrics.connection_times
            )

            yield connection

        except Exception as e:
            self.metrics.failed_connections += 1
            raise ConnectionError(f"Failed to get database connection: {e}")

        finally:
            if connection:
                try:
                    await connection.__aexit__(None, None, None)
                    if connection in self._active_connections:
                        self._active_connections.discard(connection)
                    self.metrics.total_connections_closed += 1
                    self.metrics.active_connections = len(self._active_connections)
                except Exception:
                    pass  # Connection might already be closed

    async def return_connection(self, connection: AsyncConnection) -> None:
        """
        Return a connection to the pool (for compatibility with tests).

        Args:
            connection: Connection to return
        """
        # With context manager approach, connections are automatically returned
        # This method is kept for test compatibility
        if connection in self._active_connections:
            self._active_connections.discard(connection)
            self.metrics.active_connections = len(self._active_connections)

    async def health_check(self) -> dict[str, Any]:
        """
        Perform comprehensive health check of database connection.

        Returns:
            Health status with detailed information
        """
        start_time = time.time()

        try:
            if not self.is_initialized or self.is_closed:
                return {
                    "connected": False,
                    "error": "Connection manager not initialized or closed",
                    "response_time_ms": int((time.time() - start_time) * 1000),
                }

            async with self.get_connection() as conn:
                # Test basic connectivity
                await conn.execute(text("SELECT 1"))

                # Get database version
                result = await conn.execute(text("SELECT version()"))
                version = result.scalar()

                # Get current database name
                result = await conn.execute(text("SELECT current_database()"))
                database_name = result.scalar()

            response_time = int((time.time() - start_time) * 1000)

            return {
                "connected": True,
                "response_time_ms": response_time,
                "database_version": version,
                "database_name": database_name,
                "pool_status": await self.get_pool_status(),
                "configuration": self.config.model_dump_secure(),
            }

        except Exception as e:
            response_time = int((time.time() - start_time) * 1000)
            return {
                "connected": False,
                "error": str(e),
                "error_type": self._classify_error(e),
                "response_time_ms": response_time,
            }

    async def get_pool_status(self) -> dict[str, int]:
        """
        Get current connection pool status.

        Returns:
            Pool status information
        """
        if not self.pool or not self.is_initialized:
            return {
                "size": 0,
                "active": 0,
                "checked_out": 0,
                "min_size": self.config.min_pool_size,
                "max_size": self.config.max_pool_size,
            }

        pool = self.pool.pool
        return {
            "size": pool.size() if pool else 0,
            "active": len(self._active_connections),
            "checked_out": pool.checkedout() if pool else 0,
            "min_size": self.config.min_pool_size,
            "max_size": self.config.max_pool_size,
        }

    async def get_metrics(self) -> dict[str, Any]:
        """
        Get connection manager metrics.

        Returns:
            Metrics information
        """
        return {
            "total_connections_created": self.metrics.total_connections_created,
            "total_connections_closed": self.metrics.total_connections_closed,
            "active_connections": self.metrics.active_connections,
            "failed_connections": self.metrics.failed_connections,
            "average_connection_time_ms": round(self.metrics.average_connection_time_ms, 2),
            "pool_utilization": (
                self.metrics.active_connections / self.config.max_pool_size if self.config.max_pool_size > 0 else 0
            ),
        }

    async def reconnect(self) -> None:
        """Attempt to reconnect after connection loss."""
        try:
            await self.close()
            await self.initialize()
        except Exception as e:
            raise ConnectionError(f"Failed to reconnect: {e}")

    async def update_configuration(self, new_config: DatabaseConfig) -> None:
        """
        Update connection configuration and recreate pool.

        Args:
            new_config: New database configuration
        """
        await self.close()
        self.config = new_config
        await self.initialize()

    async def _test_connection(self) -> None:
        """Test the database connection during initialization."""
        try:
            async with self.pool.connect() as conn:
                await conn.execute(text("SELECT 1"))
        except Exception as e:
            raise ConnectionError(f"Database connection test failed: {e}")

    def _classify_error(self, error: Exception) -> str:
        """Classify database errors for better error reporting."""
        error_str = str(error).lower()

        if "timeout" in error_str:
            return "timeout"
        elif "connection" in error_str and ("refused" in error_str or "failed" in error_str):
            return "connection_failed"
        elif "authentication" in error_str or "password" in error_str:
            return "authentication_failed"
        elif "database" in error_str and "not found" in error_str:
            return "database_not_found"
        else:
            return "unknown"


# Global engine instance for backward compatibility
_engine: Optional[AsyncEngine] = None
_connection_manager: Optional[ConnectionManager] = None


def get_async_engine() -> AsyncEngine:
    """
    Get or create async SQLAlchemy engine (backward compatibility).

    Returns:
        AsyncEngine: Configured async SQLAlchemy engine
    """
    global _engine

    if _engine is None:
        settings = get_settings()

        # Use DATABASE_URL if available, otherwise construct from individual fields
        if hasattr(settings, "database_url") and settings.database_url:
            database_url = settings.database_url
        else:
            # Construct from database config
            database_url = settings.database.database_url

        _engine = create_async_engine(
            database_url,
            pool_size=getattr(settings, "database_pool_size", 10),
            max_overflow=getattr(settings, "database_pool_max_overflow", 20),
            pool_timeout=getattr(settings, "database_pool_timeout", 30),
            pool_recycle=getattr(settings, "database_pool_recycle", 3600),
            echo=settings.debug,
            future=True,
            connect_args={
                "server_settings": {
                    "application_name": settings.app_name,
                }
            },
        )

    return _engine


async def get_connection_manager() -> ConnectionManager:
    """
    Get global connection manager instance.

    Returns:
        ConnectionManager: Global connection manager
    """
    global _connection_manager

    if _connection_manager is None:
        settings = get_settings()
        _connection_manager = ConnectionManager(settings.database)
        await _connection_manager.initialize()

    return _connection_manager


async def dispose_engine() -> None:
    """Dispose of the global engine instance (backward compatibility)."""
    global _engine, _connection_manager

    if _connection_manager is not None:
        await _connection_manager.close()
        _connection_manager = None

    if _engine is not None:
        await _engine.dispose()
        _engine = None


def get_async_engine_for_testing() -> AsyncEngine:
    """Get async engine configured for testing (backward compatibility)."""
    settings = get_settings()

    if hasattr(settings, "database_url") and settings.database_url:
        database_url = settings.database_url
    else:
        database_url = settings.database.database_url

    return create_async_engine(
        database_url,
        poolclass=NullPool,
        echo=False,
        future=True,
    )


async def check_database_connection() -> bool:
    """Check if database connection is working (backward compatibility)."""
    try:
        manager = await get_connection_manager()
        health_result = await manager.health_check()
        return health_result["connected"]
    except Exception:
        return False


async def get_database_info() -> dict:
    """Get database information and connection status (backward compatibility)."""
    try:
        manager = await get_connection_manager()
        return await manager.health_check()
    except Exception as e:
        return {
            "connected": False,
            "error": str(e),
        }
