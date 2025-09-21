"""
Base model patterns for SQLAlchemy 2.0.
Provides common fields and patterns for all database models.
"""

from datetime import datetime
from typing import Any, ClassVar
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


def generate_uuid() -> str:
    """Generate a UUID string for primary keys."""
    return str(uuid4())


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""

    # SQLAlchemy 2.0 style type annotation configuration
    type_annotation_map: ClassVar[dict[type, Any]] = {
        str: UUID(as_uuid=False),  # Use string UUIDs for better JSON serialization
    }


class TimestampMixin:
    """Mixin for created_at and updated_at timestamps."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False, doc="Timestamp when the record was created"
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
        doc="Timestamp when the record was last updated",
    )


class SoftDeleteMixin:
    """Mixin for soft delete functionality."""

    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False, doc="Whether the record is active (false = soft deleted)"
    )


class BaseModel(Base, TimestampMixin, SoftDeleteMixin):
    """
    Base model with UUID primary key, timestamps, and soft delete.

    All application models should inherit from this class to ensure
    consistent behavior and common fields.
    """

    __abstract__ = True

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=generate_uuid, doc="UUID primary key"
    )

    @declared_attr
    @classmethod
    def __tablename__(cls) -> str:
        """Generate table name from class name."""
        # Convert CamelCase to snake_case
        import re

        name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", cls.__name__)
        return re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()

    def __repr__(self) -> str:
        """String representation of the model."""
        return f"<{self.__class__.__name__}(id='{self.id}')>"

    def to_dict(self) -> dict[str, Any]:
        """Convert model instance to dictionary."""
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


class AuditMixin:
    """
    Mixin for audit trail functionality.

    This can be used for models that need to track who made changes
    and what type of action was performed.
    """

    action_type: Mapped[str] = mapped_column(
        nullable=False, doc="Type of action performed (CREATE, UPDATE, DELETE, etc.)"
    )

    actor_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), nullable=True, doc="ID of the user/system that performed the action"
    )

    metadata_json: Mapped[str] = mapped_column(nullable=True, doc="Additional context as JSON string")


class AuditLogModel(Base, TimestampMixin, AuditMixin):
    """
    Base model for audit log entries.

    Used to track critical operations and changes in the system.
    """

    __abstract__ = True

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=generate_uuid, doc="UUID primary key for audit entry"
    )

    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False, doc="When the audited action occurred"
    )
