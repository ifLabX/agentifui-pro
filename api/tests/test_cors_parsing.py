"""
CORS origins parsing format tests.

Tests to verify that different environment variable formats for CORS_ORIGINS
are correctly parsed by the configuration system.
"""

import os
from unittest.mock import patch


def test_cors_origins_comma_separated_format():
    """Test CORS origins with comma-separated format."""
    from core.config import Settings, reset_settings

    # Test single origin
    with patch.dict(
        os.environ,
        {
            "DATABASE_URL": "postgresql+asyncpg://user:pass@localhost:5432/test",
            "CORS_ORIGINS": "http://localhost:3000",
        },
        clear=True,
    ):
        reset_settings()
        settings = Settings()
        assert settings.cors_origins == ["http://localhost:3000"]

    # Test multiple origins with comma separation
    with patch.dict(
        os.environ,
        {
            "DATABASE_URL": "postgresql+asyncpg://user:pass@localhost:5432/test",
            "CORS_ORIGINS": "http://localhost:3000,http://localhost:3001,https://example.com",
        },
        clear=True,
    ):
        reset_settings()
        settings = Settings()
        assert len(settings.cors_origins) == 3
        assert "http://localhost:3000" in settings.cors_origins
        assert "http://localhost:3001" in settings.cors_origins
        assert "https://example.com" in settings.cors_origins


def test_cors_origins_json_array_format():
    """Test CORS origins with JSON array format."""
    from core.config import Settings, reset_settings

    # Test JSON array format with single quotes
    with patch.dict(
        os.environ,
        {
            "DATABASE_URL": "postgresql+asyncpg://user:pass@localhost:5432/test",
            "CORS_ORIGINS": '["http://localhost:3000"]',
        },
        clear=True,
    ):
        reset_settings()
        settings = Settings()
        assert settings.cors_origins == ["http://localhost:3000"]

    # Test JSON array format with multiple origins
    with patch.dict(
        os.environ,
        {
            "DATABASE_URL": "postgresql+asyncpg://user:pass@localhost:5432/test",
            "CORS_ORIGINS": '["http://localhost:3000","https://example.com","https://app.example.com"]',
        },
        clear=True,
    ):
        reset_settings()
        settings = Settings()
        assert len(settings.cors_origins) == 3
        assert "http://localhost:3000" in settings.cors_origins
        assert "https://example.com" in settings.cors_origins
        assert "https://app.example.com" in settings.cors_origins


def test_cors_origins_with_spaces():
    """Test CORS origins with spaces in comma-separated format."""
    from core.config import Settings, reset_settings

    # Test with spaces around commas
    with patch.dict(
        os.environ,
        {
            "DATABASE_URL": "postgresql+asyncpg://user:pass@localhost:5432/test",
            "CORS_ORIGINS": "http://localhost:3000, http://localhost:3001, https://example.com",
        },
        clear=True,
    ):
        reset_settings()
        settings = Settings()
        assert len(settings.cors_origins) == 3
        # Verify that spaces are stripped
        assert "http://localhost:3000" in settings.cors_origins
        assert "http://localhost:3001" in settings.cors_origins
        assert "https://example.com" in settings.cors_origins


def test_cors_methods_parsing():
    """Test CORS methods parsing with different formats."""
    from core.config import Settings, reset_settings

    # Test comma-separated methods
    with patch.dict(
        os.environ,
        {
            "DATABASE_URL": "postgresql+asyncpg://user:pass@localhost:5432/test",
            "CORS_ALLOW_METHODS": "GET,POST,PUT,DELETE",
        },
        clear=True,
    ):
        reset_settings()
        settings = Settings()
        assert len(settings.cors_allow_methods) == 4
        assert "GET" in settings.cors_allow_methods
        assert "POST" in settings.cors_allow_methods

    # Test JSON array format
    with patch.dict(
        os.environ,
        {
            "DATABASE_URL": "postgresql+asyncpg://user:pass@localhost:5432/test",
            "CORS_ALLOW_METHODS": '["GET","POST","PUT","DELETE","PATCH"]',
        },
        clear=True,
    ):
        reset_settings()
        settings = Settings()
        assert len(settings.cors_allow_methods) == 5
        assert "PATCH" in settings.cors_allow_methods


def test_cors_headers_parsing():
    """Test CORS headers parsing with different formats."""
    from core.config import Settings, reset_settings

    # Test comma-separated headers
    with patch.dict(
        os.environ,
        {
            "DATABASE_URL": "postgresql+asyncpg://user:pass@localhost:5432/test",
            "CORS_ALLOW_HEADERS": "Content-Type,Authorization,X-Request-ID",
        },
        clear=True,
    ):
        reset_settings()
        settings = Settings()
        assert len(settings.cors_allow_headers) == 3
        assert "Content-Type" in settings.cors_allow_headers
        assert "Authorization" in settings.cors_allow_headers

    # Test JSON array format
    with patch.dict(
        os.environ,
        {
            "DATABASE_URL": "postgresql+asyncpg://user:pass@localhost:5432/test",
            "CORS_ALLOW_HEADERS": '["Content-Type","Authorization","X-Custom-Header"]',
        },
        clear=True,
    ):
        reset_settings()
        settings = Settings()
        assert len(settings.cors_allow_headers) == 3
        assert "X-Custom-Header" in settings.cors_allow_headers


def test_cors_wildcard_format():
    """Test CORS with wildcard (*) format."""
    from core.config import Settings, reset_settings

    # Test single asterisk
    with patch.dict(
        os.environ,
        {
            "DATABASE_URL": "postgresql+asyncpg://user:pass@localhost:5432/test",
            "CORS_ALLOW_METHODS": "*",
        },
        clear=True,
    ):
        reset_settings()
        settings = Settings()
        assert settings.cors_allow_methods == ["*"]

    # Test JSON array with asterisk
    with patch.dict(
        os.environ,
        {
            "DATABASE_URL": "postgresql+asyncpg://user:pass@localhost:5432/test",
            "CORS_ALLOW_HEADERS": '["*"]',
        },
        clear=True,
    ):
        reset_settings()
        settings = Settings()
        assert settings.cors_allow_headers == ["*"]
