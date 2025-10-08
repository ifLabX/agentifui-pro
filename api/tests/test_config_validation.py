"""
Configuration validation tests.

These tests validate that configuration management works correctly with Pydantic Settings.
Tests MUST fail until configuration system is implemented.
"""

import os
from unittest.mock import patch

import pytest


def test_config_settings_class_exists():
    """Test that Settings configuration class exists."""
    try:
        from core.config import Settings

        # Verify the class can be instantiated
        assert Settings is not None
        assert hasattr(Settings, "model_config")
    except ImportError:
        pytest.fail("Settings class must exist in core.config module")


def test_config_settings_has_required_fields():
    """Test that Settings class has all required configuration fields."""
    from core.config import Settings

    # Create instance to check fields
    settings = Settings()

    # Required application settings
    assert hasattr(settings, "app_name")
    assert hasattr(settings, "app_version")
    assert hasattr(settings, "debug")

    # Required database settings
    assert hasattr(settings, "database_url")
    assert hasattr(settings, "database_pool_size")
    assert hasattr(settings, "database_pool_timeout")

    # Required logging settings
    assert hasattr(settings, "log_level")


def test_config_database_url_validation():
    """Test that database URL validation works correctly."""
    from core.config import Settings

    # Test with valid PostgreSQL URL
    with patch.dict(os.environ, {"DATABASE_URL": "postgresql+asyncpg://user:pass@localhost:5432/test"}):
        settings = Settings()
        assert "postgresql+asyncpg" in settings.database_url

    # Test with invalid URL should raise validation error
    with patch.dict(os.environ, {"DATABASE_URL": "invalid-url"}):
        with pytest.raises(ValueError):  # Should raise Pydantic validation error
            Settings()


def test_config_pool_size_validation():
    """Test that database pool size validation works correctly."""
    from core.config import Settings

    # Test with valid pool size
    with patch.dict(
        os.environ, {"DATABASE_POOL_SIZE": "10", "DATABASE_URL": "postgresql+asyncpg://user:pass@localhost:5432/test"}
    ):
        settings = Settings()
        assert settings.database_pool_size == 10

    # Test with invalid pool size
    with patch.dict(
        os.environ, {"DATABASE_POOL_SIZE": "-1", "DATABASE_URL": "postgresql+asyncpg://user:pass@localhost:5432/test"}
    ):
        with pytest.raises(ValueError):  # Should raise validation error
            Settings()


def test_config_log_level_validation():
    """Test that log level validation works correctly."""
    from core.config import Settings

    valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

    for level in valid_levels:
        with patch.dict(
            os.environ, {"LOG_LEVEL": level, "DATABASE_URL": "postgresql+asyncpg://user:pass@localhost:5432/test"}
        ):
            settings = Settings()
            assert settings.log_level == level

    # Test with invalid log level
    with patch.dict(
        os.environ, {"LOG_LEVEL": "INVALID", "DATABASE_URL": "postgresql+asyncpg://user:pass@localhost:5432/test"}
    ):
        with pytest.raises(ValueError):  # Should raise validation error
            Settings()


def test_config_environment_defaults():
    """Test that configuration provides sensible defaults."""
    from core.config import Settings

    # Test with minimal environment
    with patch.dict(os.environ, {"DATABASE_URL": "postgresql+asyncpg://user:pass@localhost:5432/test"}, clear=True):
        settings = Settings()

        # Should have defaults for non-required fields
        assert settings.app_name is not None
        assert settings.app_version is not None
        assert settings.debug is not None
        assert settings.log_level is not None
        assert settings.database_pool_size > 0


def test_config_cors_settings():
    """Test that CORS settings are properly configured."""
    from core.config import Settings

    with patch.dict(
        os.environ,
        {
            "DATABASE_URL": "postgresql+asyncpg://user:pass@localhost:5432/test",
            "CORS_ORIGINS": '["http://localhost:3000"]',
        },
    ):
        settings = Settings()

        assert hasattr(settings, "cors_origins")
        if settings.cors_origins:
            assert isinstance(settings.cors_origins, list)


def test_config_health_check_settings():
    """Test that health check timeout settings are properly configured."""
    from core.config import Settings

    with patch.dict(
        os.environ,
        {
            "DATABASE_URL": "postgresql+asyncpg://user:pass@localhost:5432/test",
            "HEALTH_CHECK_TIMEOUT": "5",
            "DATABASE_HEALTH_CHECK_TIMEOUT": "10",
        },
    ):
        settings = Settings()

        assert hasattr(settings, "health_check_timeout")
        assert hasattr(settings, "database_health_check_timeout")

        if hasattr(settings, "health_check_timeout"):
            assert settings.health_check_timeout > 0

        if hasattr(settings, "database_health_check_timeout"):
            assert settings.database_health_check_timeout > 0


def test_config_feature_flags():
    """Test that feature flag settings work correctly."""
    from core.config import Settings

    with patch.dict(
        os.environ,
        {
            "DATABASE_URL": "postgresql+asyncpg://user:pass@localhost:5432/test",
            "USE_UUIDV7": "true",
            "ENABLE_DOCS": "false",
        },
    ):
        settings = Settings()

        # Feature flags should be boolean
        if hasattr(settings, "use_uuidv7"):
            assert isinstance(settings.use_uuidv7, bool)

        if hasattr(settings, "enable_docs"):
            assert isinstance(settings.enable_docs, bool)


def test_config_settings_immutable():
    """Test that settings are immutable after creation."""
    from core.config import Settings

    with patch.dict(os.environ, {"DATABASE_URL": "postgresql+asyncpg://user:pass@localhost:5432/test"}):
        settings = Settings()

        # Attempt to modify should raise error (if using frozen=True)
        with pytest.raises((ValueError, TypeError)):
            settings.app_name = "modified"


def test_config_singleton_pattern():
    """Test that settings follow singleton pattern if implemented."""
    try:
        from core.config import get_settings
    except ImportError:
        # Singleton pattern not implemented, skip test
        pytest.skip("Singleton pattern not implemented")

    # If get_settings exists, test singleton behavior
    settings1 = get_settings()
    settings2 = get_settings()

    assert settings1 is settings2, "Settings should follow singleton pattern"


def test_config_validation_errors_descriptive():
    """Test that configuration validation errors are descriptive."""
    from core.config import Settings

    # Test missing required field
    with patch.dict(os.environ, {}, clear=True):
        try:
            Settings(_env_file=None)
            pytest.fail("Should raise validation error for missing DATABASE_URL")
        except Exception as e:
            # Error message should mention the missing field
            error_str = str(e).lower()
            assert "database_url" in error_str or "field required" in error_str
