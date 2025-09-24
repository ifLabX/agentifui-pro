"""
Enhanced application configuration management with Pydantic Settings.

This module provides the enhanced EnvironmentSettings class with comprehensive
configuration management, field validation, environment-specific rules, and
backward compatibility with existing configurations.
"""

import json
import warnings
from functools import lru_cache
from typing import Optional, Union

from pydantic import ConfigDict, Field, computed_field, field_validator
from pydantic.types import SecretStr
from pydantic_settings import BaseSettings

from .database import DatabaseConfig


class EnvironmentSettings(BaseSettings):
    """
    Enhanced environment settings with comprehensive configuration management.

    Provides flexible database configuration, environment-specific validation,
    enhanced CORS parsing, and backward compatibility with existing configurations.
    """

    # Application Settings
    app_name: str = Field(default="Agentifui Pro API", env="APP_NAME")
    app_version: str = Field(default="0.1.0", env="APP_VERSION")
    app_description: str = Field(default="Backend API for Agentifui Pro", env="APP_DESCRIPTION")
    debug: bool = Field(default=None, env="DEBUG")  # Will be set based on environment

    # Server Configuration
    host: str = Field(default="0.0.0.0", env="HOST")
    port: int = Field(default=8000, env="PORT", gt=0, le=65535)

    # Environment Configuration
    environment: str = Field(default="development", env="ENVIRONMENT")

    # Security Settings
    secret_key: SecretStr = Field(env="SECRET_KEY")
    algorithm: str = Field(default="HS256", env="ALGORITHM")
    access_token_expire_minutes: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES", gt=0)

    # Database Configuration - Individual Fields (preferred)
    db_host: Optional[str] = Field(default=None, env="DB_HOST")
    db_port: Optional[int] = Field(default=None, env="DB_PORT", gt=0, le=65535)
    db_username: Optional[str] = Field(default=None, env="DB_USERNAME")
    db_password: Optional[str] = Field(default=None, env="DB_PASSWORD")
    db_database: Optional[str] = Field(default=None, env="DB_DATABASE")
    db_driver: Optional[str] = Field(default=None, env="DB_DRIVER")
    db_timeout_seconds: Optional[int] = Field(default=None, env="DB_TIMEOUT_SECONDS", gt=0, le=300)
    db_min_pool_size: Optional[int] = Field(default=None, env="DB_MIN_POOL_SIZE", gt=0, le=50)
    db_max_pool_size: Optional[int] = Field(default=None, env="DB_MAX_POOL_SIZE", gt=0, le=100)

    # Database Configuration - Legacy URL (backward compatibility)
    database_url: Optional[str] = Field(default=None, env="DATABASE_URL")

    # Legacy database pool settings for backward compatibility
    database_pool_size: int = Field(default=10, env="DATABASE_POOL_SIZE", gt=0, le=100)
    database_pool_max_overflow: int = Field(default=20, env="DATABASE_POOL_MAX_OVERFLOW", ge=0, le=100)
    database_pool_timeout: int = Field(default=30, env="DATABASE_POOL_TIMEOUT", gt=0, le=300)
    database_pool_recycle: int = Field(default=3600, env="DATABASE_POOL_RECYCLE", gt=0)

    # Health Check Configuration
    health_check_timeout: int = Field(default=5, env="HEALTH_CHECK_TIMEOUT", gt=0, le=30)
    database_health_check_timeout: int = Field(default=10, env="DATABASE_HEALTH_CHECK_TIMEOUT", gt=0, le=60)

    # Logging Configuration
    log_level: Optional[str] = Field(default=None, env="LOG_LEVEL")  # Will be set based on environment
    log_format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        env="LOG_FORMAT",
    )

    # CORS Settings with enhanced parsing
    cors_origins: list[str] = Field(default_factory=lambda: ["http://localhost:3000"], env="CORS_ORIGINS")
    cors_allow_credentials: bool = Field(default=True, env="CORS_ALLOW_CREDENTIALS")
    cors_allow_methods: list[str] = Field(default=["*"], env="CORS_ALLOW_METHODS")
    cors_allow_headers: list[str] = Field(default=["*"], env="CORS_ALLOW_HEADERS")

    # Feature Flags
    enable_docs: bool = Field(default=True, env="ENABLE_DOCS")
    enable_redoc: bool = Field(default=True, env="ENABLE_REDOC")
    use_uuidv7: bool = Field(default=False, env="USE_UUIDV7")

    # Enhanced Feature Flags
    feature_auth_v2: bool = Field(default=False, env="FEATURE_AUTH_V2")
    feature_enhanced_logging: bool = Field(default=False, env="FEATURE_ENHANCED_LOGGING")
    feature_rate_limiting: bool = Field(default=False, env="FEATURE_RATE_LIMITING")

    @field_validator("environment")
    @classmethod
    def validate_environment(cls, v: str) -> str:
        """Validate that environment is one of the allowed values."""
        allowed_envs = ["development", "staging", "production"]
        if v.lower() not in allowed_envs:
            raise ValueError(f"Environment must be one of: {allowed_envs}")
        return v.lower()

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v: Optional[str], info) -> str:
        """Set log level based on environment if not explicitly provided."""
        if v is not None:
            allowed_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
            if v.upper() not in allowed_levels:
                raise ValueError(f"Log level must be one of: {allowed_levels}")
            return v.upper()

        # Set default based on environment
        environment = info.data.get("environment", "development")
        if environment in {"production", "staging"}:
            return "INFO"
        else:  # development
            return "DEBUG"

    @field_validator("debug")
    @classmethod
    def validate_debug(cls, v: Optional[bool], info) -> bool:
        """Set debug mode based on environment if not explicitly provided."""
        if v is not None:
            return v

        # Set default based on environment
        environment = info.data.get("environment", "development")
        if environment in {"production", "staging"}:
            return False
        else:  # development
            return True

    @field_validator("secret_key")
    @classmethod
    def validate_secret_key(cls, v: SecretStr, info) -> SecretStr:
        """Enhanced secret key validation with environment-specific rules."""
        environment = info.data.get("environment", "development")
        secret_value = v.get_secret_value() if hasattr(v, "get_secret_value") else str(v)

        # Default insecure keys that should never be used
        insecure_defaults = [
            "your-secret-key-here-change-in-production",
            "dev-secure-string-for-development-only-change-in-production-32",
            "secret",
            "password",
            "changeme",
            "dev-secret",
            "test-secret",
        ]

        # Production requires strong security
        if environment == "production":
            if secret_value in insecure_defaults:
                raise ValueError(
                    "Production environment requires a secure secret key. Default or common keys are not allowed."
                )
            if len(secret_value) < 32:
                raise ValueError("Production secret key must be at least 32 characters long")

        # Staging requires moderate security
        elif environment == "staging":
            if secret_value in insecure_defaults:
                raise ValueError(
                    "Staging environment should use a secure secret key. Default or common keys are not recommended."
                )
            if len(secret_value) < 16:
                raise ValueError("Staging secret key should be at least 16 characters long")

        # Development allows lenient rules but warns about insecure keys
        elif environment == "development" and secret_value in insecure_defaults:
            warnings.warn(
                f"Using default secret key in {environment} environment. "
                "This is acceptable for development but MUST be changed for production.",
                UserWarning,
                stacklevel=2,
            )

        return v

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, v: Union[str, list[str]]) -> list[str]:
        """Enhanced CORS origins parsing with comma-separated preference."""
        if isinstance(v, str):
            # Try JSON array format first (backward compatibility)
            try:
                parsed = json.loads(v)
                if isinstance(parsed, list):
                    return [origin.strip() for origin in parsed if origin.strip()]
            except json.JSONDecodeError:
                pass

            # Handle comma-separated format (preferred)
            origins = [origin.strip() for origin in v.split(",") if origin.strip()]
            return origins if origins else ["http://localhost:3000"]

        return v if isinstance(v, list) else ["http://localhost:3000"]

    @field_validator("cors_origins")
    @classmethod
    def validate_cors_origins(cls, v: list[str], info) -> list[str]:
        """Validate CORS origins based on environment."""
        environment = info.data.get("environment", "development")

        if environment == "production":
            # Production should only allow HTTPS origins (except for localhost in dev)
            for origin in v:
                if not origin.startswith(("https://", "http://localhost", "http://127.0.0.1")):
                    if origin.startswith("http://"):
                        raise ValueError(
                            f"Production environment should use HTTPS origins. Found HTTP origin: {origin}"
                        )

        return v

    @field_validator("cors_allow_methods", "cors_allow_headers", mode="before")
    @classmethod
    def parse_cors_lists(cls, v: Union[str, list[str]]) -> list[str]:
        """Parse CORS methods and headers from string or list."""
        if isinstance(v, str):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return [item.strip() for item in v.split(",") if item.strip()]
        return v

    @computed_field
    @property
    def database(self) -> DatabaseConfig:
        """Get database configuration from individual fields or DATABASE_URL."""
        # Priority: Individual fields override DATABASE_URL
        if self._has_individual_database_fields():
            return self._create_database_config_from_fields()
        elif self.database_url:
            return DatabaseConfig.from_database_url(self.database_url)
        else:
            # Use defaults for development
            return self._create_default_database_config()

    @computed_field
    @property
    def configuration_source(self) -> str:
        """Determine the source of database configuration."""
        has_individual = self._has_individual_database_fields()
        has_url = bool(self.database_url)

        if has_individual and has_url:
            return "mixed"
        elif has_individual:
            return "individual_fields"
        elif has_url:
            return "database_url"
        else:
            return "defaults"

    def _has_individual_database_fields(self) -> bool:
        """Check if any individual database fields are provided."""
        return any(
            [
                self.db_host is not None,
                self.db_port is not None,
                self.db_username is not None,
                self.db_password is not None,
                self.db_database is not None,
            ]
        )

    def _create_database_config_from_fields(self) -> DatabaseConfig:
        """Create DatabaseConfig from individual fields with DATABASE_URL fallback."""
        # Start with DATABASE_URL if available for missing fields
        base_config = {}
        if self.database_url:
            try:
                base_db_config = DatabaseConfig.from_database_url(self.database_url)
                base_config = {
                    "host": base_db_config.host,
                    "port": base_db_config.port,
                    "username": base_db_config.username,
                    "password": base_db_config.password,
                    "database": base_db_config.database,
                    "driver": base_db_config.driver,
                }
            except Exception:
                # If DATABASE_URL is invalid, use defaults
                pass

        # Override with individual fields (they take precedence)
        config_params = {
            "host": self.db_host or base_config.get("host", "localhost"),
            "port": self.db_port or base_config.get("port", 5432),
            "username": self.db_username or base_config.get("username", "postgres"),
            "password": self.db_password or base_config.get("password", "postgres"),
            "database": self.db_database or base_config.get("database", "postgres"),
            "driver": self.db_driver or base_config.get("driver", "postgresql+asyncpg"),
            "timeout_seconds": self.db_timeout_seconds or 30,
            "min_pool_size": self.db_min_pool_size or 2,
            "max_pool_size": self.db_max_pool_size or 10,
        }

        return DatabaseConfig(**config_params)

    def _create_default_database_config(self) -> DatabaseConfig:
        """Create default database configuration for development."""
        return DatabaseConfig(
            host="localhost",
            port=5432,
            username="postgres",
            password="postgres",
            database="postgres",
            driver="postgresql+asyncpg",
            timeout_seconds=30,
            min_pool_size=2,
            max_pool_size=10,
        )

    def model_dump_secure(self) -> dict:
        """Return settings excluding sensitive information."""
        data = self.model_dump()

        # Remove or mask sensitive fields
        sensitive_fields = ["secret_key", "db_password", "database_url"]
        for field in sensitive_fields:
            if field in data:
                if field == "secret_key":
                    data[field] = "***MASKED***"
                else:
                    data.pop(field, None)

        return data

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        frozen=True,
        extra="ignore",
        # Validate assignment for computed fields
        validate_assignment=True,
    )


# Backward compatibility: alias for existing code
Settings = EnvironmentSettings


@lru_cache
def get_settings() -> EnvironmentSettings:
    """
    Get enhanced environment settings instance.

    Uses LRU cache to ensure singleton pattern - settings are loaded once
    and reused throughout the application lifecycle.

    Returns:
        EnvironmentSettings: Enhanced environment settings instance
    """
    return EnvironmentSettings()


# Export settings instance for convenience
settings = get_settings()
