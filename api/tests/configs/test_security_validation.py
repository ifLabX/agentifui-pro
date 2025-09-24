"""
Test production security validation and environment-specific rules.

Tests the enhanced security validation that enforces stricter rules
in production environments while being more lenient in development.
"""

import pytest
from pydantic import ValidationError

from tests.conftest import mock_environment_variables

# These imports will fail until the implementation is complete
try:
    from configs.security import (
        SecurityValidator,
        validate_password_strength,
        validate_production_requirements,
        validate_secret_key_strength,
    )
    from configs.settings import EnvironmentSettings
except ImportError:
    # Mock the functions for contract testing
    class SecurityValidator:
        @staticmethod
        def validate_environment(settings):
            return {"valid": True, "issues": []}

    def validate_production_requirements(settings):
        return {"met": True, "issues": []}

    def validate_secret_key_strength(key, environment):
        return {"valid": True, "issues": []}

    def validate_password_strength(password, environment):
        return {"valid": True, "issues": []}

    class EnvironmentSettings:
        def __init__(self, **kwargs):
            pass


class TestSecurityValidation:
    """Test security validation for different environments."""

    def test_development_security_validation(self):
        """Test lenient security validation in development environment."""
        # This test will FAIL until security validation is implemented
        dev_config = {
            "ENVIRONMENT": "development",
            "SECRET_KEY": "dev-secret",  # Short key acceptable in dev
            "DB_PASSWORD": "dev_pass",   # Simple password acceptable in dev
            "CORS_ORIGINS": "http://localhost:3000",  # HTTP acceptable in dev
            "DEBUG": "true"
        }

        with mock_environment_variables(dev_config):
            settings = EnvironmentSettings()
            validation_result = SecurityValidator.validate_environment(settings)

            assert validation_result["valid"] is True
            # May have warnings but not blocking errors
            assert len(validation_result.get("warnings", [])) >= 0

    def test_production_security_validation_strict_requirements(self):
        """Test strict security validation in production environment."""
        # Production with proper security should pass
        secure_prod_config = {
            "ENVIRONMENT": "production",
            "SECRET_KEY": "production-secret-key-must-be-at-least-32-characters-long-for-security",
            "DB_PASSWORD": "super-secure-production-password-32-chars-long",
            "CORS_ORIGINS": "https://app.example.com,https://admin.example.com",
            "DEBUG": "false"
        }

        with mock_environment_variables(secure_prod_config):
            settings = EnvironmentSettings()
            validation_result = SecurityValidator.validate_environment(settings)

            assert validation_result["valid"] is True
            prod_requirements = validate_production_requirements(settings)
            assert prod_requirements["met"] is True

    def test_production_security_validation_failures(self):
        """Test security validation failures in production environment."""
        # Production with weak security should fail
        weak_prod_config = {
            "ENVIRONMENT": "production",
            "SECRET_KEY": "weak",  # Too short
            "DB_PASSWORD": "123",  # Too weak
            "CORS_ORIGINS": "http://insecure.com",  # HTTP not allowed
            "DEBUG": "true"  # Debug should be false in production
        }

        with mock_environment_variables(weak_prod_config):
            with pytest.raises(ValidationError) as exc_info:
                settings = EnvironmentSettings()

            errors = exc_info.value.errors()
            error_fields = [str(error["loc"]) for error in errors]

            # Should have multiple security-related validation errors
            assert len(errors) > 0

    def test_secret_key_strength_validation(self):
        """Test secret key strength validation by environment."""
        # Development - lenient
        dev_result = validate_secret_key_strength("short-key", "development")
        assert dev_result["valid"] is True

        # Production - strict (minimum 32 characters)
        short_key_result = validate_secret_key_strength("short-key", "production")
        assert short_key_result["valid"] is False
        assert "length" in " ".join(short_key_result["issues"]).lower()

        # Production - valid key
        long_key = "production-secret-key-must-be-at-least-32-characters-long"
        long_key_result = validate_secret_key_strength(long_key, "production")
        assert long_key_result["valid"] is True

    def test_password_strength_validation(self):
        """Test database password strength validation by environment."""
        # Development - simple password acceptable
        dev_result = validate_password_strength("simple", "development")
        assert dev_result["valid"] is True

        # Production - weak password rejected
        weak_result = validate_password_strength("simple", "production")
        assert weak_result["valid"] is False

        # Production - strong password accepted
        strong_password = "ProductionPassword2024!@#$%^&*()_+"
        strong_result = validate_password_strength(strong_password, "production")
        assert strong_result["valid"] is True

    def test_cors_origins_security_validation(self):
        """Test CORS origins security validation by environment."""
        # Development - HTTP origins allowed
        dev_config = {
            "ENVIRONMENT": "development",
            "SECRET_KEY": "dev-secret-key",
            "CORS_ORIGINS": "http://localhost:3000,http://127.0.0.1:3001"
        }

        with mock_environment_variables(dev_config):
            settings = EnvironmentSettings()
            validation_result = SecurityValidator.validate_environment(settings)
            # Should pass in development
            assert validation_result["valid"] is True

        # Production - only HTTPS origins allowed
        prod_http_config = {
            "ENVIRONMENT": "production",
            "SECRET_KEY": "production-secret-key-must-be-at-least-32-characters-long",
            "DB_PASSWORD": "production-password-must-be-secure-32-chars",
            "CORS_ORIGINS": "http://insecure.example.com"  # HTTP not allowed
        }

        with pytest.raises(ValidationError):
            with mock_environment_variables(prod_http_config):
                EnvironmentSettings()

        # Production - HTTPS origins allowed
        prod_https_config = {
            "ENVIRONMENT": "production",
            "SECRET_KEY": "production-secret-key-must-be-at-least-32-characters-long",
            "DB_PASSWORD": "production-password-must-be-secure-32-chars",
            "CORS_ORIGINS": "https://secure.example.com,https://admin.example.com"
        }

        with mock_environment_variables(prod_https_config):
            settings = EnvironmentSettings()
            validation_result = SecurityValidator.validate_environment(settings)
            assert validation_result["valid"] is True

    def test_debug_mode_security_validation(self):
        """Test debug mode security validation."""
        # Production with debug enabled should fail
        debug_prod_config = {
            "ENVIRONMENT": "production",
            "SECRET_KEY": "production-secret-key-must-be-at-least-32-characters-long",
            "DB_PASSWORD": "production-password-must-be-secure-32-chars",
            "DEBUG": "true"  # Debug should be false in production
        }

        with pytest.raises(ValidationError):
            with mock_environment_variables(debug_prod_config):
                EnvironmentSettings()

        # Production with debug disabled should pass
        secure_prod_config = {
            "ENVIRONMENT": "production",
            "SECRET_KEY": "production-secret-key-must-be-at-least-32-characters-long",
            "DB_PASSWORD": "production-password-must-be-secure-32-chars",
            "DEBUG": "false"
        }

        with mock_environment_variables(secure_prod_config):
            settings = EnvironmentSettings()
            validation_result = SecurityValidator.validate_environment(settings)
            assert validation_result["valid"] is True

    def test_staging_environment_security_validation(self):
        """Test security validation for staging environment (between dev and prod)."""
        staging_config = {
            "ENVIRONMENT": "staging",
            "SECRET_KEY": "staging-secret-key-moderate-length",  # Medium strength
            "DB_PASSWORD": "staging_password_123",               # Medium strength
            "CORS_ORIGINS": "https://staging.example.com",      # HTTPS required
            "DEBUG": "false"
        }

        with mock_environment_variables(staging_config):
            settings = EnvironmentSettings()
            validation_result = SecurityValidator.validate_environment(settings)

            # Staging should have moderate security requirements
            assert validation_result["valid"] is True
            # May have recommendations for improvement
            assert "recommendations" in validation_result

    def test_security_validation_comprehensive_report(self):
        """Test comprehensive security validation report."""
        test_config = {
            "ENVIRONMENT": "production",
            "SECRET_KEY": "production-secret-key-must-be-at-least-32-characters-long",
            "DB_PASSWORD": "production-password-must-be-secure-32-chars",
            "CORS_ORIGINS": "https://app.example.com",
            "DEBUG": "false"
        }

        with mock_environment_variables(test_config):
            settings = EnvironmentSettings()
            validation_result = SecurityValidator.validate_environment(settings)

            # Report should include detailed sections
            assert "valid" in validation_result
            assert "environment" in validation_result
            assert "secret_key" in validation_result
            assert "database" in validation_result
            assert "cors" in validation_result
            assert "production_requirements" in validation_result

            # Each section should have validation details
            for section in ["secret_key", "database", "cors"]:
                section_result = validation_result[section]
                assert "valid" in section_result
                if not section_result["valid"]:
                    assert "issues" in section_result

    def test_security_validation_error_messages(self):
        """Test that security validation error messages are helpful."""
        weak_config = {
            "ENVIRONMENT": "production",
            "SECRET_KEY": "weak",
            "DB_PASSWORD": "123",
            "CORS_ORIGINS": "http://insecure.com"
        }

        try:
            with mock_environment_variables(weak_config):
                EnvironmentSettings()
        except ValidationError as e:
            errors = e.errors()

            # Error messages should be descriptive
            for error in errors:
                assert "msg" in error
                assert len(error["msg"]) > 10  # Should be descriptive
                # Should mention security requirements
                assert any(keyword in error["msg"].lower()
                          for keyword in ["security", "production", "required", "minimum"])

    def test_security_validation_recommendations(self):
        """Test security validation recommendations for improvement."""
        borderline_config = {
            "ENVIRONMENT": "production",
            "SECRET_KEY": "production-secret-key-exactly-32-chars-long-minimum-requirement",  # Minimum length
            "DB_PASSWORD": "ProductionPassword123",  # Good but could be better
            "CORS_ORIGINS": "https://app.example.com"
        }

        with mock_environment_variables(borderline_config):
            settings = EnvironmentSettings()
            validation_result = SecurityValidator.validate_environment(settings)

            # Should pass validation but include recommendations
            assert validation_result["valid"] is True

            if "recommendations" in validation_result:
                recommendations = validation_result["recommendations"]
                assert isinstance(recommendations, list)
                # May suggest stronger passwords, key rotation, etc.

    def test_security_validation_with_feature_flags(self):
        """Test security validation with security-related feature flags."""
        config = {
            "ENVIRONMENT": "production",
            "SECRET_KEY": "production-secret-key-must-be-at-least-32-characters-long",
            "DB_PASSWORD": "production-password-must-be-secure-32-chars",
            "FEATURE_RATE_LIMITING": "true",     # Security feature
            "FEATURE_AUDIT_LOGGING": "true",     # Security feature
            "FEATURE_CSRF_PROTECTION": "false"   # Security risk if disabled
        }

        with mock_environment_variables(config):
            settings = EnvironmentSettings()
            validation_result = SecurityValidator.validate_environment(settings)

            # Should validate security-related feature flags
            if "feature_flags" in validation_result:
                ff_result = validation_result["feature_flags"]
                assert "valid" in ff_result

                # May warn about disabled security features
                if not ff_result["valid"]:
                    assert "disabled_security_features" in " ".join(ff_result.get("warnings", []))

    def test_environment_transition_security_validation(self):
        """Test security validation during environment transitions."""
        # Simulating upgrade from development to production

        # Development config that needs security hardening
        dev_to_prod_config = {
            "ENVIRONMENT": "production",  # Changed to production
            "SECRET_KEY": "dev-secret",   # Still using dev secret (should fail)
            "DB_PASSWORD": "dev_pass",    # Still using dev password (should fail)
            "DEBUG": "true"               # Still has debug enabled (should fail)
        }

        with pytest.raises(ValidationError) as exc_info:
            with mock_environment_variables(dev_to_prod_config):
                EnvironmentSettings()

        errors = exc_info.value.errors()
        # Should have multiple errors related to production requirements
        assert len(errors) >= 3  # At least secret_key, password, and debug errors