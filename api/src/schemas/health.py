"""
Health status Pydantic models.

This module defines the data models for health check responses
following the OpenAPI specification in contracts/health.yaml.
"""

from datetime import UTC, datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class HealthStatus(str, Enum):
    """Health status enumeration."""

    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"


class MigrationStatus(str, Enum):
    """Migration status enumeration."""

    UP_TO_DATE = "up_to_date"
    PENDING = "pending"
    UNKNOWN = "unknown"


class ConnectionPoolInfo(BaseModel):
    """Connection pool information model."""

    active_connections: int = Field(..., ge=0, description="Number of active connections in the pool")
    pool_size: int = Field(..., ge=1, description="Maximum size of the connection pool")

    model_config = ConfigDict(frozen=True)


class HealthResponse(BaseModel):
    """
    Application health response model.

    Represents the overall health status of the FastAPI application.
    """

    status: HealthStatus = Field(..., description="Overall application health status")
    timestamp: str = Field(..., description="ISO 8601 timestamp of the health check")
    version: str = Field(..., description="Application version")
    uptime_seconds: Optional[int] = Field(None, ge=0, description="Application uptime in seconds")
    errors: Optional[list[str]] = Field(None, description="List of error messages if status is not healthy")

    model_config = ConfigDict(frozen=True)


class DatabaseHealthResponse(BaseModel):
    """
    Database health response model.

    Represents the health status of the PostgreSQL database connection.
    """

    status: HealthStatus = Field(..., description="Database health status")
    timestamp: str = Field(..., description="ISO 8601 timestamp of the health check")
    database_connected: bool = Field(..., description="Whether database connection is active")
    connection_pool: Optional[ConnectionPoolInfo] = Field(None, description="Connection pool metrics")
    response_time_ms: Optional[int] = Field(None, ge=0, description="Database response time in milliseconds")
    migration_status: Optional[MigrationStatus] = Field(None, description="Alembic migration status")
    errors: Optional[list[str]] = Field(None, description="List of error messages if status is not healthy")

    model_config = ConfigDict(frozen=True)


# Utility functions for creating health responses


def create_healthy_response(version: str, uptime_seconds: Optional[int] = None) -> HealthResponse:
    """
    Create a healthy application response.

    Args:
        version: Application version
        uptime_seconds: Application uptime in seconds

    Returns:
        HealthResponse: Healthy application response
    """
    return HealthResponse(
        status=HealthStatus.HEALTHY,
        timestamp=datetime.now(UTC).isoformat().replace("+00:00", "Z"),
        version=version,
        uptime_seconds=uptime_seconds,
        errors=None,
    )


def create_unhealthy_response(version: str, errors: list[str], uptime_seconds: Optional[int] = None) -> HealthResponse:
    """
    Create an unhealthy application response.

    Args:
        version: Application version
        errors: List of error messages
        uptime_seconds: Application uptime in seconds

    Returns:
        HealthResponse: Unhealthy application response
    """
    return HealthResponse(
        status=HealthStatus.UNHEALTHY,
        timestamp=datetime.now(UTC).isoformat().replace("+00:00", "Z"),
        version=version,
        uptime_seconds=uptime_seconds,
        errors=errors,
    )


def create_healthy_database_response(
    connection_pool: Optional[ConnectionPoolInfo] = None,
    response_time_ms: Optional[int] = None,
    migration_status: Optional[MigrationStatus] = None,
) -> DatabaseHealthResponse:
    """
    Create a healthy database response.

    Args:
        connection_pool: Connection pool information
        response_time_ms: Database response time in milliseconds
        migration_status: Migration status

    Returns:
        DatabaseHealthResponse: Healthy database response
    """
    return DatabaseHealthResponse(
        status=HealthStatus.HEALTHY,
        timestamp=datetime.now(UTC).isoformat().replace("+00:00", "Z"),
        database_connected=True,
        connection_pool=connection_pool,
        response_time_ms=response_time_ms,
        migration_status=migration_status,
        errors=None,
    )


def create_unhealthy_database_response(
    errors: list[str],
    response_time_ms: Optional[int] = None,
) -> DatabaseHealthResponse:
    """
    Create an unhealthy database response.

    Args:
        errors: List of error messages
        response_time_ms: Database response time in milliseconds (if available)

    Returns:
        DatabaseHealthResponse: Unhealthy database response
    """
    return DatabaseHealthResponse(
        status=HealthStatus.UNHEALTHY,
        timestamp=datetime.now(UTC).isoformat().replace("+00:00", "Z"),
        database_connected=False,
        connection_pool=None,
        response_time_ms=response_time_ms,
        migration_status=None,
        errors=errors,
    )
