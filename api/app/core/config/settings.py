"""
Application configuration management using Pydantic Settings.
Handles environment-based configuration with validation.
"""

from functools import lru_cache
from typing import Any

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings with environment variable support.

    All settings can be overridden via environment variables.
    Boolean values should use: true/false, 1/0, yes/no, on/off
    """

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=False, extra="ignore")

    # Project Information
    project_name: str = Field(default="AgentifUI-Pro Backend", description="Name of the application")
    project_version: str = Field(default="1.0.0", description="Version of the application")
    debug: bool = Field(default=False, description="Enable debug mode")

    # Database Configuration
    database_url: str = Field(default="sqlite+aiosqlite:///./agentifui_pro.db", description="Database connection URL")

    # API Configuration
    api_v1_prefix: str = Field(default="/api/v1", description="API v1 prefix path")

    # Server Configuration
    host: str = Field(default="0.0.0.0", description="Server host address")
    port: int = Field(default=8000, ge=1, le=65535, description="Server port number")

    # CORS Configuration
    cors_origins: list[str] = Field(
        default=["http://localhost:3000", "http://127.0.0.1:3000"],
        description="Allowed CORS origins for frontend integration",
    )

    # Security Configuration
    secret_key: str = Field(
        default="your-secret-key-change-in-production",
        min_length=32,
        description="Secret key for security operations (must be 32+ chars)",
    )
    access_token_expire_minutes: int = Field(
        default=30, ge=1, le=1440, description="JWT access token expiration time in minutes (max 24h)"
    )

    # Security Features
    enable_security_headers: bool = Field(default=True, description="Enable security headers (HSTS, CSP, etc.)")
    trusted_hosts: list[str] = Field(
        default=["localhost", "127.0.0.1", "testserver"], description="Trusted host names for security"
    )

    # Logging Configuration
    log_level: str = Field(default="INFO", description="Logging level")

    # Development Features
    enable_docs: bool = Field(default=True, description="Enable OpenAPI documentation endpoints")
    enable_redoc: bool = Field(default=True, description="Enable ReDoc documentation endpoint")

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Validate log level is one of the standard levels."""
        valid_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        upper_v = v.upper()
        if upper_v not in valid_levels:
            raise ValueError(f"log_level must be one of: {', '.join(valid_levels)}")
        return upper_v

    @field_validator("database_url")
    @classmethod
    def validate_database_url(cls, v: str) -> str:
        """Validate database URL format."""
        if not v:
            raise ValueError("database_url cannot be empty")

        # Basic URL format validation
        valid_schemes = ["postgresql", "postgresql+asyncpg", "sqlite+aiosqlite"]
        scheme = v.split("://")[0] if "://" in v else ""

        if scheme not in valid_schemes:
            raise ValueError(f"database_url scheme must be one of: {', '.join(valid_schemes)}")

        return v

    @field_validator("secret_key")
    @classmethod
    def validate_secret_key(cls, v: str) -> str:
        """Validate secret key security."""
        if v == "your-secret-key-change-in-production":
            raise ValueError(
                "Secret key must be changed from default value. "
                'Generate a secure key using: python -c "import secrets; print(secrets.token_urlsafe(32))"'
            )

        # Check for common weak patterns
        weak_patterns = ["password", "secret", "key", "123", "abc"]
        v_lower = v.lower()
        for pattern in weak_patterns:
            if pattern in v_lower:
                raise ValueError(f"Secret key appears to contain weak pattern: {pattern}")

        return v

    @field_validator("cors_origins")
    @classmethod
    def validate_cors_origins(cls, v: list[str]) -> list[str]:
        """Validate CORS origins and warn about security."""
        if not v:
            raise ValueError("cors_origins cannot be empty")

        # Check for overly permissive CORS
        if "*" in v:
            raise ValueError("Wildcard (*) CORS origin is not allowed for security reasons")

        # Ensure localhost origins are present for development
        dev_origins = ["http://localhost:3000", "http://127.0.0.1:3000"]
        for origin in dev_origins:
            if origin not in v:
                v.append(origin)

        return v

    @property
    def is_development(self) -> bool:
        """Check if running in development mode."""
        return self.debug

    @property
    def is_production(self) -> bool:
        """Check if running in production mode."""
        return not self.debug

    def get_database_config(self) -> dict[str, Any]:
        """Get database configuration for SQLAlchemy."""
        config = {
            "url": self.database_url,
            "echo": self.debug,  # Log SQL queries in debug mode
        }

        # PostgreSQL specific configuration
        if "postgresql" in self.database_url:
            config.update(
                {
                    "pool_size": 20,
                    "max_overflow": 30,
                    "pool_timeout": 30,
                    "pool_recycle": 1800,  # 30 minutes
                    "pool_pre_ping": True,
                }
            )

        return config


@lru_cache
def get_settings() -> Settings:
    """
    Get application settings instance.

    Uses LRU cache to ensure settings are only loaded once.
    """
    return Settings()
