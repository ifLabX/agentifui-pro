"""
Pydantic schemas for health check endpoints.
Based on contracts/health.yaml specification.
"""

from datetime import UTC, datetime
from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field, field_serializer


class HealthStatus(str, Enum):
    """Health status enumeration."""

    HEALTHY = "healthy"


class ReadinessStatus(str, Enum):
    """Readiness status enumeration."""

    READY = "ready"
    NOT_READY = "not_ready"


class DatabaseStatus(str, Enum):
    """Database connection status enumeration."""

    CONNECTED = "connected"
    DISCONNECTED = "disconnected"


class HealthResponse(BaseModel):
    """
    Response schema for GET /health endpoint.

    Basic health check that always returns healthy if the application is running.
    """

    status: Literal[HealthStatus.HEALTHY] = Field(default=HealthStatus.HEALTHY, description="Application health status")
    timestamp: datetime = Field(description="Timestamp when the health check was performed")

    @field_serializer("timestamp")
    def serialize_timestamp(self, dt: datetime) -> str:
        """Serialize datetime to ISO format with Z suffix for UTC."""
        if dt.tzinfo is None:
            # If naive datetime, assume UTC
            dt = dt.replace(tzinfo=UTC)
        # Convert to UTC and format with Z suffix
        return dt.astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    model_config = {"json_schema_extra": {"example": {"status": "healthy", "timestamp": "2025-01-21T10:00:00.000000Z"}}}


class ReadinessResponse(BaseModel):
    """
    Response schema for GET /health/ready endpoint.

    Readiness check that includes database connectivity status.
    Returns 200 when ready, 503 when not ready.
    """

    status: ReadinessStatus = Field(description="Application readiness status")
    database: DatabaseStatus = Field(description="Database connection status")
    timestamp: datetime = Field(description="Timestamp when the readiness check was performed")

    @field_serializer("timestamp")
    def serialize_timestamp(self, dt: datetime) -> str:
        """Serialize datetime to ISO format with Z suffix for UTC."""
        if dt.tzinfo is None:
            # If naive datetime, assume UTC
            dt = dt.replace(tzinfo=UTC)
        # Convert to UTC and format with Z suffix
        return dt.astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    model_config = {
        "json_schema_extra": {
            "example": {"status": "ready", "database": "connected", "timestamp": "2025-01-21T10:00:00.000000Z"}
        }
    }

    @classmethod
    def create_ready_response(cls, database_connected: bool) -> "ReadinessResponse":
        """
        Create a readiness response based on database status.

        Args:
            database_connected: Whether the database is connected

        Returns:
            ReadinessResponse with appropriate status
        """
        if database_connected:
            return cls(status=ReadinessStatus.READY, database=DatabaseStatus.CONNECTED, timestamp=datetime.now(UTC))
        else:
            return cls(
                status=ReadinessStatus.NOT_READY, database=DatabaseStatus.DISCONNECTED, timestamp=datetime.now(UTC)
            )

    @classmethod
    def create_not_ready_response(cls, database_connected: bool = False) -> "ReadinessResponse":
        """
        Create a not ready response.

        Args:
            database_connected: Whether the database is connected (default: False)

        Returns:
            ReadinessResponse with not ready status
        """
        return cls(
            status=ReadinessStatus.NOT_READY,
            database=DatabaseStatus.CONNECTED if database_connected else DatabaseStatus.DISCONNECTED,
            timestamp=datetime.now(UTC),
        )
