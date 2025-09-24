"""
Contract test for GET /config/database/status endpoint.

This test validates the database configuration status endpoint contract
according to the OpenAPI specification in contracts/settings.yaml.
"""

from httpx import AsyncClient

from tests.conftest import mock_environment_variables


class TestDatabaseStatusContract:
    """Contract tests for the database configuration status endpoint."""

    async def test_database_status_success_response_schema(self, async_client: AsyncClient):
        """Test successful database status response schema."""
        # This test will FAIL until the endpoint is implemented
        response = await async_client.get("/config/database/status")

        assert response.status_code == 200
        data = response.json()

        # Validate response schema according to DatabaseConfigStatusResponse
        assert "configuration" in data
        configuration = data["configuration"]

        # Configuration fields (password and username omitted for security)
        assert "host" in configuration
        assert isinstance(configuration["host"], str)
        assert "port" in configuration
        assert isinstance(configuration["port"], int)
        assert "database" in configuration
        assert isinstance(configuration["database"], str)
        assert "driver" in configuration
        assert isinstance(configuration["driver"], str)

        # Connection status
        assert "connection_status" in data
        connection_status = data["connection_status"]
        assert "connected" in connection_status
        assert isinstance(connection_status["connected"], bool)
        assert "response_time_ms" in connection_status
        assert isinstance(connection_status["response_time_ms"], int)
        assert "last_check" in connection_status
        assert isinstance(connection_status["last_check"], str)

        # Configuration source
        assert "configuration_source" in data
        assert data["configuration_source"] in ["individual_fields", "database_url", "mixed"]

    async def test_database_status_with_individual_fields(self, async_client: AsyncClient):
        """Test database status when using individual field configuration."""
        db_config = {
            "DB_HOST": "test-host",
            "DB_PORT": "5432",
            "DB_USERNAME": "test-user",
            "DB_PASSWORD": "test-password",
            "DB_DATABASE": "test-db"
        }

        with mock_environment_variables(db_config):
            response = await async_client.get("/config/database/status")

            assert response.status_code == 200
            data = response.json()

            # Should indicate individual fields source
            assert data["configuration_source"] == "individual_fields"

            # Configuration should match (excluding credentials)
            config = data["configuration"]
            assert config["host"] == "test-host"
            assert config["port"] == 5432
            assert config["database"] == "test-db"
            assert config["driver"] == "postgresql+asyncpg"  # default

    async def test_database_status_with_database_url(self, async_client: AsyncClient):
        """Test database status when using DATABASE_URL configuration."""
        with mock_environment_variables({
            "DATABASE_URL": "postgresql+asyncpg://user:pass@test-host:5433/test-db"
        }):
            response = await async_client.get("/config/database/status")

            assert response.status_code == 200
            data = response.json()

            # Should indicate database_url source
            assert data["configuration_source"] == "database_url"

            # Configuration should be parsed from URL
            config = data["configuration"]
            assert config["host"] == "test-host"
            assert config["port"] == 5433
            assert config["database"] == "test-db"

    async def test_database_status_pool_status(self, async_client: AsyncClient):
        """Test database status includes pool status when available."""
        response = await async_client.get("/config/database/status")

        # Response should include pool status if connection is active
        if response.status_code == 200:
            data = response.json()
            if data["connection_status"]["connected"]:
                # Pool status should be included for connected databases
                if "pool_status" in data:
                    pool_status = data["pool_status"]
                    assert "size" in pool_status
                    assert isinstance(pool_status["size"], int)
                    assert "active" in pool_status
                    assert isinstance(pool_status["active"], int)
                    assert "checked_out" in pool_status
                    assert isinstance(pool_status["checked_out"], int)

    async def test_database_status_connection_failure(self, async_client: AsyncClient):
        """Test database status when connection fails."""
        # Configure non-existent database host
        with mock_environment_variables({
            "DB_HOST": "nonexistent-host-12345",
            "DB_PORT": "5432",
            "DB_USERNAME": "test-user",
            "DB_PASSWORD": "test-password",
            "DB_DATABASE": "test-db"
        }):
            response = await async_client.get("/config/database/status")

            # Should still return 200 but with connection_status.connected = false
            assert response.status_code == 200
            data = response.json()

            connection_status = data["connection_status"]
            assert connection_status["connected"] is False
            # Response time should still be present (time taken to fail)
            assert isinstance(connection_status["response_time_ms"], int)

    async def test_database_status_error_handling(self, async_client: AsyncClient):
        """Test error handling for server errors during status check."""
        # Mock extreme configuration that might cause server error
        with mock_environment_variables({
            "DB_HOST": "",  # Empty host might cause validation error
            "DB_PORT": "invalid",  # Invalid port
        }):
            response = await async_client.get("/config/database/status")

            if response.status_code == 500:
                data = response.json()
                assert "error" in data
                assert "message" in data
                assert "request_id" in data
                assert "timestamp" in data

    async def test_database_status_security(self, async_client: AsyncClient):
        """Test that sensitive information is not exposed in response."""
        response = await async_client.get("/config/database/status")

        if response.status_code == 200:
            data = response.json()
            response_str = str(data)

            # Ensure password is not in the response
            assert "password" not in response_str.lower()
            assert "secret" not in response_str.lower()

            # Username should not be directly exposed in configuration
            config = data["configuration"]
            assert "username" not in config
            assert "password" not in config

    async def test_database_status_performance(self, async_client: AsyncClient):
        """Test that database status endpoint responds within reasonable time."""
        import time

        start_time = time.time()
        response = await async_client.get("/config/database/status")
        end_time = time.time()

        response_time_ms = (end_time - start_time) * 1000

        # Should respond within 200ms (performance requirement)
        assert response_time_ms < 200

        if response.status_code == 200:
            data = response.json()
            # Response time in data should be reasonable
            if "connection_status" in data:
                reported_time = data["connection_status"]["response_time_ms"]
                # Database response time should be reasonable
                assert reported_time < 100  # Most database calls should be sub-100ms