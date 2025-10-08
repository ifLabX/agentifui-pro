"""
Global error handling middleware for FastAPI.

This module provides structured error handling middleware that catches
exceptions and returns standardized error responses.
"""

import logging
import traceback
from typing import Union

from fastapi import HTTPException, Request, Response
from fastapi.responses import JSONResponse
from pydantic import ValidationError as PydanticValidationError
from sqlalchemy.exc import DisconnectionError, SQLAlchemyError
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from core.config import get_settings
from models.errors import (
    ErrorType,
    create_database_error,
    create_error_response,
    create_internal_server_error,
    create_validation_error,
)

logger = logging.getLogger(__name__)


class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    """
    Global error handling middleware.

    Catches and transforms exceptions into standardized error responses
    following the error schema defined in contracts/errors.yaml.
    """

    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self.settings = get_settings()

    async def dispatch(self, request: Request, call_next) -> Response:
        """
        Process request and handle any exceptions.

        Args:
            request: Incoming HTTP request
            call_next: Next middleware or endpoint in chain

        Returns:
            Response: HTTP response (success or error)
        """
        try:
            response = await call_next(request)
            return response

        except HTTPException as exc:
            # Handle FastAPI HTTP exceptions
            return await self._handle_http_exception(request, exc)

        except PydanticValidationError as exc:
            # Handle Pydantic validation errors
            return await self._handle_validation_error(request, exc)

        except (SQLAlchemyError, DisconnectionError) as exc:
            # Handle database-related errors
            return await self._handle_database_error(request, exc)

        except Exception as exc:
            # Handle all other unexpected exceptions
            return await self._handle_unexpected_error(request, exc)

    async def _handle_http_exception(self, request: Request, exc: HTTPException) -> JSONResponse:
        """
        Handle FastAPI HTTP exceptions.

        Args:
            request: HTTP request context
            exc: HTTP exception raised

        Returns:
            JSONResponse: Standardized error response
        """
        # Map HTTP status codes to error types
        error_type_mapping = {
            400: ErrorType.VALIDATION_ERROR,
            401: ErrorType.AUTHENTICATION_ERROR,
            403: ErrorType.AUTHORIZATION_ERROR,
            404: ErrorType.NOT_FOUND_ERROR,
            503: ErrorType.SERVICE_UNAVAILABLE,
        }

        error_type = error_type_mapping.get(exc.status_code, ErrorType.INTERNAL_SERVER_ERROR)

        error_response = create_error_response(
            error_type=error_type,
            message=str(exc.detail),
            request_id=self._get_request_id(request),
        )

        return JSONResponse(
            status_code=exc.status_code,
            content=error_response.model_dump(),
        )

    async def _handle_validation_error(self, request: Request, exc: PydanticValidationError) -> JSONResponse:
        """
        Handle Pydantic validation errors.

        Args:
            request: HTTP request context
            exc: Pydantic validation exception

        Returns:
            JSONResponse: Validation error response
        """
        # Transform Pydantic errors to our validation error format
        validation_errors = []
        for error in exc.errors():
            field_path = ".".join(str(loc) for loc in error["loc"])
            validation_errors.append(
                {
                    "field": field_path,
                    "message": error["msg"],
                    "value": error.get("input"),
                }
            )

        error_response = create_validation_error(
            validation_errors=validation_errors,
            message="Request validation failed",
        )

        return JSONResponse(
            status_code=422,
            content=error_response.model_dump(),
        )

    async def _handle_database_error(
        self, request: Request, exc: Union[SQLAlchemyError, DisconnectionError]
    ) -> JSONResponse:
        """
        Handle database-related errors.

        Args:
            request: HTTP request context
            exc: Database exception

        Returns:
            JSONResponse: Database error response
        """
        logger.error("Database error: %s", exc, exc_info=True)

        # Determine if it's a connection error or other database issue
        if isinstance(exc, DisconnectionError):
            error_response = create_database_error(
                message="Database connection lost",
                detail="The database connection was lost during the request" if self.settings.debug else None,
                request_id=self._get_request_id(request),
            )
        else:
            error_response = create_database_error(
                message="Database operation failed",
                detail=str(exc) if self.settings.debug else None,
                request_id=self._get_request_id(request),
            )

        return JSONResponse(
            status_code=503,
            content=error_response.model_dump(),
        )

    async def _handle_unexpected_error(self, request: Request, exc: Exception) -> JSONResponse:
        """
        Handle unexpected exceptions.

        Args:
            request: HTTP request context
            exc: Unexpected exception

        Returns:
            JSONResponse: Internal server error response
        """
        # Log the full exception for debugging
        logger.error(
            "Unexpected error processing %s %s: %s",
            request.method,
            request.url,
            exc,
            exc_info=True,
        )

        # Include traceback in debug mode only
        detail = None
        if self.settings.debug:
            detail = f"{str(exc)}\n\n{traceback.format_exc()}"

        error_response = create_internal_server_error(
            message="An unexpected error occurred",
            detail=detail,
            request_id=self._get_request_id(request),
        )

        return JSONResponse(
            status_code=500,
            content=error_response.model_dump(),
        )

    def _get_request_id(self, request: Request) -> str:
        """
        Extract or generate request ID for error tracking.

        Args:
            request: HTTP request context

        Returns:
            str: Request identifier
        """
        # Try to get request ID from headers (e.g., X-Request-ID)
        request_id = request.headers.get("x-request-id")
        if request_id:
            return request_id

        # Try to get from request state (set by other middleware)
        request_id = getattr(request.state, "request_id", None)
        if request_id:
            return request_id

        # Generate a new request ID (will be handled by error response creation)
        return None


def setup_error_handling(app) -> None:
    """
    Set up global error handling for the FastAPI application.

    Args:
        app: FastAPI application instance
    """
    app.add_middleware(ErrorHandlerMiddleware)

    # Configure logging for error handling
    logging.basicConfig(
        level=getattr(logging, get_settings().log_level),
        format=get_settings().log_format,
    )
