"""
Contract test for GET /config/validate endpoint.

This test validates the configuration validation endpoint contract
according to the OpenAPI specification in contracts/settings.yaml.
"""

from httpx import AsyncClient

from tests.conftest import mock_environment_variables


class TestConfigValidateContract:
    """Contract tests for the configuration validation endpoint."""

    async def test_config_validate_success_response_schema(self, async_client: AsyncClient):
        """Test successful configuration validation response schema."""
        # This test will FAIL until the endpoint is implemented
        response = await async_client.get("/config/validate")

        assert response.status_code == 200
        data = response.json()

        # Validate response schema according to ConfigurationValidationResponse
        assert "valid" in data
        assert isinstance(data["valid"], bool)

        assert "environment" in data
        assert isinstance(data["environment"], str)
        assert data["environment"] in ["development", "staging", "production"]

        assert "validation_results" in data
        validation_results = data["validation_results"]

        # Database validation result
        assert "database" in validation_results
        database_result = validation_results["database"]
        assert "valid" in database_result
        assert isinstance(database_result["valid"], bool)

        # CORS validation result
        assert "cors" in validation_results
        cors_result = validation_results["cors"]
        assert "valid" in cors_result
        assert isinstance(cors_result["valid"], bool)
        assert "origins_format" in cors_result
        assert cors_result["origins_format"] in ["comma_separated", "json_array", "mixed"]

        # Security validation result
        assert "security" in validation_results
        security_result = validation_results["security"]
        assert "valid" in security_result
        assert isinstance(security_result["valid"], bool)

        # Feature flags validation result
        assert "feature_flags" in validation_results
        feature_flags_result = validation_results["feature_flags"]
        assert "valid" in feature_flags_result
        assert isinstance(feature_flags_result["valid"], bool)

    async def test_config_validate_with_invalid_configuration(self, async_client: AsyncClient):
        """Test configuration validation with invalid settings."""
        # Mock invalid database port
        with mock_environment_variables({"DB_PORT": "70000"}):
            response = await async_client.get("/config/validate")

            # Should return 400 for validation failure
            assert response.status_code == 400
            data = response.json()

            assert "error" in data
            assert "message" in data
            assert "validation_errors" in data
            assert isinstance(data["validation_errors"], list)

    async def test_config_validate_development_environment(self, async_client: AsyncClient):
        """Test configuration validation in development environment."""
        dev_config = {
            "ENVIRONMENT": "development",
            "DB_HOST": "localhost",
            "DB_PORT": "5432",
            "DB_USERNAME": "dev-user",
            "DB_PASSWORD": "dev-password",
            "DB_DATABASE": "dev-db",
            "SECRET_KEY": "dev-secret-key",
            "CORS_ORIGINS": "http://localhost:3000,http://localhost:3001"
        }

        with mock_environment_variables(dev_config):
            response = await async_client.get("/config/validate")

            assert response.status_code == 200
            data = response.json()
            assert data["environment"] == "development"
            assert data["valid"] is True

    async def test_config_validate_production_environment(self, async_client: AsyncClient):
        """Test configuration validation in production environment."""
        prod_config = {
            "ENVIRONMENT": "production",
            "DB_HOST": "prod-host.example.com",
            "DB_PORT": "5432",
            "DB_USERNAME": "prod-user",
            "DB_PASSWORD": "super-secure-production-password-32-chars-long",
            "DB_DATABASE": "prod-db",
            "SECRET_KEY": "production-secret-key-must-be-at-least-32-characters-long-for-security",
            "CORS_ORIGINS": "https://app.example.com,https://admin.example.com"
        }

        with mock_environment_variables(prod_config):
            response = await async_client.get("/config/validate")

            assert response.status_code == 200
            data = response.json()
            assert data["environment"] == "production"

            # Production should have stricter validation
            security_result = data["validation_results"]["security"]
            assert security_result["production_requirements"]["met"] is True

    async def test_config_validate_cors_format_detection(self, async_client: AsyncClient):
        """Test CORS origins format detection."""
        # Test comma-separated format
        with mock_environment_variables({"CORS_ORIGINS": "http://localhost:3000,http://localhost:3001"}):
            response = await async_client.get("/config/validate")
            assert response.status_code == 200
            data = response.json()
            assert data["validation_results"]["cors"]["origins_format"] == "comma_separated"

        # Test JSON array format
        with mock_environment_variables({"CORS_ORIGINS": '["http://localhost:3000","http://localhost:3001"]'}):
            response = await async_client.get("/config/validate")
            assert response.status_code == 200
            data = response.json()
            assert data["validation_results"]["cors"]["origins_format"] == "json_array"

    async def test_config_validate_warnings_and_recommendations(self, async_client: AsyncClient):
        """Test that warnings and recommendations are included when appropriate."""
        # Use JSON array format to trigger migration recommendation
        with mock_environment_variables({"CORS_ORIGINS": '["http://localhost:3000"]'}):
            response = await async_client.get("/config/validate")

            assert response.status_code == 200
            data = response.json()

            # Should include warnings or recommendations arrays
            assert "warnings" in data
            assert isinstance(data["warnings"], list)
            assert "recommendations" in data
            assert isinstance(data["recommendations"], list)

    async def test_config_validate_error_handling(self, async_client: AsyncClient):
        """Test error handling for server errors during validation."""
        # This test may need to be adjusted based on actual error conditions
        # For now, we test the expected error response schema

        # Mock a scenario that might cause server error (empty environment)
        with mock_environment_variables({}):
            response = await async_client.get("/config/validate")

            # May return 500 for server error or 400 for validation error
            if response.status_code == 500:
                data = response.json()
                assert "error" in data
                assert "message" in data
                assert "request_id" in data
                assert "timestamp" in data