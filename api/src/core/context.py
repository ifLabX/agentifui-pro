"""
Request-scoped context helpers for multi-tenant operations.

This module exposes utilities to manage tenant and actor identifiers using
ContextVar instances so database policies can enforce isolation automatically.
"""

from __future__ import annotations

from collections.abc import Generator, Iterator
from contextlib import contextmanager
from contextvars import ContextVar, Token
from dataclasses import dataclass, replace


@dataclass(frozen=True, slots=True)
class RequestContext:
    """Immutable snapshot of tenant-aware request metadata."""

    tenant_id: str | None = None
    user_id: str | None = None
    include_deleted: bool = False
    allow_global_access: bool = False

    def derive(
        self,
        *,
        tenant_id: str | None = None,
        user_id: str | None = None,
        include_deleted: bool | None = None,
        allow_global_access: bool | None = None,
    ) -> RequestContext:
        """Create a modified copy without mutating this instance."""
        return replace(
            self,
            tenant_id=self.tenant_id if tenant_id is None else tenant_id,
            user_id=self.user_id if user_id is None else user_id,
            include_deleted=self.include_deleted if include_deleted is None else include_deleted,
            allow_global_access=(
                self.allow_global_access if allow_global_access is None else allow_global_access
            ),
        )


_context_var: ContextVar[RequestContext | None] = ContextVar("request_context", default=None)
_EMPTY_CONTEXT = RequestContext()


def get_request_context() -> RequestContext:
    """Return the current request context."""
    context = _context_var.get()
    if context is None:
        return _EMPTY_CONTEXT
    return context


def set_request_context(context: RequestContext) -> Token[RequestContext | None]:
    """
    Set the current request context.

    Returns:
        Context token that can be used to restore the previous context.
    """
    return _context_var.set(context)


def reset_request_context(token: Token[RequestContext | None] | None = None) -> None:
    """
    Restore the previous request context.

    Args:
        token: Optional token returned from `set_request_context`. When omitted,
               the context resets to the default empty state.
    """
    if token is None:
        _context_var.set(None)
    else:
        _context_var.reset(token)


def require_tenant_id() -> str:
    """Fetch tenant identifier from context or raise a descriptive error."""
    tenant_id = get_request_context().tenant_id
    if tenant_id is None:
        from src.core.exceptions import TenantContextError

        raise TenantContextError("Tenant context is required but was not provided")
    return tenant_id


@contextmanager
def tenant_context(
    tenant_id: str,
    *,
    user_id: str | None = None,
    include_deleted: bool = False,
    allow_global_access: bool = False,
) -> Generator[RequestContext, None, None]:
    """
    Set the tenant context for the duration of a synchronous or async operation.

    Intended for background tasks, tests, or scripts that do not run through
    FastAPI's dependency injection stack.
    """
    token = set_request_context(
        RequestContext(
            tenant_id=tenant_id,
            user_id=user_id,
            include_deleted=include_deleted,
            allow_global_access=allow_global_access,
        )
    )
    try:
        yield get_request_context()
    finally:
        reset_request_context(token)


@contextmanager
def include_soft_deleted() -> Iterator[RequestContext]:
    """Temporarily include soft-deleted rows in ORM queries."""
    current = get_request_context()
    token = set_request_context(current.derive(include_deleted=True))
    try:
        yield get_request_context()
    finally:
        reset_request_context(token)


@contextmanager
def system_context(
    *,
    user_id: str | None = None,
    include_deleted: bool = False,
) -> Iterator[RequestContext]:
    """
    Run with elevated privileges, bypassing tenant filtering.

    Useful for administrative tasks that need to operate across tenants.
    """
    token = set_request_context(
        RequestContext(
            tenant_id=None,
            user_id=user_id,
            include_deleted=include_deleted,
            allow_global_access=True,
        )
    )
    try:
        yield get_request_context()
    finally:
        reset_request_context(token)


__all__ = [
    "RequestContext",
    "get_request_context",
    "include_soft_deleted",
    "require_tenant_id",
    "reset_request_context",
    "set_request_context",
    "system_context",
    "tenant_context",
]
