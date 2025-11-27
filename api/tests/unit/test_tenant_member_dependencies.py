"""
Unit tests for tenant membership and role dependencies.
"""

import uuid

import pytest
from fastapi import HTTPException
from src.api.deps import require_tenant_member, require_tenant_role
from src.core.context import RequestContext, reset_request_context, set_request_context
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


def _build_member(user_id: str, tenant_id: str, role: TenantMemberRole, status: TenantMemberStatus) -> TenantMember:
    return TenantMember(
        user_id=user_id,
        tenant_id=tenant_id,
        role=role,
        status=status,
    )


@pytest.mark.asyncio
async def test_require_tenant_member_requires_actor() -> None:
    dependency = require_tenant_member()
    tenant = _build_tenant()
    token = set_request_context(RequestContext(tenant_id=tenant.id))

    try:
        with pytest.raises(HTTPException) as exc:
            await dependency(session=_StubSession(None), tenant=tenant)
        assert exc.value.status_code == 401
    finally:
        reset_request_context(token)


@pytest.mark.asyncio
async def test_require_tenant_member_rejects_missing_membership() -> None:
    dependency = require_tenant_member()
    tenant = _build_tenant()
    actor_id = str(uuid.uuid4())
    token = set_request_context(RequestContext(tenant_id=tenant.id, user_id=actor_id))

    try:
        with pytest.raises(HTTPException) as exc:
            await dependency(session=_StubSession(None), tenant=tenant)
        assert exc.value.status_code == 403
    finally:
        reset_request_context(token)


@pytest.mark.asyncio
async def test_require_tenant_member_rejects_inactive_status() -> None:
    dependency = require_tenant_member()
    tenant = _build_tenant()
    actor_id = str(uuid.uuid4())
    member = _build_member(actor_id, tenant.id, TenantMemberRole.MEMBER, TenantMemberStatus.SUSPENDED)
    token = set_request_context(RequestContext(tenant_id=tenant.id, user_id=actor_id))

    try:
        with pytest.raises(HTTPException) as exc:
            await dependency(session=_StubSession(member), tenant=tenant)
        assert exc.value.status_code == 403
    finally:
        reset_request_context(token)


@pytest.mark.asyncio
async def test_require_tenant_role_checks_role_membership() -> None:
    dependency = require_tenant_role(TenantMemberRole.ADMIN, TenantMemberRole.OWNER)
    tenant = _build_tenant()
    actor_id = str(uuid.uuid4())
    member = _build_member(actor_id, tenant.id, TenantMemberRole.MEMBER, TenantMemberStatus.ACTIVE)
    token = set_request_context(RequestContext(tenant_id=tenant.id, user_id=actor_id))

    try:
        with pytest.raises(HTTPException) as exc:
            await dependency(session=_StubSession(member), tenant=tenant)
        assert exc.value.status_code == 403
    finally:
        reset_request_context(token)


@pytest.mark.asyncio
async def test_require_tenant_role_allows_authorized_member() -> None:
    dependency = require_tenant_role(TenantMemberRole.ADMIN, TenantMemberRole.OWNER)
    tenant = _build_tenant()
    actor_id = str(uuid.uuid4())
    member = _build_member(actor_id, tenant.id, TenantMemberRole.ADMIN, TenantMemberStatus.ACTIVE)
    token = set_request_context(RequestContext(tenant_id=tenant.id, user_id=actor_id))

    try:
        resolved = await dependency(session=_StubSession(member), tenant=tenant)
        assert resolved is member
    finally:
        reset_request_context(token)
