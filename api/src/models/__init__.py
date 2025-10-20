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
from src.models.tenant import (
    Tenant,
    TenantMember,
    TenantMemberRole,
    TenantMemberStatus,
    TenantStatus,
)

__all__ = [
    "Base",
    "ErrorResponse",
    "ErrorType",
    "ServiceUnavailableError",
    "Tenant",
    "TenantMember",
    "TenantMemberRole",
    "TenantMemberStatus",
    "TenantStatus",
    "ValidationError",
    "ValidationErrorResponse",
]
