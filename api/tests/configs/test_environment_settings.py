"""
Test enhanced environment settings validation and configuration management.

Tests the enhanced EnvironmentSettings class with field validation,
environment-specific rules, and comprehensive configuration management.
"""

import pytest
from pydantic import ValidationError

from tests.conftest import mock_environment_variables

# These imports will fail until the implementation is complete
try:
    from configs.settings import EnvironmentSettings
except ImportError:
    # Mock the class for contract testing
    class EnvironmentSettings:
        def __init__(self, **kwargs):
            pass


class TestEnvironmentSettings:
    """Test enhanced environment settings validation and configuration."""

    def test_environment_settings_development_config(self):
        """Test development environment configuration."""
        # This test will FAIL until EnvironmentSettings is enhanced
        dev_config = {
            "ENVIRONMENT": "development",
            "DB_HOST": "localhost",
            "DB_PORT": "5432",
            "DB_USERNAME": "dev_user",
            "DB_PASSWORD": "dev_password",
            "DB_DATABASE": "dev_db",
            "SECRET_KEY": "dev-secret-key",
            "CORS_ORIGINS": "http://localhost:3000,http://localhost:3001",
        }

        with mock_environment_variables(dev_config):
            settings = EnvironmentSettings()

            assert settings.environment == "development"
            assert settings.database.host == "localhost"
            assert settings.database.port == 5432
            assert settings.database.database == "dev_db"
            assert settings.secret_key == "dev-secret-key"

    def test_environment_settings_production_config(self):
        """Test production environment configuration with stricter validation."""
        prod_config = {
            "ENVIRONMENT": "production",
            "DB_HOST": "prod-host.example.com",
            "DB_PORT": "5432",
            "DB_USERNAME": "prod_user",
            "DB_PASSWORD": "super-secure-production-password-32-chars-long",
            "DB_DATABASE": "prod_db",
            "SECRET_KEY": "production-secret-key-must-be-at-least-32-characters-long-for-security",
            "CORS_ORIGINS": "https://app.example.com,https://admin.example.com",
        }

        with mock_environment_variables(prod_config):
            settings = EnvironmentSettings()

            assert settings.environment == "production"
            assert settings.database.host == "prod-host.example.com"
            assert len(settings.secret_key) >= 32  # Production requirement
            assert all(origin.startswith("https://") for origin in settings.cors_origins)

    def test_environment_settings_database_url_backward_compatibility(self):
        """Test backward compatibility with DATABASE_URL."""
        config = {
            "DATABASE_URL": "postgresql+asyncpg://user:pass@db.example.com:5433/mydb",
            "SECRET_KEY": "test-secret-key",
            "CORS_ORIGINS": "http://localhost:3000",
        }

        with mock_environment_variables(config):
            settings = EnvironmentSettings()

            assert settings.database.host == "db.example.com"
            assert settings.database.port == 5433
            assert settings.database.database == "mydb"
            assert settings.database.username == "user"

    def test_environment_settings_mixed_database_config(self):
        """Test mixed database configuration (both URL and individual fields)."""
        config = {
            "DATABASE_URL": "postgresql+asyncpg://user:pass@db.example.com:5433/mydb",
            "DB_HOST": "override-host",  # Should override URL host
            "DB_PORT": "5434",  # Should override URL port
            "SECRET_KEY": "test-secret-key",
            "CORS_ORIGINS": "http://localhost:3000",
        }

        with mock_environment_variables(config):
            settings = EnvironmentSettings()

            # Individual fields should take precedence over URL
            assert settings.database.host == "override-host"
            assert settings.database.port == 5434
            # Other fields from URL should remain
            assert settings.database.database == "mydb"
            assert settings.database.username == "user"

    def test_environment_settings_cors_parsing(self):
        """Test CORS origins parsing from comma-separated values."""
        config = {
            "SECRET_KEY": "test-secret-key",
            "CORS_ORIGINS": "http://localhost:3000,http://localhost:3001,https://app.example.com",
        }

        with mock_environment_variables(config):
            settings = EnvironmentSettings()

            expected_origins = ["http://localhost:3000", "http://localhost:3001", "https://app.example.com"]
            assert settings.cors_origins == expected_origins

    def test_environment_settings_cors_json_array_backward_compatibility(self):
        """Test backward compatibility with JSON array format for CORS origins."""
        config = {"SECRET_KEY": "test-secret-key", "CORS_ORIGINS": '["http://localhost:3000", "http://localhost:3001"]'}

        with mock_environment_variables(config):
            settings = EnvironmentSettings()

            expected_origins = ["http://localhost:3000", "http://localhost:3001"]
            assert settings.cors_origins == expected_origins

    def test_environment_settings_validation_errors(self):
        """Test validation errors for invalid configuration."""
        # Invalid environment
        config = {"ENVIRONMENT": "invalid_env"}
        with mock_environment_variables(config):
            with pytest.raises(ValidationError) as exc_info:
                EnvironmentSettings()

        errors = exc_info.value.errors()
        assert any(error["loc"] == ("environment",) for error in errors)

        # Missing required fields
        config = {}  # Missing SECRET_KEY
        with mock_environment_variables(config):
            with pytest.raises(ValidationError) as exc_info:
                EnvironmentSettings()

        errors = exc_info.value.errors()
        assert any("secret_key" in str(error["loc"]) for error in errors)

    def test_environment_settings_production_security_validation(self):
        """Test production-specific security validation."""
        # Production with weak secret key should fail
        config = {
            "ENVIRONMENT": "production",
            "SECRET_KEY": "weak",  # Too short for production
            "DB_PASSWORD": "weak_prod_password",  # Too short for production
            "CORS_ORIGINS": "http://insecure.com",  # HTTP not allowed in production
        }

        with pytest.raises(ValidationError) as exc_info:
            with mock_environment_variables(config):
                EnvironmentSettings()

        errors = exc_info.value.errors()
        error_fields = [str(error["loc"]) for error in errors]

        # Should have validation errors for production security requirements
        assert any("secret_key" in field for field in error_fields)

    def test_environment_settings_default_values(self):
        """Test default values for optional configuration."""
        minimal_config = {"SECRET_KEY": "test-secret-key-with-sufficient-length"}

        with mock_environment_variables(minimal_config):
            settings = EnvironmentSettings()

            # Should use default values
            assert settings.environment == "development"  # Default environment
            assert settings.database.host == "localhost"  # Default database host
            assert settings.database.port == 5432  # Default database port
            assert settings.debug is True  # Default debug mode for development

    def test_environment_settings_feature_flags(self):
        """Test feature flags configuration."""
        config = {
            "SECRET_KEY": "test-secret-key",
            "FEATURE_AUTH_V2": "true",
            "FEATURE_ENHANCED_LOGGING": "false",
            "FEATURE_RATE_LIMITING": "1",  # Truthy value
        }

        with mock_environment_variables(config):
            settings = EnvironmentSettings()

            assert settings.feature_auth_v2 is True
            assert settings.feature_enhanced_logging is False
            assert settings.feature_rate_limiting is True

    def test_environment_settings_logging_configuration(self):
        """Test logging configuration based on environment."""
        # Development logging
        dev_config = {"ENVIRONMENT": "development", "SECRET_KEY": "test-secret-key"}

        with mock_environment_variables(dev_config):
            settings = EnvironmentSettings()
            assert settings.log_level == "DEBUG"
            assert settings.debug is True

        # Production logging
        prod_config = {
            "ENVIRONMENT": "production",
            "SECRET_KEY": "production-secret-key-must-be-at-least-32-characters-long",
            "DB_PASSWORD": "production-password-must-be-secure-32-chars",
        }

        with mock_environment_variables(prod_config):
            settings = EnvironmentSettings()
            assert settings.log_level == "INFO"
            assert settings.debug is False

    def test_environment_settings_database_connection_config(self):
        """Test database connection-specific configuration."""
        config = {
            "SECRET_KEY": "test-secret-key",
            "DB_TIMEOUT_SECONDS": "45",
            "DB_MAX_POOL_SIZE": "20",
            "DB_MIN_POOL_SIZE": "2",
        }

        with mock_environment_variables(config):
            settings = EnvironmentSettings()

            assert settings.database.timeout_seconds == 45
            assert settings.database.max_pool_size == 20
            assert settings.database.min_pool_size == 2

    def test_environment_settings_configuration_source_detection(self):
        """Test detection of configuration sources."""
        # Individual fields only
        individual_config = {
            "DB_HOST": "localhost",
            "DB_PORT": "5432",
            "DB_USERNAME": "user",
            "DB_PASSWORD": "pass",
            "DB_DATABASE": "db",
            "SECRET_KEY": "test-secret-key",
        }

        with mock_environment_variables(individual_config):
            settings = EnvironmentSettings()
            assert settings.configuration_source == "individual_fields"

        # DATABASE_URL only
        url_config = {"DATABASE_URL": "postgresql+asyncpg://user:pass@host:5432/db", "SECRET_KEY": "test-secret-key"}

        with mock_environment_variables(url_config):
            settings = EnvironmentSettings()
            assert settings.configuration_source == "database_url"

        # Mixed configuration
        mixed_config = {
            "DATABASE_URL": "postgresql+asyncpg://user:pass@host:5432/db",
            "DB_HOST": "override-host",
            "SECRET_KEY": "test-secret-key",
        }

        with mock_environment_variables(mixed_config):
            settings = EnvironmentSettings()
            assert settings.configuration_source == "mixed"

    def test_environment_settings_serialization_security(self):
        """Test that sensitive information is excluded from serialization."""
        config = {"SECRET_KEY": "super-secret-key", "DB_PASSWORD": "database-password", "JWT_SECRET": "jwt-secret"}

        with mock_environment_variables(config):
            settings = EnvironmentSettings()

            # Serialize to dict
            settings_dict = settings.model_dump()

            # Sensitive fields should be excluded or masked
            assert settings_dict.get("secret_key") != "super-secret-key"
            assert "database-password" not in str(settings_dict)
            assert "jwt-secret" not in str(settings_dict)
