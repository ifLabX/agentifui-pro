"""add multi-tenant foundation

Revision ID: 3c2b8f88b1a5
Revises: 9814f556d003
Create Date: 2025-03-14 10:00:00.000000

"""
from collections.abc import Sequence
from typing import Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "3c2b8f88b1a5"
down_revision: Union[str, None] = "9814f556d003"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

tenant_status_enum = postgresql.ENUM(
    "active",
    "suspended",
    "deleted",
    name="tenant_status",
    create_type=False,
)
tenant_member_role_enum = postgresql.ENUM(
    "owner",
    "admin",
    "member",
    "viewer",
    name="tenant_member_role",
    create_type=False,  # Prevent automatic creation of the enum type
)
)
tenant_member_status_enum = postgresql.ENUM(
    "invited",
    "active",
    "suspended",
    "removed",
    name="tenant_member_status",
    create_type=False,
)


def upgrade() -> None:
    """Upgrade database schema."""
    bind = op.get_bind()
    tenant_status_enum.create(bind, checkfirst=True)
    tenant_member_role_enum.create(bind, checkfirst=True)
    tenant_member_status_enum.create(bind, checkfirst=True)

    op.create_table(
        "tenants",
        sa.Column("id", postgresql.UUID(as_uuid=False), server_default=sa.text("uuidv7()"), primary_key=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("created_by", postgresql.UUID(as_uuid=False), nullable=True),
        sa.Column("updated_by", postgresql.UUID(as_uuid=False), nullable=True),
        sa.Column("version", sa.Integer(), nullable=False, server_default=sa.text("1")),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("deleted_by", postgresql.UUID(as_uuid=False), nullable=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("slug", sa.String(length=255), nullable=False),
        sa.Column("status", tenant_status_enum, nullable=False, server_default="active"),
        sa.Column("region", sa.String(length=64), nullable=True),
        sa.Column("settings", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("is_personal", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.UniqueConstraint("slug", name="uq_tenants_slug"),
    )
    op.create_index("ix_tenants_status", "tenants", ["status"])

    op.create_table(
        "tenant_members",
        sa.Column("id", postgresql.UUID(as_uuid=False), server_default=sa.text("uuidv7()"), primary_key=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("created_by", postgresql.UUID(as_uuid=False), nullable=True),
        sa.Column("updated_by", postgresql.UUID(as_uuid=False), nullable=True),
        sa.Column("version", sa.Integer(), nullable=False, server_default=sa.text("1")),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("deleted_by", postgresql.UUID(as_uuid=False), nullable=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column("role", tenant_member_role_enum, nullable=False, server_default="member"),
        sa.Column("status", tenant_member_status_enum, nullable=False, server_default="active"),
        sa.Column("invited_at", sa.DateTime(timezone=True), nullable=True, server_default=sa.func.now()),
        sa.Column("joined_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=False), nullable=False),
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.id"], ondelete="CASCADE"),
        sa.UniqueConstraint("tenant_id", "user_id", name="uq_tenant_members_user"),
    )
    op.create_index("ix_tenant_members_tenant_id", "tenant_members", ["tenant_id"])


def downgrade() -> None:
    """Downgrade database schema."""
    op.drop_index("ix_tenant_members_tenant_id", table_name="tenant_members")
    op.drop_table("tenant_members")

    op.drop_index("ix_tenants_status", table_name="tenants")
    op.drop_table("tenants")

    bind = op.get_bind()
    tenant_member_status_enum.drop(bind, checkfirst=True)
    tenant_member_role_enum.drop(bind, checkfirst=True)
    tenant_status_enum.drop(bind, checkfirst=True)
