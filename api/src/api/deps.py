"""
Shared API dependencies for FastAPI routes.
"""

from collections.abc import Awaitable, Callable, Iterable
from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.context import get_request_context, require_tenant_id
from src.core.db import get_db_session
from src.core.exceptions import TenantContextError
from src.models.tenant import Tenant, TenantMember, TenantMemberRole, TenantMemberStatus


async def get_current_tenant(session: Annotated[AsyncSession, Depends(get_db_session)]) -> Tenant:
    """
    Resolve the current tenant from the request context.
    """
    try:
        tenant_id = require_tenant_id()
    except TenantContextError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    tenant = await session.get(Tenant, tenant_id)
    if tenant is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant not found",
        )

    return tenant


def get_optional_tenant_id() -> str | None:
    """Convenience dependency to access the tenant identifier when optional."""
    return get_request_context().tenant_id


def _require_actor_id() -> str:
    """
    Ensure a user/actor identifier exists in the request context.
    """
    actor_id = get_request_context().user_id
    if actor_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Actor context is required",
        )
    return actor_id


async def _get_tenant_member(session: AsyncSession, tenant_id: str, user_id: str) -> TenantMember | None:
    """
    Fetch a tenant member record for the given tenant/user combination.
    """
    stmt = select(TenantMember).where(
        TenantMember.tenant_id == tenant_id,
        TenantMember.user_id == user_id,
    )
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


def require_tenant_member(
    allowed_roles: Iterable[TenantMemberRole] | None = None,
    *,
    allow_invited: bool = False,
) -> Callable[..., Awaitable[TenantMember]]:
    """
    Dependency factory that ensures the current actor is an active tenant member.
    """
    role_set = set(allowed_roles) if allowed_roles is not None else None

    async def dependency(
        session: Annotated[AsyncSession, Depends(get_db_session)],
        tenant: Annotated[Tenant, Depends(get_current_tenant)],
    ) -> TenantMember:
        actor_id = _require_actor_id()
        member = await _get_tenant_member(session, tenant.id, actor_id)

        if member is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User is not a member of this tenant",
            )

        if member.status in {TenantMemberStatus.REMOVED, TenantMemberStatus.SUSPENDED}:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Tenant membership is not active",
            )

        if not allow_invited and member.status == TenantMemberStatus.INVITED:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Tenant membership is not active",
            )

        if role_set is not None and member.role not in role_set:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient tenant role",
            )

        return member

    return dependency


def require_tenant_role(
    *roles: TenantMemberRole,
    allow_invited: bool = False,
) -> Callable[..., Awaitable[TenantMember]]:
    """
    Convenience dependency to require a tenant member with one of the given roles.
    """
    if not roles:
        raise ValueError("At least one role is required")

    return require_tenant_member(roles, allow_invited=allow_invited)


__all__ = [
    "get_current_tenant",
    "get_db_session",
    "get_optional_tenant_id",
    "require_tenant_member",
    "require_tenant_role",
]
