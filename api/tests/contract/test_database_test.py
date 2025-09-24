"""
Contract test for POST /config/database/test endpoint.

This test validates the database connection testing endpoint contract
according to the OpenAPI specification in contracts/settings.yaml.
"""

from httpx import AsyncClient


class TestDatabaseTestContract:
    """Contract tests for the database connection test endpoint."""

    async def test_database_test_success_response_schema(self, async_client: AsyncClient):
        """Test successful database connection test response schema."""
        # This test will FAIL until the endpoint is implemented
        test_config = {
            "host": "localhost",
            "port": 5432,
            "username": "test-user",
            "password": "test-password",
            "database": "test-db",
            "timeout_seconds": 10,
        }

        response = await async_client.post("/config/database/test", json=test_config)

        assert response.status_code == 200
        data = response.json()

        # Validate response schema according to DatabaseTestResponse
        assert "success" in data
        assert isinstance(data["success"], bool)

        assert "response_time_ms" in data
        assert isinstance(data["response_time_ms"], int)

        assert "tested_configuration" in data
        tested_config = data["tested_configuration"]
        assert "host" in tested_config
        assert "port" in tested_config
        assert "database" in tested_config
        assert "driver" in tested_config

        if data["success"]:
            # Successful connection should include database info
            assert "database_info" in data
            db_info = data["database_info"]
            assert "version" in db_info
            assert isinstance(db_info["version"], str)
        else:
            # Failed connection should include error details
            assert "error_details" in data
            error_details = data["error_details"]
            assert "error_type" in error_details
            assert error_details["error_type"] in [
                "connection_failed",
                "authentication_failed",
                "database_not_found",
                "timeout",
                "unknown",
            ]
            assert "message" in error_details
            assert isinstance(error_details["message"], str)

    async def test_database_test_without_request_body(self, async_client: AsyncClient):
        """Test database connection test using current configuration (no request body)."""
        # Test without request body should use current config
        response = await async_client.post("/config/database/test")

        assert response.status_code == 200
        data = response.json()

        # Should still return valid schema
        assert "success" in data
        assert "response_time_ms" in data
        assert "tested_configuration" in data

    async def test_database_test_with_valid_config(self, async_client: AsyncClient):
        """Test database connection test with valid configuration."""
        test_config = {
            "host": "localhost",
            "port": 5432,
            "username": "postgres",
            "password": "postgres",
            "database": "postgres",
            "driver": "postgresql+asyncpg",
            "timeout_seconds": 5,
        }

        response = await async_client.post("/config/database/test", json=test_config)

        assert response.status_code == 200
        data = response.json()

        # Tested configuration should match what was sent
        tested_config = data["tested_configuration"]
        assert tested_config["host"] == "localhost"
        assert tested_config["port"] == 5432
        assert tested_config["database"] == "postgres"
        assert tested_config["driver"] == "postgresql+asyncpg"

    async def test_database_test_with_invalid_host(self, async_client: AsyncClient):
        """Test database connection test with invalid host."""
        test_config = {
            "host": "nonexistent-host-12345",
            "port": 5432,
            "username": "test-user",
            "password": "test-password",
            "database": "test-db",
            "timeout_seconds": 5,
        }

        response = await async_client.post("/config/database/test", json=test_config)

        assert response.status_code == 200
        data = response.json()

        # Should return failure with appropriate error details
        assert data["success"] is False
        assert "error_details" in data

        error_details = data["error_details"]
        assert error_details["error_type"] in ["connection_failed", "timeout"]
        assert "suggestions" in error_details
        assert isinstance(error_details["suggestions"], list)

    async def test_database_test_with_invalid_credentials(self, async_client: AsyncClient):
        """Test database connection test with invalid credentials."""
        test_config = {
            "host": "localhost",
            "port": 5432,
            "username": "invalid-user",
            "password": "wrong-password",
            "database": "test-db",
            "timeout_seconds": 5,
        }

        response = await async_client.post("/config/database/test", json=test_config)

        assert response.status_code == 200
        data = response.json()

        # Should return failure with authentication error
        if not data["success"]:
            error_details = data["error_details"]
            assert error_details["error_type"] in ["authentication_failed", "connection_failed"]

    async def test_database_test_timeout(self, async_client: AsyncClient):
        """Test database connection test timeout handling."""
        test_config = {
            "host": "10.255.255.1",  # Non-routable IP to cause timeout
            "port": 5432,
            "username": "test-user",
            "password": "test-password",
            "database": "test-db",
            "timeout_seconds": 1,  # Short timeout
        }

        response = await async_client.post("/config/database/test", json=test_config)

        assert response.status_code == 200
        data = response.json()

        # Should return failure due to timeout
        if not data["success"]:
            error_details = data["error_details"]
            assert error_details["error_type"] in ["timeout", "connection_failed"]

    async def test_database_test_validation_errors(self, async_client: AsyncClient):
        """Test database connection test with invalid request data."""
        # Invalid port number
        test_config = {
            "host": "localhost",
            "port": 70000,  # Invalid port
            "username": "test-user",
            "password": "test-password",
            "database": "test-db",
        }

        response = await async_client.post("/config/database/test", json=test_config)

        assert response.status_code == 400
        data = response.json()

        # Should return validation error
        assert "error" in data
        assert "message" in data
        assert "validation_errors" in data
        assert isinstance(data["validation_errors"], list)

    async def test_database_test_missing_required_fields(self, async_client: AsyncClient):
        """Test database connection test with missing required fields."""
        test_config = {
            "host": "localhost",
            # Missing port, username, password, database
        }

        response = await async_client.post("/config/database/test", json=test_config)

        # Should return 400 for validation errors
        assert response.status_code == 400
        data = response.json()
        assert "validation_errors" in data

    async def test_database_test_malformed_json(self, async_client: AsyncClient):
        """Test database connection test with malformed JSON."""
        response = await async_client.post(
            "/config/database/test", content="invalid json", headers={"Content-Type": "application/json"}
        )

        assert response.status_code == 422  # Unprocessable Entity

    async def test_database_test_performance(self, async_client: AsyncClient):
        """Test that database test endpoint responds within reasonable time."""
        import time

        test_config = {
            "host": "localhost",
            "port": 5432,
            "username": "test-user",
            "password": "test-password",
            "database": "test-db",
            "timeout_seconds": 2,
        }

        start_time = time.time()
        response = await async_client.post("/config/database/test", json=test_config)
        end_time = time.time()

        response_time_ms = (end_time - start_time) * 1000

        # Should respond within performance requirement (plus timeout buffer)
        assert response_time_ms < 3000  # 3 seconds max including timeout

        if response.status_code == 200:
            data = response.json()
            # Reported response time should be reasonable
            reported_time = data["response_time_ms"]
            assert isinstance(reported_time, int)
            assert reported_time >= 0

    async def test_database_test_security(self, async_client: AsyncClient):
        """Test that sensitive information is not exposed in error messages."""
        test_config = {
            "host": "localhost",
            "port": 5432,
            "username": "test-user",
            "password": "secret-password-123",
            "database": "test-db",
        }

        response = await async_client.post("/config/database/test", json=test_config)

        # Password should not appear in response
        response_text = response.text
        assert "secret-password-123" not in response_text
        assert test_config["password"] not in response_text

    async def test_database_test_default_values(self, async_client: AsyncClient):
        """Test database connection test with default values."""
        # Minimal config should use defaults
        test_config = {"host": "localhost", "username": "test-user", "password": "test-password", "database": "test-db"}

        response = await async_client.post("/config/database/test", json=test_config)

        if response.status_code == 200:
            data = response.json()
            tested_config = data["tested_configuration"]

            # Should use default values
            assert tested_config["port"] == 5432  # Default PostgreSQL port
            assert tested_config["driver"] == "postgresql+asyncpg"  # Default driver
