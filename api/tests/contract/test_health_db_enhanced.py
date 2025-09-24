"""
Contract test for GET /health/db enhanced endpoint.

This test validates the enhanced database health check endpoint contract
with detailed metrics and connection pool information.
"""

from httpx import AsyncClient

from tests.conftest import mock_environment_variables


class TestHealthDbEnhancedContract:
    """Contract tests for the enhanced database health check endpoint."""

    async def test_health_db_enhanced_success_response_schema(self, async_client: AsyncClient):
        """Test successful enhanced database health check response schema."""
        # This test will FAIL until the endpoint is enhanced
        response = await async_client.get("/health/db")

        assert response.status_code == 200
        data = response.json()

        # Basic health status
        assert "status" in data
        assert data["status"] in ["healthy", "unhealthy", "degraded"]

        assert "timestamp" in data
        assert isinstance(data["timestamp"], str)

        # Enhanced database information
        assert "database" in data
        database_info = data["database"]

        assert "connected" in database_info
        assert isinstance(database_info["connected"], bool)

        assert "response_time_ms" in database_info
        assert isinstance(database_info["response_time_ms"], int)

        assert "version" in database_info
        assert isinstance(database_info["version"], str)

        # Connection pool metrics
        assert "connection_pool" in database_info
        pool_info = database_info["connection_pool"]

        assert "size" in pool_info
        assert isinstance(pool_info["size"], int)
        assert pool_info["size"] >= 0

        assert "active" in pool_info
        assert isinstance(pool_info["active"], int)
        assert pool_info["active"] >= 0

        assert "checked_out" in pool_info
        assert isinstance(pool_info["checked_out"], int)
        assert pool_info["checked_out"] >= 0

        # Configuration information (sanitized)
        assert "configuration" in database_info
        config_info = database_info["configuration"]

        assert "host" in config_info
        assert isinstance(config_info["host"], str)
        assert "port" in config_info
        assert isinstance(config_info["port"], int)
        assert "database" in config_info
        assert isinstance(config_info["database"], str)
        assert "driver" in config_info
        assert isinstance(config_info["driver"], str)

        # Ensure sensitive information is not exposed
        assert "username" not in config_info
        assert "password" not in config_info

    async def test_health_db_enhanced_connection_failure(self, async_client: AsyncClient):
        """Test enhanced health check when database connection fails."""
        # Mock invalid database configuration
        with mock_environment_variables(
            {
                "DB_HOST": "nonexistent-host-12345",
                "DB_PORT": "5432",
                "DB_USERNAME": "test-user",
                "DB_PASSWORD": "test-password",
                "DB_DATABASE": "test-db",
            }
        ):
            response = await async_client.get("/health/db")

            # Should still return 200 but with unhealthy status
            assert response.status_code == 200
            data = response.json()

            assert data["status"] == "unhealthy"
            database_info = data["database"]
            assert database_info["connected"] is False

            # Should still include response time (time taken to fail)
            assert isinstance(database_info["response_time_ms"], int)
            assert database_info["response_time_ms"] >= 0

            # Pool metrics should reflect no active connections
            pool_info = database_info["connection_pool"]
            assert pool_info["active"] == 0
            assert pool_info["checked_out"] == 0

    async def test_health_db_enhanced_performance_metrics(self, async_client: AsyncClient):
        """Test that enhanced health check includes performance metrics."""
        response = await async_client.get("/health/db")

        if response.status_code == 200:
            data = response.json()
            database_info = data["database"]

            # Response time should be reasonable for healthy database
            if database_info["connected"]:
                response_time = database_info["response_time_ms"]
                assert response_time >= 0
                # Healthy database should respond quickly
                assert response_time < 1000  # 1 second max for health check

            # Pool metrics should be consistent
            pool_info = database_info["connection_pool"]
            assert pool_info["active"] <= pool_info["size"]
            assert pool_info["checked_out"] <= pool_info["active"]

    async def test_health_db_enhanced_configuration_sources(self, async_client: AsyncClient):
        """Test enhanced health check with different configuration sources."""
        # Test with individual fields
        with mock_environment_variables(
            {
                "DB_HOST": "localhost",
                "DB_PORT": "5432",
                "DB_USERNAME": "test-user",
                "DB_PASSWORD": "test-password",
                "DB_DATABASE": "test-db",
            }
        ):
            response = await async_client.get("/health/db")
            assert response.status_code == 200
            data = response.json()

            config_info = data["database"]["configuration"]
            assert config_info["host"] == "localhost"
            assert config_info["port"] == 5432
            assert config_info["database"] == "test-db"

        # Test with DATABASE_URL (backward compatibility)
        with mock_environment_variables({"DATABASE_URL": "postgresql+asyncpg://user:pass@test-host:5433/test-db"}):
            response = await async_client.get("/health/db")
            assert response.status_code == 200
            data = response.json()

            config_info = data["database"]["configuration"]
            assert config_info["host"] == "test-host"
            assert config_info["port"] == 5433
            assert config_info["database"] == "test-db"

    async def test_health_db_enhanced_security(self, async_client: AsyncClient):
        """Test that enhanced health check does not expose sensitive information."""
        response = await async_client.get("/health/db")

        # Password should never appear in response
        response_text = response.text.lower()
        assert "password" not in response_text
        assert "secret" not in response_text
        assert "auth" not in response_text

        if response.status_code == 200:
            data = response.json()
            # Ensure configuration section doesn't contain credentials
            config_info = data["database"]["configuration"]
            assert "username" not in config_info
            assert "password" not in config_info
            assert "credentials" not in config_info

    async def test_health_db_enhanced_error_handling(self, async_client: AsyncClient):
        """Test enhanced health check error handling for server errors."""
        # Mock extreme configuration that might cause server error
        with mock_environment_variables(
            {
                "DB_HOST": "",  # Empty host
                "DB_PORT": "invalid",  # Invalid port
            }
        ):
            response = await async_client.get("/health/db")

            # Could return 500 for server error or 200 with unhealthy status
            if response.status_code == 500:
                data = response.json()
                assert "error" in data
                assert "message" in data
                assert "request_id" in data
                assert "timestamp" in data
            elif response.status_code == 200:
                data = response.json()
                assert data["status"] == "unhealthy"

    async def test_health_db_enhanced_performance_requirement(self, async_client: AsyncClient):
        """Test that enhanced health check meets performance requirements."""
        import time

        start_time = time.time()
        response = await async_client.get("/health/db")
        end_time = time.time()

        response_time_ms = (end_time - start_time) * 1000

        # Health check should be fast (performance requirement)
        assert response_time_ms < 500  # 500ms max for health endpoint

        if response.status_code == 200:
            data = response.json()
            # Internal database response time should also be reasonable
            db_response_time = data["database"]["response_time_ms"]
            assert db_response_time < 200  # Database health check should be sub-200ms

    async def test_health_db_enhanced_pool_monitoring(self, async_client: AsyncClient):
        """Test connection pool monitoring in enhanced health check."""
        response = await async_client.get("/health/db")

        if response.status_code == 200:
            data = response.json()
            if data["database"]["connected"]:
                pool_info = data["database"]["connection_pool"]

                # Pool should have reasonable configuration
                assert pool_info["size"] > 0  # Should have minimum pool size
                assert pool_info["size"] <= 100  # Should have maximum pool size

                # Active connections should not exceed total size
                assert pool_info["active"] <= pool_info["size"]

                # Checked out connections should not exceed active
                assert pool_info["checked_out"] <= pool_info["active"]

                # All metrics should be non-negative
                assert all(value >= 0 for value in pool_info.values())
