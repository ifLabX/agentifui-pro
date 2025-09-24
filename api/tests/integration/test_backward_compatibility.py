"""
Test backward compatibility with existing DATABASE_URL configuration.

Tests that the enhanced configuration system maintains full backward
compatibility with existing DATABASE_URL-based configurations during transition.
"""

from httpx import AsyncClient

from tests.conftest import mock_environment_variables

# These imports will fail until the implementation is complete
try:
    from configs.settings import EnvironmentSettings
    from database.connection import ConnectionManager
except ImportError:
    # Mock the classes for contract testing
    class EnvironmentSettings:
        def __init__(self, **kwargs):
            pass

    class ConnectionManager:
        def __init__(self, config):
            pass


class TestBackwardCompatibility:
    """Test backward compatibility with legacy DATABASE_URL configuration."""

    async def test_database_url_only_configuration(self, async_client: AsyncClient):
        """Test application works with DATABASE_URL only (legacy configuration)."""
        # This test will FAIL until backward compatibility is implemented
        legacy_config = {
            "DATABASE_URL": "postgresql+asyncpg://user:pass@localhost:5432/testdb",
            "SECRET_KEY": "test-secret-key"
        }

        with mock_environment_variables(legacy_config):
            # Application should start and work normally
            response = await async_client.get("/health")
            assert response.status_code == 200

            # Database health check should work
            response = await async_client.get("/health/db")
            assert response.status_code == 200

            # Configuration endpoints should parse DATABASE_URL correctly
            response = await async_client.get("/config/database/status")
            assert response.status_code == 200
            data = response.json()

            config = data["configuration"]
            assert config["host"] == "localhost"
            assert config["port"] == 5432
            assert config["database"] == "testdb"
            assert data["configuration_source"] == "database_url"

    async def test_mixed_configuration_precedence(self, async_client: AsyncClient):
        """Test precedence when both DATABASE_URL and individual fields are present."""
        mixed_config = {
            "DATABASE_URL": "postgresql+asyncpg://url_user:url_pass@url_host:5433/url_db",
            "DB_HOST": "field_host",      # Should override URL host
            "DB_PORT": "5434",            # Should override URL port
            "DB_USERNAME": "field_user",   # Should override URL username
            # DB_PASSWORD and DB_DATABASE not set - should use URL values
            "SECRET_KEY": "test-secret-key"
        }

        with mock_environment_variables(mixed_config):
            response = await async_client.get("/config/database/status")
            assert response.status_code == 200
            data = response.json()

            config = data["configuration"]
            # Individual fields should take precedence
            assert config["host"] == "field_host"
            assert config["port"] == 5434
            # Fields not specified should use URL values
            assert config["database"] == "url_db"

            assert data["configuration_source"] == "mixed"

    async def test_legacy_cors_origins_json_array(self, async_client: AsyncClient):
        """Test backward compatibility with JSON array format for CORS origins."""
        legacy_cors_config = {
            "SECRET_KEY": "test-secret-key",
            "CORS_ORIGINS": '["http://localhost:3000", "http://localhost:3001", "https://app.example.com"]'
        }

        with mock_environment_variables(legacy_cors_config):
            response = await async_client.get("/config/validate")
            assert response.status_code == 200
            data = response.json()

            # Should parse JSON array correctly
            cors_result = data["validation_results"]["cors"]
            assert cors_result["origins_format"] == "json_array"
            assert cors_result["valid"] is True

            # May include migration recommendation
            if "recommendations" in data:
                recommendations = " ".join(data["recommendations"])
                assert "comma-separated" in recommendations.lower()

    async def test_legacy_environment_variables_parsing(self):
        """Test parsing of legacy environment variable formats."""
        legacy_config = {
            "DATABASE_URL": "postgresql+asyncpg://legacy_user:legacy_pass@legacy_host:5432/legacy_db",
            "SECRET_KEY": "legacy-secret-key",
            "DEBUG": "1",  # Legacy boolean format
            "CORS_ORIGINS": '["http://localhost:3000"]'  # Legacy JSON format
        }

        with mock_environment_variables(legacy_config):
            settings = EnvironmentSettings()

            # DATABASE_URL should be parsed correctly
            assert settings.database.host == "legacy_host"
            assert settings.database.username == "legacy_user"
            assert settings.database.database == "legacy_db"

            # Legacy boolean parsing
            assert settings.debug is True

            # Legacy CORS origins parsing
            assert settings.cors_origins == ["http://localhost:3000"]

    async def test_gradual_migration_scenario(self, async_client: AsyncClient):
        """Test gradual migration from DATABASE_URL to individual fields."""
        # Stage 1: Start with DATABASE_URL only
        stage1_config = {
            "DATABASE_URL": "postgresql+asyncpg://user:pass@old_host:5432/old_db",
            "SECRET_KEY": "test-secret-key"
        }

        with mock_environment_variables(stage1_config):
            response = await async_client.get("/config/database/status")
            assert response.status_code == 200
            data = response.json()
            assert data["configuration_source"] == "database_url"

        # Stage 2: Add some individual fields (mixed configuration)
        stage2_config = {
            "DATABASE_URL": "postgresql+asyncpg://user:pass@old_host:5432/old_db",
            "DB_HOST": "new_host",  # Override host
            "SECRET_KEY": "test-secret-key"
        }

        with mock_environment_variables(stage2_config):
            response = await async_client.get("/config/database/status")
            assert response.status_code == 200
            data = response.json()
            assert data["configuration_source"] == "mixed"
            assert data["configuration"]["host"] == "new_host"  # Field takes precedence

        # Stage 3: Complete migration to individual fields
        stage3_config = {
            "DB_HOST": "new_host",
            "DB_PORT": "5432",
            "DB_USERNAME": "new_user",
            "DB_PASSWORD": "new_pass",
            "DB_DATABASE": "new_db",
            "SECRET_KEY": "test-secret-key"
            # DATABASE_URL removed
        }

        with mock_environment_variables(stage3_config):
            response = await async_client.get("/config/database/status")
            assert response.status_code == 200
            data = response.json()
            assert data["configuration_source"] == "individual_fields"

    async def test_legacy_feature_flag_formats(self):
        """Test backward compatibility with legacy feature flag formats."""
        legacy_flags_config = {
            "SECRET_KEY": "test-secret-key",
            # Legacy boolean formats
            "FEATURE_AUTH_V2": "1",      # Numeric boolean
            "FEATURE_LOGGING": "true",   # String boolean
            "FEATURE_METRICS": "True",   # Capitalized boolean
            "FEATURE_DISABLED": "false", # Disabled feature
            # Legacy list format (if any features used lists)
            "FEATURE_ALLOWED_ORIGINS": '["example.com", "test.com"]'
        }

        with mock_environment_variables(legacy_flags_config):
            settings = EnvironmentSettings()

            # Should parse legacy boolean formats correctly
            assert settings.feature_auth_v2 is True
            assert settings.feature_logging is True
            assert settings.feature_metrics is True
            assert settings.feature_disabled is False

    async def test_legacy_database_drivers_support(self, async_client: AsyncClient):
        """Test backward compatibility with different database drivers."""
        # Test different legacy driver formats
        driver_configs = [
            "postgresql://user:pass@host:5432/db",           # Basic PostgreSQL
            "postgresql+psycopg2://user:pass@host:5432/db",  # Old psycopg2
            "postgresql+asyncpg://user:pass@host:5432/db",   # Current asyncpg
        ]

        for database_url in driver_configs:
            config = {
                "DATABASE_URL": database_url,
                "SECRET_KEY": "test-secret-key"
            }

            with mock_environment_variables(config):
                # Should parse all driver formats correctly
                response = await async_client.get("/config/database/status")
                # May succeed or return appropriate error for unsupported drivers
                assert response.status_code in [200, 400]  # 400 for unsupported drivers

                if response.status_code == 200:
                    data = response.json()
                    assert "driver" in data["configuration"]

    async def test_legacy_configuration_validation(self, async_client: AsyncClient):
        """Test that legacy configurations pass validation."""
        legacy_production_config = {
            "DATABASE_URL": "postgresql+asyncpg://prod_user:secure_prod_password@prod.example.com:5432/prod_db",
            "SECRET_KEY": "production-secret-key-must-be-at-least-32-characters-long-for-security",
            "ENVIRONMENT": "production",
            "CORS_ORIGINS": '["https://app.example.com", "https://admin.example.com"]',
            "DEBUG": "false"
        }

        with mock_environment_variables(legacy_production_config):
            response = await async_client.get("/config/validate")
            # Should validate successfully even with legacy format
            assert response.status_code == 200
            data = response.json()
            assert data["valid"] is True

    async def test_no_breaking_changes_in_api(self, async_client: AsyncClient):
        """Test that existing API endpoints maintain their contracts."""
        legacy_config = {
            "DATABASE_URL": "postgresql+asyncpg://user:pass@localhost:5432/testdb",
            "SECRET_KEY": "test-secret-key"
        }

        with mock_environment_variables(legacy_config):
            # All existing endpoints should continue to work
            endpoints_to_test = [
                "/health",
                "/health/db",
                # Add other existing endpoints that should remain unchanged
            ]

            for endpoint in endpoints_to_test:
                response = await async_client.get(endpoint)
                # Should not return 404 or 500 for existing endpoints
                assert response.status_code not in [404, 500]

    async def test_legacy_error_handling(self, async_client: AsyncClient):
        """Test that error handling maintains backward compatibility."""
        # Invalid DATABASE_URL should return helpful error
        invalid_config = {
            "DATABASE_URL": "invalid-url-format",
            "SECRET_KEY": "test-secret-key"
        }

        with mock_environment_variables(invalid_config):
            response = await async_client.get("/config/validate")

            # Should return validation error (400) not server error (500)
            assert response.status_code == 400
            data = response.json()

            # Error format should be consistent
            assert "error" in data
            assert "message" in data
            assert "validation_errors" in data

    async def test_performance_impact_of_compatibility_layer(self, async_client: AsyncClient):
        """Test that backward compatibility doesn't significantly impact performance."""
        import time

        configs = [
            # Legacy DATABASE_URL only
            {
                "DATABASE_URL": "postgresql+asyncpg://user:pass@localhost:5432/testdb",
                "SECRET_KEY": "test-secret-key"
            },
            # New individual fields
            {
                "DB_HOST": "localhost",
                "DB_PORT": "5432",
                "DB_USERNAME": "user",
                "DB_PASSWORD": "pass",
                "DB_DATABASE": "testdb",
                "SECRET_KEY": "test-secret-key"
            }
        ]

        response_times = []

        for config in configs:
            with mock_environment_variables(config):
                start_time = time.time()
                response = await async_client.get("/config/database/status")
                end_time = time.time()

                if response.status_code == 200:
                    response_time = (end_time - start_time) * 1000
                    response_times.append(response_time)

        # Both configurations should have similar performance
        if len(response_times) == 2:
            time_difference = abs(response_times[0] - response_times[1])
            # Difference should be minimal (less than 100ms)
            assert time_difference < 100

    async def test_data_consistency_across_formats(self, async_client: AsyncClient):
        """Test that the same database configuration produces consistent results across formats."""
        # Same database config in different formats
        database_url_config = {
            "DATABASE_URL": "postgresql+asyncpg://testuser:testpass@testhost:5433/testdb",
            "SECRET_KEY": "test-secret-key"
        }

        individual_fields_config = {
            "DB_HOST": "testhost",
            "DB_PORT": "5433",
            "DB_USERNAME": "testuser",
            "DB_PASSWORD": "testpass",
            "DB_DATABASE": "testdb",
            "DB_DRIVER": "postgresql+asyncpg",
            "SECRET_KEY": "test-secret-key"
        }

        responses = []

        for config in [database_url_config, individual_fields_config]:
            with mock_environment_variables(config):
                response = await async_client.get("/config/database/status")
                if response.status_code == 200:
                    responses.append(response.json())

        # Both should produce equivalent configuration data
        if len(responses) == 2:
            config1 = responses[0]["configuration"]
            config2 = responses[1]["configuration"]

            # Core database connection parameters should be identical
            assert config1["host"] == config2["host"]
            assert config1["port"] == config2["port"]
            assert config1["database"] == config2["database"]
            assert config1["driver"] == config2["driver"]