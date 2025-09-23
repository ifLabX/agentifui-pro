"""
Application configuration management with Pydantic Settings.

This module provides type-safe configuration management using environment variables
with validation and default values.
"""
from functools import lru_cache

from pydantic import ConfigDict, Field, field_validator
from pydantic.types import SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    All settings are validated using Pydantic and provide type safety.
    """

    # Application Settings
    app_name: str = Field(default="Agentifui Pro API", env="APP_NAME")
    app_version: str = Field(default="0.1.0", env="APP_VERSION")
    app_description: str = Field(
        default="Backend API for Agentifui Pro", env="APP_DESCRIPTION"
    )
    debug: bool = Field(default=False, env="DEBUG")

    # Server Configuration
    host: str = Field(default="0.0.0.0", env="HOST")
    port: int = Field(default=8000, env="PORT", gt=0, le=65535)

    # Database Configuration
    database_url: str = Field(..., env="DATABASE_URL")
    database_pool_size: int = Field(default=10, env="DATABASE_POOL_SIZE", gt=0, le=100)
    database_pool_max_overflow: int = Field(
        default=20, env="DATABASE_POOL_MAX_OVERFLOW", ge=0, le=100
    )
    database_pool_timeout: int = Field(
        default=30, env="DATABASE_POOL_TIMEOUT", gt=0, le=300
    )
    database_pool_recycle: int = Field(
        default=3600, env="DATABASE_POOL_RECYCLE", gt=0
    )

    # Health Check Configuration
    health_check_timeout: int = Field(
        default=5, env="HEALTH_CHECK_TIMEOUT", gt=0, le=30
    )
    database_health_check_timeout: int = Field(
        default=10, env="DATABASE_HEALTH_CHECK_TIMEOUT", gt=0, le=60
    )

    # Logging Configuration
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        env="LOG_FORMAT",
    )

    # Security Settings (for future use)
    secret_key: SecretStr = Field(
        default="your-secret-key-here-change-in-production", env="SECRET_KEY"
    )
    algorithm: str = Field(default="HS256", env="ALGORITHM")
    access_token_expire_minutes: int = Field(
        default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES", gt=0
    )

    # CORS Settings
    cors_origins: list[str] = Field(
        default=["http://localhost:3000"], env="CORS_ORIGINS"
    )
    cors_allow_credentials: bool = Field(default=True, env="CORS_ALLOW_CREDENTIALS")
    cors_allow_methods: list[str] = Field(default=["*"], env="CORS_ALLOW_METHODS")
    cors_allow_headers: list[str] = Field(default=["*"], env="CORS_ALLOW_HEADERS")

    # Environment
    environment: str = Field(default="development", env="ENVIRONMENT")

    # Feature Flags
    enable_docs: bool = Field(default=True, env="ENABLE_DOCS")
    enable_redoc: bool = Field(default=True, env="ENABLE_REDOC")
    use_uuidv7: bool = Field(default=False, env="USE_UUIDV7")

    @field_validator("database_url")
    @classmethod
    def validate_database_url(cls, v):
        """Validate that database URL is a PostgreSQL connection string."""
        if not v.startswith(("postgresql://", "postgresql+asyncpg://")):
            raise ValueError("Database URL must be a PostgreSQL connection string")
        return v

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v):
        """Validate that log level is one of the allowed values."""
        allowed_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in allowed_levels:
            raise ValueError(f"Log level must be one of: {allowed_levels}")
        return v.upper()

    @field_validator("environment")
    @classmethod
    def validate_environment(cls, v):
        """Validate that environment is one of the allowed values."""
        allowed_envs = ["development", "staging", "production"]
        if v.lower() not in allowed_envs:
            raise ValueError(f"Environment must be one of: {allowed_envs}")
        return v.lower()

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, v):
        """Parse CORS origins from string or list."""
        if isinstance(v, str):
            # Handle JSON string format
            import json
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                # Handle comma-separated string
                return [origin.strip() for origin in v.split(",")]
        return v

    @field_validator("cors_allow_methods", mode="before")
    @classmethod
    def parse_cors_methods(cls, v):
        """Parse CORS methods from string or list."""
        if isinstance(v, str):
            import json
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return [method.strip() for method in v.split(",")]
        return v

    @field_validator("cors_allow_headers", mode="before")
    @classmethod
    def parse_cors_headers(cls, v):
        """Parse CORS headers from string or list."""
        if isinstance(v, str):
            import json
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return [header.strip() for header in v.split(",")]
        return v

    @field_validator("secret_key")
    @classmethod
    def validate_secret_key(cls, v, info):
        """Validate secret key security in production environment."""
        # Get environment from context
        environment = info.data.get("environment", "development")

        # Default insecure keys that should never be used in production
        insecure_defaults = [
            "your-secret-key-here-change-in-production",
            "dev-secure-string-for-development-only-change-in-production-32",
            "secret",
            "password",
            "changeme",
        ]

        secret_value = v.get_secret_value() if hasattr(v, 'get_secret_value') else str(v)

        # In production, enforce strong secret key requirements
        if environment == "production":
            if secret_value in insecure_defaults:
                raise ValueError(
                    "Production environment requires a secure secret key. "
                    "Default or common keys are not allowed."
                )

            if len(secret_value) < 32:
                raise ValueError(
                    "Production secret key must be at least 32 characters long"
                )

        # In development, warn about insecure keys but allow them
        elif environment == "development" and secret_value in insecure_defaults:
            import warnings
            warnings.warn(
                f"Using default secret key in {environment} environment. "
                "This is acceptable for development but MUST be changed for production.",
                UserWarning, stacklevel=2
            )

        return v

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        # Make settings immutable
        frozen=True,
        extra="ignore"  # Ignore extra fields for now
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


# Export settings instance for convenience
settings = get_settings()