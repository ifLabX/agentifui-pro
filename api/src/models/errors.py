"""
Error response Pydantic models.

This module defines the error response models following the schema
defined in contracts/errors.yaml for consistent error handling.
"""

import uuid
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field


class ErrorType(StrEnum):
    """Error type enumeration."""

    INTERNAL_SERVER_ERROR = "INTERNAL_SERVER_ERROR"
    DATABASE_CONNECTION_ERROR = "DATABASE_CONNECTION_ERROR"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    SERVICE_UNAVAILABLE = "SERVICE_UNAVAILABLE"
    CONFIGURATION_ERROR = "CONFIGURATION_ERROR"
    AUTHENTICATION_ERROR = "AUTHENTICATION_ERROR"
    AUTHORIZATION_ERROR = "AUTHORIZATION_ERROR"
    NOT_FOUND_ERROR = "NOT_FOUND_ERROR"
    TIMEOUT_ERROR = "TIMEOUT_ERROR"


class ErrorResponse(BaseModel):
    """
    Generic error response model.

    Used for most error conditions with optional additional details.
    """

    error: str = Field(..., description="Error type or code")
    message: str = Field(..., description="Human-readable error message")
    detail: Optional[str] = Field(None, description="Additional error details for debugging")
    timestamp: str = Field(..., description="ISO 8601 timestamp when error occurred")
    request_id: Optional[str] = Field(None, description="Unique request identifier for error tracking")

    model_config = ConfigDict(frozen=True)


class ValidationError(BaseModel):
    """
    Individual field validation error.

    Used within ValidationErrorResponse for detailed field-level errors.
    """

    field: str = Field(..., description="Field name that failed validation")
    message: str = Field(..., description="Validation error message")
    value: Optional[Any] = Field(None, description="The invalid value that was provided")

    model_config = ConfigDict(frozen=True)


class ValidationErrorResponse(BaseModel):
    """
    Validation error response model.

    Used specifically for request validation failures with detailed
    field-level error information.
    """

    error: Literal["VALIDATION_ERROR"] = Field(
        default="VALIDATION_ERROR", description="Error type indicating validation failure"
    )
    message: str = Field(..., description="General validation error message")
    timestamp: str = Field(..., description="ISO 8601 timestamp when error occurred")
    validation_errors: list[ValidationError] = Field(..., description="Specific field validation errors")

    model_config = ConfigDict(frozen=True)


class ServiceUnavailableError(BaseModel):
    """
    Service unavailable error response model.

    Used when service is temporarily unavailable with optional retry information.
    """

    error: Literal["SERVICE_UNAVAILABLE"] = Field(
        default="SERVICE_UNAVAILABLE",
        description="Error indicating service is temporarily unavailable",
    )
    message: str = Field(..., description="Service unavailable message")
    timestamp: str = Field(..., description="ISO 8601 timestamp when error occurred")
    retry_after: Optional[int] = Field(None, ge=1, description="Suggested retry delay in seconds")

    model_config = ConfigDict(frozen=True)


# Utility functions for creating error responses


def create_error_response(
    error_type: str,
    message: str,
    detail: Optional[str] = None,
    request_id: Optional[str] = None,
) -> ErrorResponse:
    """
    Create a generic error response.

    Args:
        error_type: Error type or code
        message: Human-readable error message
        detail: Additional error details
        request_id: Request identifier for tracking

    Returns:
        ErrorResponse: Generic error response
    """
    if request_id is None:
        request_id = str(uuid.uuid4())

    return ErrorResponse(
        error=error_type,
        message=message,
        detail=detail,
        timestamp=datetime.now(UTC).isoformat().replace("+00:00", "Z"),
        request_id=request_id,
    )


def create_database_error(
    message: str = "Unable to connect to database",
    detail: Optional[str] = None,
    request_id: Optional[str] = None,
) -> ErrorResponse:
    """
    Create a database connection error response.

    Args:
        message: Error message
        detail: Additional error details
        request_id: Request identifier

    Returns:
        ErrorResponse: Database error response
    """
    return create_error_response(
        error_type=ErrorType.DATABASE_CONNECTION_ERROR,
        message=message,
        detail=detail,
        request_id=request_id,
    )


def create_validation_error(
    validation_errors: list[dict[str, Any]],
    message: str = "Request validation failed",
) -> ValidationErrorResponse:
    """
    Create a validation error response.

    Args:
        validation_errors: List of validation error dictionaries
        message: General validation error message

    Returns:
        ValidationErrorResponse: Validation error response
    """
    errors = [
        ValidationError(
            field=error["field"],
            message=error["message"],
            value=error.get("value"),
        )
        for error in validation_errors
    ]

    return ValidationErrorResponse(
        message=message,
        timestamp=datetime.now(UTC).isoformat().replace("+00:00", "Z"),
        validation_errors=errors,
    )


def create_service_unavailable_error(
    message: str = "Service temporarily unavailable",
    retry_after: Optional[int] = None,
) -> ServiceUnavailableError:
    """
    Create a service unavailable error response.

    Args:
        message: Service unavailable message
        retry_after: Suggested retry delay in seconds

    Returns:
        ServiceUnavailableError: Service unavailable error response
    """
    return ServiceUnavailableError(
        message=message,
        timestamp=datetime.now(UTC).isoformat().replace("+00:00", "Z"),
        retry_after=retry_after,
    )


def create_internal_server_error(
    message: str = "An unexpected error occurred",
    detail: Optional[str] = None,
    request_id: Optional[str] = None,
) -> ErrorResponse:
    """
    Create an internal server error response.

    Args:
        message: Error message
        detail: Additional error details
        request_id: Request identifier

    Returns:
        ErrorResponse: Internal server error response
    """
    return create_error_response(
        error_type=ErrorType.INTERNAL_SERVER_ERROR,
        message=message,
        detail=detail,
        request_id=request_id,
    )


def create_configuration_error(
    message: str = "Configuration error",
    detail: Optional[str] = None,
    request_id: Optional[str] = None,
) -> ErrorResponse:
    """
    Create a configuration error response.

    Args:
        message: Error message
        detail: Additional error details
        request_id: Request identifier

    Returns:
        ErrorResponse: Configuration error response
    """
    return create_error_response(
        error_type=ErrorType.CONFIGURATION_ERROR,
        message=message,
        detail=detail,
        request_id=request_id,
    )
