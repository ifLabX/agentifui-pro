"""
Models package initialization.

This module imports all model classes to ensure they are registered
with SQLAlchemy metadata for proper migration generation.
"""
from models.base import Base
from models.errors import (
    ErrorResponse,
    ErrorType,
    ServiceUnavailableError,
    ValidationError,
    ValidationErrorResponse,
)

__all__ = [
    "Base",
    "ErrorResponse",
    "ErrorType",
    "ServiceUnavailableError",
    "ValidationError",
    "ValidationErrorResponse",
]