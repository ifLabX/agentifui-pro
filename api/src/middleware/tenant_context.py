"""
Middleware to populate request-scoped tenant context.
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable

from fastapi import Request, Response
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
        tenant_id = request.headers.get(self.tenant_header) or request.query_params.get("tenant_id")
        actor_id = request.headers.get(self.actor_header)

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


__all__ = ["TenantContextMiddleware"]
