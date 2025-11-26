"""
Middleware to populate request-scoped tenant context.
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from uuid import UUID

from fastapi import HTTPException, Request, Response, status
from src.core.context import RequestContext, reset_request_context, set_request_context
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

DEFAULT_TENANT_HEADER = "x-tenant-id"
DEFAULT_ACTOR_HEADER = "x-actor-id"


class TenantContextMiddleware(BaseHTTPMiddleware):
    """
    Extract tenant and actor identifiers from incoming requests.
    """

    def __init__(
        self,
        app: ASGIApp,
        *,
        tenant_header: str = DEFAULT_TENANT_HEADER,
        actor_header: str = DEFAULT_ACTOR_HEADER,
    ) -> None:
        super().__init__(app)
        self.tenant_header = tenant_header
        self.actor_header = actor_header

    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        """
        Populate the request context and ensure cleanup after the response.
        """
        if request.query_params.get("tenant_id") is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"tenant_id must be provided via the {self.tenant_header} header",
            )

        tenant_id_header = request.headers.get(self.tenant_header)
        actor_id_header = request.headers.get(self.actor_header)

        tenant_id = self._validate_optional_uuid(tenant_id_header, field_name="tenant_id")
        actor_id = self._validate_optional_uuid(actor_id_header, field_name="actor_id")

        token = set_request_context(
            RequestContext(
                tenant_id=tenant_id,
                user_id=actor_id,
            )
        )

        request.state.tenant_id = tenant_id
        request.state.actor_id = actor_id

        try:
            response = await call_next(request)
        finally:
            reset_request_context(token)

        return response

    @staticmethod
    def _validate_optional_uuid(value: str | None, *, field_name: str) -> str | None:
        """
        Validate that the provided value is a UUID string when present.
        """
        if value is None:
            return None

        try:
            return str(UUID(value))
        except (TypeError, ValueError) as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"{field_name} must be a valid UUID",
            ) from exc


__all__ = ["TenantContextMiddleware"]
