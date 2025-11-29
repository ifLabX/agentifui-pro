"""
Database models for multi-tenant management.
"""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import Any

from sqlalchemy import (
    Boolean,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    String,
    UniqueConstraint,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base import Base, SoftDeleteMixin, TenantAwareMixin, VersionedAuditMixin


class TenantStatus(StrEnum):
    """Lifecycle state for tenants."""

    ACTIVE = "active"
    SUSPENDED = "suspended"
    DELETED = "deleted"


class Tenant(Base, SoftDeleteMixin, VersionedAuditMixin):
    """Core tenant/workspace entity."""

    __tablename__ = "tenants"
    __table_args__ = (
        UniqueConstraint("slug", name="uq_tenants_slug"),
        Index("ix_tenants_status", "status"),
    )

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[TenantStatus] = mapped_column(
        Enum(TenantStatus, name="tenant_status"),
        nullable=False,
        default=TenantStatus.ACTIVE,
        server_default=TenantStatus.ACTIVE.value,
    )
    region: Mapped[str | None] = mapped_column(String(64), nullable=True)
    settings: Mapped[dict[str, Any]] = mapped_column(
        JSONB,
        nullable=False,
        server_default=text("'{}'::jsonb"),
    )
    is_personal: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default=text("false"),
    )

    members: Mapped[list[TenantMember]] = relationship(
        back_populates="tenant",
        cascade="all,delete-orphan",
    )


class TenantMemberRole(StrEnum):
    """Role assigned to a tenant member."""

    OWNER = "owner"
    ADMIN = "admin"
    MEMBER = "member"
    VIEWER = "viewer"


class TenantMemberStatus(StrEnum):
    """Membership state for tenant members."""

    INVITED = "invited"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    REMOVED = "removed"


class TenantMember(Base, TenantAwareMixin, SoftDeleteMixin, VersionedAuditMixin):
    """Association between external users and tenants."""

    __tablename__ = "tenant_members"
    __table_args__ = (
        UniqueConstraint("tenant_id", "user_id", name="uq_tenant_members_user"),
        Index("ix_tenant_members_tenant_id", "tenant_id"),
    )

    user_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        nullable=False,
        comment="Identifier of the linked user account",
    )
    role: Mapped[TenantMemberRole] = mapped_column(
        Enum(TenantMemberRole, name="tenant_member_role"),
        nullable=False,
        default=TenantMemberRole.MEMBER,
        server_default=TenantMemberRole.MEMBER.value,
    )
    status: Mapped[TenantMemberStatus] = mapped_column(
        Enum(TenantMemberStatus, name="tenant_member_status"),
        nullable=False,
        default=TenantMemberStatus.ACTIVE,
        server_default=TenantMemberStatus.ACTIVE.value,
    )
    invited_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        server_default=func.now(),
    )
    joined_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    tenant_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("tenants.id", ondelete="CASCADE"),
        nullable=False,
        comment="Owning tenant identifier",
    )

    tenant: Mapped[Tenant] = relationship(back_populates="members")


__all__ = [
    "Tenant",
    "TenantMember",
    "TenantMemberRole",
    "TenantMemberStatus",
    "TenantStatus",
]
