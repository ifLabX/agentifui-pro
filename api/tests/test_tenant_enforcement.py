"""
Tests for tenant enforcement logic in SQLAlchemy event hooks.
"""

from types import SimpleNamespace

import pytest
from sqlalchemy import func, select
from src.core.context import RequestContext, reset_request_context, set_request_context, system_context
from src.core.db import _inject_default_orm_filters, _statement_targets_tenant_entities
from src.core.exceptions import TenantContextError
from src.models.tenant import TenantMember


def test_statement_targets_tenant_entities_with_aggregate() -> None:
    """Aggregate queries should still be recognised as tenant scoped."""
    stmt = select(func.count()).select_from(TenantMember)
    assert _statement_targets_tenant_entities(stmt)


def test_tenant_context_required_for_aggregate_select() -> None:
    """Ensure tenant context is required when executing aggregate queries."""
    reset_request_context()
    stmt = select(func.count()).select_from(TenantMember)
    orm_state = SimpleNamespace(is_select=True, statement=stmt)

    with pytest.raises(TenantContextError):
        _inject_default_orm_filters(orm_state)


def test_tenant_context_allows_aggregate_select() -> None:
    """When tenant context is present the filter should apply without errors."""
    stmt = select(func.count()).select_from(TenantMember)

    token = set_request_context(RequestContext(tenant_id="tenant-123"))
    try:
        orm_state = SimpleNamespace(is_select=True, statement=stmt)
        _inject_default_orm_filters(orm_state)
    finally:
        reset_request_context(token)


def test_system_context_bypasses_tenant_requirement() -> None:
    """Global/system context should allow aggregate access without tenant id."""
    stmt = select(func.count()).select_from(TenantMember)

    with system_context():
        orm_state = SimpleNamespace(is_select=True, statement=stmt)
        _inject_default_orm_filters(orm_state)
