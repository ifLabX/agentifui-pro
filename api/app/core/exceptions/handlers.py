"""
Global exception handlers for the FastAPI application.
Provides consistent error responses and logging.
"""

import logging
from typing import Union

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError as PydanticValidationError
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger(__name__)


class APIError(Exception):
    """Base exception for API errors."""

    def __init__(
        self,
        status_code: int,
        detail: str,
        error_code: str | None = None,
    ) -> None:
        self.status_code = status_code
        self.detail = detail
        self.error_code = error_code or "GENERIC_ERROR"


class DatabaseError(APIError):
    """Exception for database-related errors."""

    def __init__(self, detail: str = "Database operation failed") -> None:
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail, error_code="DATABASE_ERROR")


class ValidationError(APIError):
    """Exception for validation errors."""

    def __init__(self, detail: str = "Validation failed") -> None:
        super().__init__(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail, error_code="VALIDATION_ERROR")


async def api_exception_handler(request: Request, exc: APIError) -> JSONResponse:
    """
    Handle custom API exceptions.

    Args:
        request: The incoming request
        exc: The API exception

    Returns:
        JSON response with error details
    """
    logger.error(
        "API Exception: %s - %s (Status: %s, Path: %s)", exc.error_code, exc.detail, exc.status_code, request.url.path
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={"error": {"code": exc.error_code, "message": exc.detail, "type": "api_error"}},
    )


async def validation_exception_handler(
    request: Request, exc: Union[RequestValidationError, PydanticValidationError]
) -> JSONResponse:
    """
    Handle Pydantic validation exceptions.

    Args:
        request: The incoming request
        exc: The validation exception

    Returns:
        JSON response with validation error details
    """
    logger.warning("Validation Error: %s (Path: %s)", str(exc), request.url.path)

    # Extract error details from Pydantic errors
    errors = []
    if hasattr(exc, "errors"):
        for error in exc.errors():
            errors.append(
                {
                    "field": " -> ".join(str(loc) for loc in error.get("loc", [])),
                    "message": error.get("msg", ""),
                    "type": error.get("type", ""),
                }
            )

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Request validation failed",
                "type": "validation_error",
                "details": errors,
            }
        },
    )


async def database_exception_handler(request: Request, exc: SQLAlchemyError) -> JSONResponse:
    """
    Handle SQLAlchemy database exceptions.

    Args:
        request: The incoming request
        exc: The database exception

    Returns:
        JSON response with database error details
    """
    logger.error("Database Error: %s (Path: %s)", str(exc), request.url.path, exc_info=True)

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": {"code": "DATABASE_ERROR", "message": "Database operation failed", "type": "database_error"}},
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Handle unexpected exceptions.

    Args:
        request: The incoming request
        exc: The unexpected exception

    Returns:
        JSON response with generic error message
    """
    logger.error("Unexpected Error: %s (Path: %s)", str(exc), request.url.path, exc_info=True)

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {"code": "INTERNAL_ERROR", "message": "An unexpected error occurred", "type": "internal_error"}
        },
    )


def add_exception_handlers(app: FastAPI) -> None:
    """
    Add all exception handlers to the FastAPI application.

    Args:
        app: The FastAPI application instance
    """
    # Custom API exceptions
    app.add_exception_handler(APIError, api_exception_handler)

    # Validation exceptions
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(PydanticValidationError, validation_exception_handler)

    # Database exceptions
    app.add_exception_handler(SQLAlchemyError, database_exception_handler)

    # Generic exception handler (catch-all)
    app.add_exception_handler(Exception, generic_exception_handler)

    logger.info("Exception handlers registered successfully")
