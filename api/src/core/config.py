"""
Application configuration management with Pydantic Settings.

This module provides type-safe configuration management using environment variables
with validation and default values.
"""

import asyncio
import tomllib
from functools import lru_cache
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from typing import Any

from pydantic import Field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


def _load_pyproject_version(pyproject_path: Path) -> str:
    """
    Read the version from pyproject.toml to keep development parity with the packaged build.
    """
    if not pyproject_path.is_file():
        return "0.0.0"

    try:
        with pyproject_path.open("rb") as pyproject_file:
            project = tomllib.load(pyproject_file)
    except tomllib.TOMLDecodeError:
        return "0.0.0"

    project_version = project.get("project", {}).get("version")
    if isinstance(project_version, str):
        return project_version

    return "0.0.0"


def _resolve_app_version(pyproject_path: Path | None = None) -> str:
    """
    Prefer the installed package metadata, falling back to pyproject.toml when running from source.
    """
    try:
        return version("agentifui-pro-api")
    except PackageNotFoundError:
        resolved_pyproject = pyproject_path or Path(__file__).resolve().parents[2] / "pyproject.toml"
        return _load_pyproject_version(resolved_pyproject)


__version__ = _resolve_app_version()


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    All settings are validated using Pydantic and provide type safety.
    """

    # Application Settings
    # Keep version aligned with package metadata in all environments
    app_name: str = Field(default="Agentifui Pro API")
    app_version: str = Field(default=__version__)
    app_description: str = Field(default="Backend API for Agentifui Pro")
    debug: bool = Field(default=False)

    # Server Configuration
    host: str = Field(default="0.0.0.0")
    port: int = Field(default=8000, gt=0, le=65535)

    # Database Configuration
    database_url: str = Field(...)
    database_pool_size: int = Field(default=10, gt=0, le=100)
    database_pool_max_overflow: int = Field(default=20, ge=0, le=100)
    database_pool_timeout: int = Field(default=30, gt=0, le=300)
    database_pool_recycle: int = Field(default=3600, gt=0)

    # Redis Configuration
    redis_url: str = Field(...)
    redis_pool_max_connections: int = Field(default=50, gt=0, le=1000)
    redis_socket_connect_timeout: float = Field(default=5.0, gt=0, le=60)
    redis_socket_timeout: float = Field(default=5.0, gt=0, le=60)
    redis_health_check_timeout: float = Field(default=2.0, gt=0, le=30)
    redis_health_check_interval: int = Field(default=30, ge=0, le=3600)
    redis_key_prefix: str = Field(default="agentifui-pro")
    redis_default_ttl_seconds: int = Field(default=3600, gt=0, le=604800)

    # Health Check Configuration
    health_check_timeout: int = Field(default=5, gt=0, le=30)
    database_health_check_timeout: int = Field(default=10, gt=0, le=60)

    # Logging Configuration
    log_level: str = Field(default="INFO")
    log_format: str = Field(default="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    # CORS Settings
    cors_origins: str | list[str] = Field(default=["http://localhost:3000"])
    cors_allow_credentials: bool = Field(default=True)
    cors_allow_methods: str | list[str] = Field(default=["*"])
    cors_allow_headers: str | list[str] = Field(default=["*"])

    # Environment
    environment: str = Field(default="development")

    # Feature Flags
    enable_docs: bool = Field(default=True)
    enable_redoc: bool = Field(default=True)

    @field_validator("database_url")
    @classmethod
    def validate_database_url(cls, v: str) -> str:
        """Validate that database URL is a PostgreSQL connection string."""
        if not v.startswith(("postgresql://", "postgresql+asyncpg://")):
            raise ValueError("Database URL must be a PostgreSQL connection string")
        return v

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Validate that log level is one of the allowed values."""
        allowed_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in allowed_levels:
            raise ValueError(f"Log level must be one of: {allowed_levels}")
        return v.upper()

    @field_validator("environment")
    @classmethod
    def validate_environment(cls, v: str) -> str:
        """Validate that environment is one of the allowed values."""
        allowed_envs = ["development", "staging", "production"]
        if v.lower() not in allowed_envs:
            raise ValueError(f"Environment must be one of: {allowed_envs}")
        return v.lower()

    @field_validator("redis_url")
    @classmethod
    def validate_redis_url(cls, v: str) -> str:
        """Validate that Redis URL is well-formed."""
        if not v.startswith(("redis://", "rediss://")):
            raise ValueError("Redis URL must start with redis:// or rediss://")
        return v

    @field_validator("redis_key_prefix")
    @classmethod
    def validate_redis_key_prefix(cls, v: str) -> str:
        """Ensure Redis key prefix is non-empty."""
        if not v.strip():
            raise ValueError("Redis key prefix cannot be empty")
        return v.strip()

    @model_validator(mode="before")
    @classmethod
    def parse_cors_fields(cls, data: dict[str, Any]) -> dict[str, Any]:
        """
        Parse CORS fields from string (comma-separated or JSON) to list.

        Supports multiple formats:
        - JSON array: '["http://localhost:3000","http://localhost:3001"]'
        - Comma-separated: 'http://localhost:3000,http://localhost:3001'
        - Single value: 'http://localhost:3000'
        """
        import json

        # Process all CORS list fields
        cors_list_fields = ["cors_origins", "cors_allow_methods", "cors_allow_headers"]

        for field_name in cors_list_fields:
            if field_name in data and isinstance(data[field_name], str):
                value = data[field_name]
                try:
                    # Try JSON parsing first
                    data[field_name] = json.loads(value)
                except json.JSONDecodeError:
                    # Fall back to comma-separated parsing
                    data[field_name] = [item.strip() for item in value.split(",")]

        return data

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        # Make settings immutable
        frozen=True,
        extra="ignore",  # Ignore extra fields for now
    )


@lru_cache
def get_settings() -> Settings:
    """
    Get application settings instance.

    Uses LRU cache to ensure singleton pattern - settings are loaded once
    and reused throughout the application lifecycle.

    Returns:
        Settings: Application settings instance
    """
    return Settings()


def reset_settings() -> None:
    """
    Clear settings cache for testing or environment reloading.

    Use this in tests when you need to reload settings with new environment
    variables or when switching between different configurations.

    Example:
        >>> from unittest.mock import patch
        >>> import os
        >>> with patch.dict(os.environ, {"DATABASE_URL": "postgresql://..."}):
        ...     reset_settings()
        ...     settings = get_settings()  # Gets fresh settings with new URL
    """
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        get_settings.cache_clear()
        # Reset Redis client to ensure new settings are applied
        from src.core.redis import reset_redis_client_blocking

        reset_redis_client_blocking()
        return

    raise RuntimeError("reset_settings cannot run inside an active event loop; use reset_settings_async instead.")


async def reset_settings_async() -> None:
    """
    Async variant to clear settings and reset Redis when already in an event loop.
    """
    get_settings.cache_clear()
    from src.core.redis import reset_redis_client

    await reset_redis_client()


# Export settings instance for convenience
settings = get_settings()
