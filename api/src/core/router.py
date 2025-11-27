"""
Router factories and registration helpers for tenant-aware APIs.
"""

from __future__ import annotations

from collections.abc import Sequence
from enum import Enum
from typing import Any

from fastapi import APIRouter, Depends, FastAPI
from fastapi.params import Depends as DependsParam
from src.api.deps import require_tenant_member, require_tenant_role
from src.models.tenant import TenantMemberRole

DependencyList = Sequence[DependsParam]
RouterTags = Sequence[str | Enum] | None


def _normalize_tags(tags: RouterTags) -> list[str | Enum] | None:
    """
    Convert tag sequences to mutable lists for FastAPI routers.
    """
    return list(tags) if tags is not None else None


def _merge_dependencies(defaults: list[DependsParam], existing: DependencyList | None) -> list[DependsParam]:
    """
    Combine base dependencies with any provided dependencies.
    """
    merged = list(defaults)
    if existing:
        merged.extend(existing)
    return merged


def public_router(
    prefix: str,
    *,
    tags: RouterTags = None,
    dependencies: DependencyList | None = None,
    **kwargs: Any,
) -> APIRouter:
    """
    Create a router for public endpoints without tenant enforcement.
    """
    router_tags = _normalize_tags(tags)
    return APIRouter(prefix=prefix, tags=router_tags, dependencies=dependencies, **kwargs)


def tenant_router(
    prefix: str,
    *,
    tags: RouterTags = None,
    dependencies: DependencyList | None = None,
    allowed_roles: Sequence[TenantMemberRole] | None = None,
    allow_invited: bool = False,
    **kwargs: Any,
) -> APIRouter:
    """
    Create a router that enforces tenant membership at the router level.
    """
    base_dependency = Depends(require_tenant_member(allowed_roles, allow_invited=allow_invited))
    merged_dependencies = _merge_dependencies([base_dependency], dependencies)
    router_tags = _normalize_tags(tags)
    return APIRouter(prefix=prefix, tags=router_tags, dependencies=merged_dependencies, **kwargs)


def admin_router(
    prefix: str,
    *,
    tags: RouterTags = None,
    dependencies: DependencyList | None = None,
    roles: Sequence[TenantMemberRole] | None = None,
    allow_invited: bool = False,
    **kwargs: Any,
) -> APIRouter:
    """
    Create a router that restricts access to specific tenant roles.
    """
    role_scope = tuple(roles) if roles else (TenantMemberRole.ADMIN, TenantMemberRole.OWNER)
    base_dependency = Depends(require_tenant_role(*role_scope, allow_invited=allow_invited))
    merged_dependencies = _merge_dependencies([base_dependency], dependencies)
    router_tags = _normalize_tags(tags)
    return APIRouter(prefix=prefix, tags=router_tags, dependencies=merged_dependencies, **kwargs)


def include_tenant_router(
    app: FastAPI,
    router: APIRouter,
    *,
    allowed_roles: Sequence[TenantMemberRole] | None = None,
    allow_invited: bool = False,
) -> None:
    """
    Register an existing router with tenant membership enforcement without mutating the router.
    """
    base_dependency = Depends(require_tenant_member(allowed_roles, allow_invited=allow_invited))
    merged_dependencies = _merge_dependencies([base_dependency], router.dependencies)
    app.include_router(router, dependencies=merged_dependencies)


def include_admin_router(
    app: FastAPI,
    router: APIRouter,
    *,
    roles: Sequence[TenantMemberRole] | None = None,
    allow_invited: bool = False,
) -> None:
    """
    Register an existing router with role-restricted tenant enforcement without mutating the router.
    """
    role_scope = tuple(roles) if roles else (TenantMemberRole.ADMIN, TenantMemberRole.OWNER)
    base_dependency = Depends(require_tenant_role(*role_scope, allow_invited=allow_invited))
    merged_dependencies = _merge_dependencies([base_dependency], router.dependencies)
    app.include_router(router, dependencies=merged_dependencies)


def include_public_router(app: FastAPI, router: APIRouter) -> None:
    """
    Register a public router without tenant enforcement.
    """
    app.include_router(router)


__all__ = [
    "admin_router",
    "include_admin_router",
    "include_public_router",
    "include_tenant_router",
    "public_router",
    "tenant_router",
]
