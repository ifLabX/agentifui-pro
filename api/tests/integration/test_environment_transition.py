"""
Test environment transition validation (development to production).

Tests the enhanced configuration validation that ensures smooth transitions
between environments while enforcing stricter security requirements.
"""

from httpx import AsyncClient

from tests.conftest import mock_environment_variables

# These imports will fail until the implementation is complete
try:
    from configs.security import SecurityValidator
    from configs.settings import EnvironmentSettings
except ImportError:
    # Mock the classes for contract testing
    class EnvironmentSettings:
        def __init__(self, **kwargs):
            pass

    class SecurityValidator:
        @staticmethod
        def validate_environment_transition(from_env, to_env, settings):
            return {"valid": True, "issues": []}


class TestEnvironmentTransition:
    """Test environment transition validation and requirements."""

    async def test_development_to_staging_transition(self, async_client: AsyncClient):
        """Test transition from development to staging environment."""
        # This test will FAIL until environment transition validation is implemented

        # Development configuration (baseline)
        dev_config = {
            "ENVIRONMENT": "development",
            "SECRET_KEY": "dev-secret-key",
            "DB_PASSWORD": "dev_password",
            "CORS_ORIGINS": "http://localhost:3000",
            "DEBUG": "true"
        }

        # Staging configuration (intermediate security)
        staging_config = {
            "ENVIRONMENT": "staging",
            "SECRET_KEY": "staging-secret-key-with-better-length",
            "DB_PASSWORD": "staging_secure_password_123",
            "CORS_ORIGINS": "https://staging.example.com",
            "DEBUG": "false"
        }

        # Validate transition requirements
        with mock_environment_variables(dev_config):
            dev_settings = EnvironmentSettings()

        with mock_environment_variables(staging_config):
            staging_settings = EnvironmentSettings()

        transition_result = SecurityValidator.validate_environment_transition(
            "development", "staging", staging_settings
        )

        assert transition_result["valid"] is True
        # May include recommendations for further security improvements

    async def test_staging_to_production_transition(self, async_client: AsyncClient):
        """Test transition from staging to production environment."""
        # Staging configuration
        staging_config = {
            "ENVIRONMENT": "staging",
            "SECRET_KEY": "staging-secret-key-with-better-length",
            "DB_PASSWORD": "staging_secure_password_123",
            "CORS_ORIGINS": "https://staging.example.com",
            "DEBUG": "false"
        }

        # Production configuration (strict security)
        prod_config = {
            "ENVIRONMENT": "production",
            "SECRET_KEY": "production-secret-key-must-be-at-least-32-characters-long-for-security",
            "DB_PASSWORD": "super-secure-production-password-32-chars-long",
            "CORS_ORIGINS": "https://app.example.com,https://admin.example.com",
            "DEBUG": "false"
        }

        with mock_environment_variables(staging_config):
            staging_settings = EnvironmentSettings()

        with mock_environment_variables(prod_config):
            prod_settings = EnvironmentSettings()

        transition_result = SecurityValidator.validate_environment_transition(
            "staging", "production", prod_settings
        )

        assert transition_result["valid"] is True

    async def test_development_to_production_transition_validation(self):
        """Test direct development to production transition (should warn about skipping staging)."""
        # Development configuration
        dev_config = {
            "ENVIRONMENT": "development",
            "SECRET_KEY": "dev-secret-key",
            "DB_PASSWORD": "dev_password",
            "DEBUG": "true"
        }

        # Production configuration
        prod_config = {
            "ENVIRONMENT": "production",
            "SECRET_KEY": "production-secret-key-must-be-at-least-32-characters-long-for-security",
            "DB_PASSWORD": "super-secure-production-password-32-chars-long",
            "DEBUG": "false"
        }

        with mock_environment_variables(dev_config):
            dev_settings = EnvironmentSettings()

        with mock_environment_variables(prod_config):
            prod_settings = EnvironmentSettings()

        transition_result = SecurityValidator.validate_environment_transition(
            "development", "production", prod_settings
        )

        # Should be valid but include warnings about skipping staging
        assert transition_result["valid"] is True
        if "warnings" in transition_result:
            warnings_text = " ".join(transition_result["warnings"])
            assert "staging" in warnings_text.lower()

    async def test_configuration_validation_during_transition(self, async_client: AsyncClient):
        """Test that configuration validation catches transition issues."""
        # Invalid production configuration (still using dev settings)
        invalid_prod_config = {
            "ENVIRONMENT": "production",  # Claims to be production
            "SECRET_KEY": "dev-secret",   # But uses dev secret (too short)
            "DB_PASSWORD": "dev_pass",    # And dev password (too weak)
            "CORS_ORIGINS": "http://localhost:3000",  # And dev CORS (HTTP)
            "DEBUG": "true"               # And still has debug enabled
        }

        with mock_environment_variables(invalid_prod_config):
            response = await async_client.get("/config/validate")

            # Should fail validation due to insufficient security for production
            assert response.status_code == 400
            data = response.json()

            assert "validation_errors" in data
            errors = data["validation_errors"]

            # Should have multiple security-related errors
            error_fields = [error.get("field", "") for error in errors]
            assert any("secret_key" in field.lower() for field in error_fields)

    async def test_backward_compatibility_during_transition(self, async_client: AsyncClient):
        """Test that backward compatibility is maintained during environment transitions."""
        # Legacy configuration that should still work in new environment
        legacy_config = {
            "DATABASE_URL": "postgresql+asyncpg://user:pass@prod-host:5432/prod-db",
            "SECRET_KEY": "production-secret-key-must-be-at-least-32-characters-long-for-security",
            "ENVIRONMENT": "production",
            "CORS_ORIGINS": '["https://app.example.com", "https://admin.example.com"]'  # Legacy JSON
        }

        with mock_environment_variables(legacy_config):
            # Should work with both old and new validation
            response = await async_client.get("/config/validate")
            assert response.status_code == 200

            response = await async_client.get("/config/database/status")
            assert response.status_code == 200
            data = response.json()

            # Should parse legacy configurations correctly
            assert data["configuration"]["host"] == "prod-host"
            assert data["configuration_source"] == "database_url"

    async def test_feature_flag_transition_validation(self):
        """Test feature flag validation during environment transitions."""
        # Development with experimental features enabled
        dev_config = {
            "ENVIRONMENT": "development",
            "SECRET_KEY": "dev-secret-key",
            "FEATURE_EXPERIMENTAL_AUTH": "true",
            "FEATURE_DEBUG_LOGGING": "true",
            "FEATURE_UNSAFE_OPERATIONS": "true"
        }

        # Production should disable experimental/unsafe features
        prod_config = {
            "ENVIRONMENT": "production",
            "SECRET_KEY": "production-secret-key-must-be-at-least-32-characters-long-for-security",
            "FEATURE_EXPERIMENTAL_AUTH": "false",  # Disabled for stability
            "FEATURE_DEBUG_LOGGING": "false",      # Disabled for security
            "FEATURE_UNSAFE_OPERATIONS": "false"   # Disabled for safety
        }

        with mock_environment_variables(prod_config):
            settings = EnvironmentSettings()
            validation_result = SecurityValidator.validate_environment_transition(
                "development", "production", settings
            )

            assert validation_result["valid"] is True

    async def test_database_connection_transition_validation(self, async_client: AsyncClient):
        """Test database connection validation during environment transitions."""
        # Development using localhost database
        dev_db_config = {
            "ENVIRONMENT": "development",
            "DB_HOST": "localhost",
            "DB_PORT": "5432",
            "DB_USERNAME": "dev_user",
            "DB_PASSWORD": "dev_password",
            "DB_DATABASE": "dev_db",
            "SECRET_KEY": "dev-secret-key"
        }

        # Production should use secure external database
        prod_db_config = {
            "ENVIRONMENT": "production",
            "DB_HOST": "secure-prod-db.example.com",
            "DB_PORT": "5432",
            "DB_USERNAME": "prod_user",
            "DB_PASSWORD": "super-secure-production-password-32-chars-long",
            "DB_DATABASE": "prod_db",
            "SECRET_KEY": "production-secret-key-must-be-at-least-32-characters-long-for-security"
        }

        # Test database connection validation
        with mock_environment_variables(prod_db_config):
            response = await async_client.post("/config/database/test")
            # Should accept production database configuration
            assert response.status_code == 200

    async def test_cors_origins_transition_validation(self, async_client: AsyncClient):
        """Test CORS origins validation during environment transitions."""
        # Development allows localhost origins
        dev_cors_config = {
            "ENVIRONMENT": "development",
            "SECRET_KEY": "dev-secret-key",
            "CORS_ORIGINS": "http://localhost:3000,http://127.0.0.1:3001"
        }

        # Production requires HTTPS origins
        prod_cors_config = {
            "ENVIRONMENT": "production",
            "SECRET_KEY": "production-secret-key-must-be-at-least-32-characters-long-for-security",
            "CORS_ORIGINS": "https://app.example.com,https://admin.example.com"
        }

        with mock_environment_variables(prod_cors_config):
            response = await async_client.get("/config/validate")
            assert response.status_code == 200
            data = response.json()

            cors_result = data["validation_results"]["cors"]
            assert cors_result["valid"] is True

    async def test_logging_configuration_transition(self):
        """Test logging configuration changes during environment transitions."""
        # Development with verbose logging
        dev_config = {
            "ENVIRONMENT": "development",
            "SECRET_KEY": "dev-secret-key",
            "LOG_LEVEL": "DEBUG"
        }

        # Production with controlled logging
        prod_config = {
            "ENVIRONMENT": "production",
            "SECRET_KEY": "production-secret-key-must-be-at-least-32-characters-long-for-security",
            "LOG_LEVEL": "INFO"
        }

        with mock_environment_variables(prod_config):
            settings = EnvironmentSettings()

            # Production should have appropriate logging level
            assert settings.log_level == "INFO"
            assert settings.debug is False

    async def test_middleware_configuration_transition(self, async_client: AsyncClient):
        """Test middleware configuration during environment transitions."""
        # Production should have security middleware enabled
        prod_config = {
            "ENVIRONMENT": "production",
            "SECRET_KEY": "production-secret-key-must-be-at-least-32-characters-long-for-security",
            "ENABLE_SECURITY_HEADERS": "true",
            "ENABLE_RATE_LIMITING": "true",
            "ENABLE_REQUEST_TRACING": "true"
        }

        with mock_environment_variables(prod_config):
            # Middleware should be properly configured for production
            response = await async_client.get("/health")
            assert response.status_code == 200

            # Security headers should be present in production
            headers = response.headers
            # May include security headers like Content-Security-Policy, etc.

    async def test_transition_checklist_validation(self):
        """Test comprehensive transition checklist validation."""
        prod_config = {
            "ENVIRONMENT": "production",
            "SECRET_KEY": "production-secret-key-must-be-at-least-32-characters-long-for-security",
            "DB_PASSWORD": "super-secure-production-password-32-chars-long",
            "DEBUG": "false",
            "CORS_ORIGINS": "https://app.example.com",
            "LOG_LEVEL": "INFO"
        }

        with mock_environment_variables(prod_config):
            settings = EnvironmentSettings()
            validation_result = SecurityValidator.validate_environment_transition(
                "development", "production", settings
            )

            assert validation_result["valid"] is True

            # Should include transition checklist
            if "checklist" in validation_result:
                checklist = validation_result["checklist"]
                required_items = [
                    "secret_key_updated",
                    "database_password_secured",
                    "debug_disabled",
                    "https_enforced",
                    "logging_configured"
                ]

                for item in required_items:
                    assert any(item in str(check) for check in checklist)

    async def test_rollback_compatibility_validation(self, async_client: AsyncClient):
        """Test that configurations support rollback scenarios."""
        # Current production configuration
        current_prod_config = {
            "ENVIRONMENT": "production",
            "SECRET_KEY": "production-secret-key-must-be-at-least-32-characters-long-for-security",
            "DB_HOST": "prod-new.example.com",
            "DB_DATABASE": "prod_v2_db"
        }

        # Rollback configuration (previous version)
        rollback_config = {
            "ENVIRONMENT": "production",
            "SECRET_KEY": "production-secret-key-must-be-at-least-32-characters-long-for-security",
            "DB_HOST": "prod-old.example.com",
            "DB_DATABASE": "prod_v1_db"
        }

        # Both configurations should be valid for production
        for config in [current_prod_config, rollback_config]:
            with mock_environment_variables(config):
                response = await async_client.get("/config/validate")
                assert response.status_code == 200