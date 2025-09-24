"""
Test database connection lifecycle management.

Tests the enhanced ConnectionManager with connection pooling,
lifecycle management, health monitoring, and error recovery.
"""

import asyncio
from unittest.mock import patch

import pytest

# These imports will fail until the implementation is complete
try:
    from configs.database import DatabaseConfig
    from database.connection import ConnectionManager
except ImportError:
    # Mock the classes for contract testing
    class ConnectionManager:
        def __init__(self, config):
            self.config = config

        async def initialize(self):
            pass

        async def close(self):
            pass

        async def get_connection(self):
            return None

        async def health_check(self):
            return {"connected": False}

    class DatabaseConfig:
        def __init__(self, **kwargs):
            pass


class TestDatabaseConnectionManager:
    """Test database connection manager lifecycle and pooling."""

    @pytest.fixture
    async def connection_manager(self):
        """Fixture for connection manager with test configuration."""
        # This fixture will FAIL until ConnectionManager is implemented
        config = DatabaseConfig(
            host="localhost",
            port=5432,
            username="test_user",
            password="test_password",
            database="test_db",
            driver="postgresql+asyncpg",
            min_pool_size=2,
            max_pool_size=10,
            timeout_seconds=30,
        )

        manager = ConnectionManager(config)
        await manager.initialize()

        yield manager

        await manager.close()

    async def test_connection_manager_initialization(self, connection_manager):
        """Test connection manager initialization with pool creation."""
        # Should initialize connection pool
        assert connection_manager.pool is not None
        assert connection_manager.is_initialized is True

        # Pool should respect configuration
        pool_info = await connection_manager.get_pool_status()
        assert pool_info["min_size"] == 2
        assert pool_info["max_size"] == 10

    async def test_connection_manager_get_connection(self, connection_manager):
        """Test getting database connection from pool."""
        # Should provide working connection
        async with connection_manager.get_connection() as conn:
            assert conn is not None
            # Connection should be usable
            result = await conn.execute("SELECT 1")
            assert result is not None

    async def test_connection_manager_connection_pooling(self, connection_manager):
        """Test connection pooling behavior and limits."""
        connections = []

        # Get multiple connections up to pool limit
        for i in range(5):
            conn = await connection_manager.get_connection()
            connections.append(conn)

        # Pool status should reflect active connections
        pool_status = await connection_manager.get_pool_status()
        assert pool_status["active"] == 5
        assert pool_status["checked_out"] <= 5

        # Return connections to pool
        for conn in connections:
            await connection_manager.return_connection(conn)

        # Pool should show reduced active connections
        pool_status = await connection_manager.get_pool_status()
        assert pool_status["active"] < 5

    async def test_connection_manager_pool_exhaustion(self, connection_manager):
        """Test behavior when connection pool is exhausted."""
        connections = []

        # Exhaust the connection pool
        for i in range(10):  # Max pool size
            conn = await connection_manager.get_connection()
            connections.append(conn)

        # Next connection request should either wait or fail gracefully
        with pytest.raises((asyncio.TimeoutError, ConnectionError)):
            async with asyncio.timeout(1):  # Short timeout
                await connection_manager.get_connection()

        # Clean up
        for conn in connections:
            await connection_manager.return_connection(conn)

    async def test_connection_manager_health_check(self, connection_manager):
        """Test database health check functionality."""
        health_status = await connection_manager.health_check()

        # Should provide comprehensive health information
        assert "connected" in health_status
        assert "response_time_ms" in health_status
        assert "pool_status" in health_status
        assert "database_version" in health_status

        if health_status["connected"]:
            assert isinstance(health_status["response_time_ms"], int)
            assert health_status["response_time_ms"] >= 0
            assert "pool_status" in health_status

    async def test_connection_manager_error_recovery(self, connection_manager):
        """Test connection manager error recovery and resilience."""
        # Simulate connection failure
        with patch.object(connection_manager, "_create_pool") as mock_create:
            mock_create.side_effect = ConnectionError("Database unreachable")

            # Health check should handle errors gracefully
            health_status = await connection_manager.health_check()
            assert health_status["connected"] is False
            assert "error" in health_status

        # Manager should attempt reconnection
        await connection_manager.reconnect()

        # After recovery, should work normally
        health_status = await connection_manager.health_check()
        # May succeed or fail depending on actual database availability

    async def test_connection_manager_concurrent_access(self, connection_manager):
        """Test connection manager under concurrent access."""

        async def get_and_use_connection():
            async with connection_manager.get_connection() as conn:
                # Simulate database work
                await asyncio.sleep(0.1)
                return await conn.execute("SELECT 1")

        # Run multiple concurrent operations
        tasks = [get_and_use_connection() for _ in range(20)]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Most operations should succeed
        successful = [r for r in results if not isinstance(r, Exception)]
        assert len(successful) > 15  # Allow some failures due to timing

    async def test_connection_manager_configuration_changes(self):
        """Test connection manager behavior with configuration changes."""
        # Initial configuration
        config1 = DatabaseConfig(
            host="localhost",
            port=5432,
            username="test_user",
            password="test_password",
            database="test_db1",
            max_pool_size=5,
        )

        manager = ConnectionManager(config1)
        await manager.initialize()

        initial_pool_size = (await manager.get_pool_status())["max_size"]
        assert initial_pool_size == 5

        # Update configuration
        config2 = DatabaseConfig(
            host="localhost",
            port=5432,
            username="test_user",
            password="test_password",
            database="test_db2",  # Different database
            max_pool_size=10,  # Different pool size
        )

        await manager.update_configuration(config2)

        # Pool should be recreated with new configuration
        updated_pool_size = (await manager.get_pool_status())["max_size"]
        assert updated_pool_size == 10

        await manager.close()

    async def test_connection_manager_timeout_handling(self):
        """Test connection timeout handling."""
        config = DatabaseConfig(
            host="10.255.255.1",  # Non-routable IP to cause timeout
            port=5432,
            username="test_user",
            password="test_password",
            database="test_db",
            timeout_seconds=1,  # Short timeout
        )

        manager = ConnectionManager(config)

        # Initialization should handle timeout
        with pytest.raises((asyncio.TimeoutError, ConnectionError)):
            await manager.initialize()

        # Health check should report timeout
        health_status = await manager.health_check()
        assert health_status["connected"] is False
        assert health_status.get("error_type") in ["timeout", "connection_failed"]

    async def test_connection_manager_memory_cleanup(self, connection_manager):
        """Test proper memory cleanup and resource management."""
        import gc

        # Get initial object count
        initial_objects = len(gc.get_objects())

        # Create and use many connections
        for i in range(100):
            async with connection_manager.get_connection() as conn:
                await conn.execute("SELECT 1")

        # Force garbage collection
        gc.collect()

        # Object count should not grow significantly
        final_objects = len(gc.get_objects())
        object_growth = final_objects - initial_objects

        # Allow some growth but not excessive (connection leaks)
        assert object_growth < 50  # Reasonable threshold

    async def test_connection_manager_graceful_shutdown(self, connection_manager):
        """Test graceful shutdown of connection manager."""
        # Get some active connections
        conn1 = await connection_manager.get_connection()
        conn2 = await connection_manager.get_connection()

        # Shutdown should wait for active connections
        shutdown_task = asyncio.create_task(connection_manager.close())

        # Give a moment for shutdown to start
        await asyncio.sleep(0.1)

        # Shutdown should not complete while connections are active
        assert not shutdown_task.done()

        # Return connections
        await connection_manager.return_connection(conn1)
        await connection_manager.return_connection(conn2)

        # Now shutdown should complete
        await shutdown_task

        assert connection_manager.is_closed is True

    @pytest.mark.parametrize("pool_size", [1, 5, 10, 20])
    async def test_connection_manager_different_pool_sizes(self, pool_size):
        """Test connection manager with different pool sizes."""
        config = DatabaseConfig(
            host="localhost",
            port=5432,
            username="test_user",
            password="test_password",
            database="test_db",
            max_pool_size=pool_size,
        )

        manager = ConnectionManager(config)
        await manager.initialize()

        try:
            # Should be able to get connections up to pool size
            connections = []
            for i in range(min(pool_size, 5)):  # Limit test connections
                conn = await manager.get_connection()
                connections.append(conn)

            pool_status = await manager.get_pool_status()
            assert pool_status["max_size"] == pool_size
            assert pool_status["active"] <= pool_size

            # Clean up connections
            for conn in connections:
                await connection_manager.return_connection(conn)

        finally:
            await manager.close()

    async def test_connection_manager_database_reconnection(self, connection_manager):
        """Test automatic database reconnection after connection loss."""
        # Simulate initial successful connection
        health_status = await connection_manager.health_check()
        initially_connected = health_status.get("connected", False)

        # Simulate connection loss (mock database going down)
        with patch.object(connection_manager.pool, "acquire", side_effect=ConnectionError):
            health_status = await connection_manager.health_check()
            assert health_status["connected"] is False

        # Simulate database recovery and test reconnection
        await connection_manager.reconnect()

        # Should attempt to restore connection
        health_status = await connection_manager.health_check()
        # Connection status depends on actual database availability

    async def test_connection_manager_metrics_collection(self, connection_manager):
        """Test connection manager metrics collection."""
        # Use connection manager to generate metrics
        for i in range(5):
            async with connection_manager.get_connection() as conn:
                await conn.execute("SELECT 1")

        # Should collect usage metrics
        metrics = await connection_manager.get_metrics()

        assert "total_connections_created" in metrics
        assert "total_connections_closed" in metrics
        assert "active_connections" in metrics
        assert "average_connection_time_ms" in metrics

        # Metrics should be reasonable
        assert metrics["total_connections_created"] >= 0
        assert metrics["active_connections"] >= 0
