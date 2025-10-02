"""
Base database model with UUID primary key support.

This module provides the base model class for all database entities
with PostgreSQL UUIDv7 support and common fields.
"""

import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, MetaData, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from config.settings import get_settings


def generate_uuid() -> str:
    """
    Generate UUID for primary keys.

    Uses UUID4 as fallback until PostgreSQL 18 UUIDv7 is available.
    This function will be updated to use UUIDv7 when supported.

    Returns:
        str: UUID string for database storage
    """
    settings = get_settings()

    if settings.use_uuidv7:
        # Placeholder for PostgreSQL 18 UUIDv7 support
        # When PostgreSQL 18 is available, this will use:
        # SELECT gen_uuid_v7() from the database
        # For now, fall back to UUID4
        pass

    return str(uuid.uuid4())


# Database naming convention for consistent constraint names
convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

metadata = MetaData(naming_convention=convention)


class Base(DeclarativeBase):
    """
    Base model class for all database entities.

    Provides common fields and UUID primary key support with
    preparation for PostgreSQL 18 UUIDv7 integration.
    """

    metadata = metadata

    # Common fields for all models
    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        primary_key=True,
        default=generate_uuid,
        comment="Primary key using UUID",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        comment="Record creation timestamp",
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        comment="Record last update timestamp",
    )

    def __repr__(self) -> str:
        """String representation of the model."""
        return f"<{self.__class__.__name__}(id={self.id})>"

    def to_dict(self) -> dict[str, Any]:
        """
        Convert model instance to dictionary.

        Returns:
            dict: Model data as dictionary
        """
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


# Export the base class for model inheritance
__all__ = ["Base", "generate_uuid"]
