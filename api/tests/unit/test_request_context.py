"""
Unit tests for request context helpers.
"""

from src.core.context import (
    RequestContext,
    get_request_context,
    include_soft_deleted,
    reset_request_context,
    system_context,
    tenant_context,
)


def test_tenant_context_sets_expected_fields() -> None:
    """Ensure tenant_context helper applies fields to the context var."""
    reset_request_context()
    assert get_request_context() == RequestContext()

    with tenant_context("tenant-123", user_id="user-456"):
        ctx = get_request_context()
        assert ctx.tenant_id == "tenant-123"
        assert ctx.user_id == "user-456"
        assert not ctx.include_deleted
        assert not ctx.allow_global_access

    assert get_request_context() == RequestContext()


def test_include_soft_deleted_toggles_flag() -> None:
    """include_soft_deleted should temporarily allow querying deleted rows."""
    reset_request_context()

    with tenant_context("tenant-1"):
        assert not get_request_context().include_deleted
        with include_soft_deleted():
            assert get_request_context().include_deleted
        assert not get_request_context().include_deleted


def test_system_context_enables_global_access() -> None:
    """system_context should bypass tenant filtering while restoring afterwards."""
    reset_request_context()

    with system_context(user_id="system"):
        ctx = get_request_context()
        assert ctx.allow_global_access
        assert ctx.user_id == "system"
        assert ctx.tenant_id is None

    assert get_request_context() == RequestContext()
