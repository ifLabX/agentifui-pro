"""
Guardrail tests to keep tenant isolation and routing conventions enforced.
"""

import importlib
import pkgutil

from fastapi import APIRouter
from src.models.base import Base, TenantAwareMixin
from src.models.tenant import Tenant


def test_models_are_tenant_scoped_by_default() -> None:
    """
    Ensure new models inherit TenantAwareMixin unless explicitly whitelisted.
    """
    allowed_global_models = {Tenant}
    missing_mixin: list[str] = []

    for mapper in Base.registry.mappers:
        model_cls = mapper.class_
        if model_cls in allowed_global_models:
            continue
        if not issubclass(model_cls, TenantAwareMixin):
            missing_mixin.append(model_cls.__name__)

    assert not missing_mixin, (
        f"Models must inherit TenantAwareMixin or be whitelisted as global: {sorted(missing_mixin)}"
    )


def test_endpoint_routers_enforce_tenant_dependencies() -> None:
    """
    Ensure routers are created with tenant-aware dependencies by default.
    """
    import src.api.endpoints as endpoints_pkg

    public_prefixes = {"/health", "/branding"}
    violations: list[str] = []

    for module_info in pkgutil.iter_modules(endpoints_pkg.__path__):
        if module_info.name.startswith("_"):
            continue

        module = importlib.import_module(f"{endpoints_pkg.__name__}.{module_info.name}")
        router = getattr(module, "router", None)

        if not isinstance(router, APIRouter):
            continue

        if router.prefix in public_prefixes:
            continue

        if not router.dependencies:
            violations.append(module_info.name)

    assert not violations, (
        "Routers must enforce tenant membership/roles (use tenant_router/admin_router). "
        f"Offending modules: {', '.join(sorted(violations))}"
    )
