import uuid

import pytest
from fastapi import APIRouter, FastAPI, HTTPException
from src.core.context import RequestContext, reset_request_context, set_request_context
from src.core.router import (
    admin_router,
    include_admin_router,
    include_tenant_router,
    public_router,
    tenant_router,
)
from src.models.tenant import Tenant, TenantMember, TenantMemberRole, TenantMemberStatus


class _StubResult:
    def __init__(self, member: TenantMember | None) -> None:
        self._member = member

    def scalar_one_or_none(self) -> TenantMember | None:
        return self._member


class _StubSession:
    def __init__(self, member: TenantMember | None) -> None:
        self._member = member

    async def execute(self, _statement: object) -> _StubResult:
        return _StubResult(self._member)


def _build_tenant() -> Tenant:
    tenant = Tenant(name="Test Tenant", slug="test-tenant")
    tenant.id = str(uuid.uuid4())
    return tenant


def _build_member(user_id: str, tenant_id: str, role: TenantMemberRole) -> TenantMember:
    return TenantMember(
        user_id=user_id,
        tenant_id=tenant_id,
        role=role,
        status=TenantMemberStatus.ACTIVE,
    )


def test_public_router_normalizes_tags() -> None:
    router = public_router("/health", tags=("one", "two"))
    assert router.prefix == "/health"
    assert router.tags == ["one", "two"]


@pytest.mark.asyncio
async def test_tenant_router_applies_membership_dependency() -> None:
    tenant = _build_tenant()
    actor_id = str(uuid.uuid4())
    member = _build_member(actor_id, tenant.id, TenantMemberRole.MEMBER)
    router = tenant_router("/items")
    dependency = router.dependencies[0].dependency
    token = set_request_context(RequestContext(tenant_id=tenant.id, user_id=actor_id))

    try:
        resolved = await dependency(session=_StubSession(member), tenant=tenant)
    finally:
        reset_request_context(token)

    assert resolved is member


@pytest.mark.asyncio
async def test_admin_router_enforces_admin_roles() -> None:
    tenant = _build_tenant()
    actor_id = str(uuid.uuid4())
    member = _build_member(actor_id, tenant.id, TenantMemberRole.MEMBER)
    router = admin_router("/admin")
    dependency = router.dependencies[0].dependency
    token = set_request_context(RequestContext(tenant_id=tenant.id, user_id=actor_id))

    try:
        with pytest.raises(HTTPException) as exc:
            await dependency(session=_StubSession(member), tenant=tenant)
    finally:
        reset_request_context(token)

    assert exc.value.status_code == 403


def test_include_tenant_router_attaches_dependency() -> None:
    app = FastAPI()
    router = APIRouter()

    @router.get("/ping")
    async def ping() -> dict[str, bool]:
        return {"ok": True}

    include_tenant_router(app, router)
    route = next(r for r in app.routes if getattr(r, "path", "") == "/ping")

    assert route.dependencies, "Tenant enforcement dependency should be attached"


def test_include_admin_router_attaches_dependency() -> None:
    app = FastAPI()
    router = APIRouter()

    @router.get("/secure")
    async def secure() -> dict[str, bool]:
        return {"ok": True}

    include_admin_router(app, router)
    route = next(r for r in app.routes if getattr(r, "path", "") == "/secure")

    assert route.dependencies, "Admin enforcement dependency should be attached"
