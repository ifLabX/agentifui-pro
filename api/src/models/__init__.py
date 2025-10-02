"""
Models package initialization.

Import all SQLAlchemy models here to register them with Base.metadata
for Alembic autogenerate support.
"""

from src.models.base import Base
from src.models.errors import (
    ErrorResponse,
    ErrorType,
    ServiceUnavailableError,
    ValidationError,
    ValidationErrorResponse,
)

# Import new database models here:
# from src.models.user import User

__all__ = [
    "Base",
    "ErrorResponse",
    "ErrorType",
    "ServiceUnavailableError",
    "ValidationError",
    "ValidationErrorResponse",
    # Add new models to exports:
    # "User",
]
