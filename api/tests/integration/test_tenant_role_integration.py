"""
Integration-style tests to verify middleware + role dependencies work together.
"""

import uuid
from typing import Annotated, Any

from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient
from src.api.deps import get_current_tenant, get_db_session, require_tenant_role
from src.middleware.error_handler import setup_error_handling
from src.middleware.tenant_context import TenantContextMiddleware
from src.models.tenant import Tenant, TenantMember, TenantMemberRole, TenantMemberStatus


class _StubResult:
    def __init__(self, member: TenantMember | None) -> None:
        self._member = member

    def scalar_one_or_none(self) -> TenantMember | None:
        return self._member


class _StubSession:
    def __init__(self, member: TenantMember | None) -> None:
        self._member = member

    async def execute(self, _statement: Any) -> _StubResult:
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


def _create_app(member: TenantMember | None) -> TestClient:
    tenant = _build_tenant()

    async def override_current_tenant() -> Tenant:
        return tenant

    async def override_session() -> _StubSession:
        return _StubSession(member)

    app = FastAPI()
    app.add_middleware(TenantContextMiddleware)
    setup_error_handling(app)

    owner_dependency = require_tenant_role(TenantMemberRole.OWNER)

    @app.get("/protected")
    async def protected(
        _member: Annotated[TenantMember, Depends(owner_dependency)],
    ) -> dict[str, str]:
        return {"status": "ok"}

    app.dependency_overrides[get_current_tenant] = override_current_tenant
    app.dependency_overrides[get_db_session] = override_session

    return TestClient(app)


def test_missing_actor_header_returns_unauthorized() -> None:
    client = _create_app(member=None)
    headers = {"x-tenant-id": str(uuid.uuid4())}

    response = client.get("/protected", headers=headers)

    assert response.status_code == 401
    assert response.json()["detail"] == "Actor context is required"


def test_non_member_returns_forbidden() -> None:
    client = _create_app(member=None)
    headers = {
        "x-tenant-id": str(uuid.uuid4()),
        "x-actor-id": str(uuid.uuid4()),
    }

    response = client.get("/protected", headers=headers)

    assert response.status_code == 403
    assert response.json()["detail"] == "User is not a member of this tenant"


def test_insufficient_role_returns_forbidden() -> None:
    actor_id = str(uuid.uuid4())
    tenant_id = str(uuid.uuid4())
    member = _build_member(actor_id, tenant_id, role=TenantMemberRole.MEMBER)
    client = _create_app(member=member)
    headers = {
        "x-tenant-id": tenant_id,
        "x-actor-id": actor_id,
    }

    response = client.get("/protected", headers=headers)

    assert response.status_code == 403
    assert response.json()["detail"] == "Insufficient tenant role"


def test_authorized_member_succeeds() -> None:
    actor_id = str(uuid.uuid4())
    tenant_id = str(uuid.uuid4())
    member = _build_member(actor_id, tenant_id, role=TenantMemberRole.OWNER)
    client = _create_app(member=member)
    headers = {
        "x-tenant-id": tenant_id,
        "x-actor-id": actor_id,
    }

    response = client.get("/protected", headers=headers)

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
