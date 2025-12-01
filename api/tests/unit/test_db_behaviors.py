import uuid

import pytest
from sqlalchemy import select
from src.core import db
from src.core.context import RequestContext, reset_request_context, set_request_context
from src.core.exceptions import TenantContextError
from src.models.tenant import Tenant, TenantMember, TenantMemberRole, TenantMemberStatus


class _StubSession:
    def __init__(self, *, new=None, deleted=None, dirty=None, is_modified=True) -> None:
        self.new = new or []
        self.deleted = deleted or []
        self.dirty = dirty or []
        self.added: list[object] = []
        self.exited = False
        self._is_modified = is_modified
        self.rollback_called = False

    async def rollback(self) -> None:
        self.rollback_called = True

    def add(self, instance: object) -> None:
        self.added.append(instance)

    def is_modified(self, _instance: object, *, include_collections: bool = False) -> bool:
        return self._is_modified


class _SessionContext:
    def __init__(self) -> None:
        self.session = _StubSession()
        self.exited = False

    def __call__(self) -> "_SessionContext":
        return self

    async def __aenter__(self) -> _StubSession:
        return self.session

    async def __aexit__(self, exc_type, exc, tb) -> None:
        self.exited = True


class _OrmExecuteState:
    def __init__(self, statement) -> None:
        self.is_select = True
        self.statement = statement


@pytest.mark.asyncio
async def test_dispose_engine_disposes_when_initialized(monkeypatch: pytest.MonkeyPatch) -> None:
    class _Engine:
        def __init__(self) -> None:
            self.disposed = False

        async def dispose(self) -> None:
            self.disposed = True

    engine = _Engine()
    monkeypatch.setattr(db, "_engine", engine)

    await db.dispose_engine()

    assert engine.disposed is True
    assert db._engine is None  # type: ignore[attr-defined]


@pytest.mark.asyncio
async def test_get_database_info_handles_exceptions(monkeypatch: pytest.MonkeyPatch) -> None:
    def _raise_engine() -> None:
        raise RuntimeError("boom")

    monkeypatch.setattr(db, "get_async_engine", _raise_engine)

    info = await db.get_database_info()

    assert info["connected"] is False
    assert "boom" in info["error"]


@pytest.mark.asyncio
async def test_get_db_session_rolls_back_on_error(monkeypatch: pytest.MonkeyPatch) -> None:
    session_context = _SessionContext()
    monkeypatch.setattr(db, "get_session_factory", lambda: session_context)

    generator = db.get_db_session()
    session = await anext(generator)

    with pytest.raises(RuntimeError):
        await generator.athrow(RuntimeError("failure"))

    assert session.rollback_called is True
    assert session_context.exited is True


def test_inject_default_filters_require_tenant_for_scoped_queries(monkeypatch: pytest.MonkeyPatch) -> None:
    state = _OrmExecuteState(select(TenantMember))
    token = set_request_context(RequestContext())

    try:
        with pytest.raises(TenantContextError):
            db._inject_default_orm_filters(state)  # type: ignore[attr-defined]
    finally:
        reset_request_context(token)


def test_apply_audit_metadata_sets_defaults() -> None:
    tenant_id = str(uuid.uuid4())
    user_id = str(uuid.uuid4())

    soft_deleted = Tenant(name="Soft", slug="soft")
    new_member = TenantMember(
        user_id=str(uuid.uuid4()),
        tenant_id=tenant_id,
        role=TenantMemberRole.MEMBER,
        status=TenantMemberStatus.ACTIVE,
    )
    new_member.tenant_id = None
    dirty_member = TenantMember(
        user_id=str(uuid.uuid4()),
        tenant_id=tenant_id,
        role=TenantMemberRole.MEMBER,
        status=TenantMemberStatus.ACTIVE,
    )

    session = _StubSession(new=[new_member], deleted=[soft_deleted], dirty=[dirty_member])
    token = set_request_context(RequestContext(tenant_id=tenant_id, user_id=user_id))

    try:
        db._apply_audit_and_soft_delete_metadata(session, None, None)  # type: ignore[attr-defined]
    finally:
        reset_request_context(token)

    assert soft_deleted.deleted_by == user_id
    assert soft_deleted.deleted_at is not None
    assert new_member.tenant_id == tenant_id
    assert new_member.created_by == user_id
    assert new_member.updated_by == user_id
    assert dirty_member.updated_by == user_id


def test_apply_audit_metadata_rejects_mismatched_tenant() -> None:
    tenant_id = str(uuid.uuid4())
    member = TenantMember(
        user_id=str(uuid.uuid4()),
        tenant_id="other",
        role=TenantMemberRole.MEMBER,
        status=TenantMemberStatus.ACTIVE,
    )
    session = _StubSession(new=[member], deleted=[], dirty=[])
    token = set_request_context(RequestContext(tenant_id=tenant_id, user_id=str(uuid.uuid4())))

    try:
        with pytest.raises(TenantContextError):
            db._apply_audit_and_soft_delete_metadata(session, None, None)  # type: ignore[attr-defined]
    finally:
        reset_request_context(token)
