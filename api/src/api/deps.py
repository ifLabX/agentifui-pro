"""
Shared API dependencies for FastAPI routes.
"""

from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.context import get_request_context, require_tenant_id
from src.core.db import get_db_session
from src.core.exceptions import TenantContextError
from src.models.tenant import Tenant


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


__all__ = ["get_current_tenant", "get_db_session", "get_optional_tenant_id"]
