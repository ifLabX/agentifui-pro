"""
Database configuration model with field validation.

This module provides the DatabaseConfig model with comprehensive field validation,
URL composition capabilities, and backward compatibility with DATABASE_URL format.
"""

import urllib.parse

from pydantic import BaseModel, Field, computed_field, field_validator


class DatabaseConfig(BaseModel):
    """
    Database configuration model with field validation and URL composition.

    Supports both individual field configuration and DATABASE_URL parsing
    for maximum flexibility and backward compatibility.
    """

    host: str = Field(
        default="localhost",
        description="Database host address",
        min_length=1,
        max_length=255
    )

    port: int = Field(
        default=5432,
        description="Database port number",
        ge=1,
        le=65535
    )

    username: str = Field(
        description="Database username",
        min_length=1,
        max_length=63
    )

    password: str = Field(
        description="Database password",
        min_length=1,
        max_length=255
    )

    database: str = Field(
        description="Database name",
        min_length=1,
        max_length=63
    )

    driver: str = Field(
        default="postgresql+asyncpg",
        description="Database driver",
        pattern=r"^postgresql(\+asyncpg|\+psycopg|\+psycopg2)?$"
    )

    timeout_seconds: int = Field(
        default=30,
        description="Connection timeout in seconds",
        ge=1,
        le=300
    )

    min_pool_size: int = Field(
        default=2,
        description="Minimum connection pool size",
        ge=1,
        le=50
    )

    max_pool_size: int = Field(
        default=10,
        description="Maximum connection pool size",
        ge=1,
        le=100
    )

    @field_validator("host")
    @classmethod
    def validate_host(cls, v: str) -> str:
        """Validate database host address."""
        if not v or v.isspace():
            raise ValueError("Host cannot be empty or whitespace")
        return v.strip()

    @field_validator("username", "password", "database")
    @classmethod
    def validate_required_strings(cls, v: str) -> str:
        """Validate required string fields."""
        if not v or v.isspace():
            raise ValueError("Field cannot be empty or whitespace")
        return v.strip()

    @field_validator("max_pool_size")
    @classmethod
    def validate_pool_size_relationship(cls, v: int, info) -> int:
        """Validate that max_pool_size >= min_pool_size."""
        if hasattr(info.data, 'min_pool_size') and v < info.data['min_pool_size']:
            raise ValueError("max_pool_size must be greater than or equal to min_pool_size")
        return v

    @computed_field
    @property
    def database_url(self) -> str:
        """Generate database URL from individual fields."""
        # URL-encode the password to handle special characters
        encoded_password = urllib.parse.quote(self.password, safe="")

        return (
            f"{self.driver}://{self.username}:{encoded_password}"
            f"@{self.host}:{self.port}/{self.database}"
        )

    @classmethod
    def from_database_url(cls, database_url: str) -> "DatabaseConfig":
        """
        Create DatabaseConfig from DATABASE_URL string.

        Provides backward compatibility with existing DATABASE_URL configurations.
        """
        try:
            parsed = urllib.parse.urlparse(database_url)
        except Exception as e:
            raise ValueError(f"Invalid DATABASE_URL format: {e}")

        if not parsed.scheme:
            raise ValueError("DATABASE_URL must include a scheme (driver)")
        if not parsed.hostname:
            raise ValueError("DATABASE_URL must include a hostname")
        if not parsed.username:
            raise ValueError("DATABASE_URL must include a username")
        if not parsed.password:
            raise ValueError("DATABASE_URL must include a password")
        if not parsed.path or parsed.path == "/":
            raise ValueError("DATABASE_URL must include a database name")

        # Extract database name (remove leading slash)
        database = parsed.path.lstrip("/")

        # Handle default port
        port = parsed.port or 5432

        # URL-decode the password
        password = urllib.parse.unquote(parsed.password)

        return cls(
            host=parsed.hostname,
            port=port,
            username=parsed.username,
            password=password,
            database=database,
            driver=parsed.scheme
        )

    def model_dump(self, **kwargs) -> dict:
        """Override model_dump to mask sensitive information."""
        data = super().model_dump(**kwargs)

        # Mask password for security
        if "password" in data:
            data["password"] = "***MASKED***"

        return data

    def model_dump_secure(self) -> dict:
        """Return model data excluding sensitive fields."""
        data = self.model_dump()

        # Remove sensitive fields entirely
        sensitive_fields = ["password", "username"]
        for field in sensitive_fields:
            data.pop(field, None)

        return data

    def get_connection_params(self) -> dict:
        """Get connection parameters for database drivers."""
        return {
            "host": self.host,
            "port": self.port,
            "username": self.username,
            "password": self.password,
            "database": self.database,
            "connect_timeout": self.timeout_seconds,
            "pool_min_size": self.min_pool_size,
            "pool_max_size": self.max_pool_size
        }