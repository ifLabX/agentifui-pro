"""
SQLAlchemy declarative base and common mixins for tenant-aware models.

Provides shared columns such as UUIDv7 primary keys, optimistic locking,
auditing metadata, tenant scoping, and soft-deletion helpers.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from sqlalchemy import DateTime, Integer, MetaData, func, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column

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

    Provides UUID primary key support using PostgreSQL 18 native uuidv7()
    function alongside timestamp metadata fields.
    """

    metadata = metadata

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        primary_key=True,
        server_default=text("uuidv7()"),
        comment="Primary key generated via PostgreSQL uuidv7()",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        comment="Record creation timestamp",
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
        comment="Record update timestamp",
    )

    def __repr__(self) -> str:
        """Human-readable representation for debugging."""
        return f"<{self.__class__.__name__}(id={self.id})>"

    def to_dict(self) -> dict[str, Any]:
        """Convert model instance to a dictionary representation."""
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


class VersionedAuditMixin:
    """Track creator/updater metadata and support optimistic concurrency control."""

    __abstract__ = True

    created_by: Mapped[str | None] = mapped_column(
        UUID(as_uuid=False),
        nullable=True,
        comment="Identifier of the principal that created the record",
    )
    updated_by: Mapped[str | None] = mapped_column(
        UUID(as_uuid=False),
        nullable=True,
        comment="Identifier of the principal that last updated the record",
    )
    version: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        server_default=text("1"),
        comment="Optimistic concurrency control counter",
    )

    @declared_attr.directive
    def __mapper_args__(cls) -> dict[str, Any]:  # type: ignore[override]  # noqa: N805
        """Enable SQLAlchemy's optimistic locking using the version column."""
        return {"version_id_col": cls.version}  # pragma: no cover - handled by SQLAlchemy


class TenantAwareMixin:
    """Mixin that enforces tenant isolation using a tenant_id column."""

    __abstract__ = True

    @declared_attr
    def tenant_id(cls) -> Mapped[str]:  # noqa: N805
        return mapped_column(
            UUID(as_uuid=False),
            nullable=False,
            comment="Owning tenant identifier",
        )


class SoftDeleteMixin:
    """Enable soft deletion semantics using timestamp markers."""

    __abstract__ = True

    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        comment="Timestamp when the record was soft deleted",
    )
    deleted_by: Mapped[str | None] = mapped_column(
        UUID(as_uuid=False),
        nullable=True,
        comment="Identifier of the principal that soft deleted the record",
    )

    def soft_delete(self, deleted_by: str | None = None) -> None:
        """Mark the record as deleted without removing it from the database."""
        now = datetime.now(UTC)
        self.deleted_at = now
        self.deleted_by = deleted_by

    def restore(self) -> None:
        """Restore a previously soft-deleted record."""
        self.deleted_at = None
        self.deleted_by = None

    @property
    def is_deleted(self) -> bool:
        """Check whether the record has been soft deleted."""
        return self.deleted_at is not None


__all__ = [
    "Base",
    "SoftDeleteMixin",
    "TenantAwareMixin",
    "VersionedAuditMixin",
]
