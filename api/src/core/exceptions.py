"""
Custom exception hierarchy for multi-tenant infrastructure.
"""


class TenantContextError(RuntimeError):
    """Raised when a tenant-aware operation lacks the required context."""


class TenantAccessError(TenantContextError):
    """Raised when accessing resources outside the permitted tenant scope."""


__all__ = ["TenantAccessError", "TenantContextError"]
