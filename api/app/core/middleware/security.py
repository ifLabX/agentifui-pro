"""
Security middleware for FastAPI application.
Implements security headers and trusted host validation.
"""

import logging
from collections.abc import Callable

from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Middleware to add security headers to all responses.

    Implements OWASP recommended security headers.
    """

    def __init__(self, app, enable_security_headers: bool = True):
        super().__init__(app)
        self.enable_security_headers = enable_security_headers

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Add security headers to response."""
        response = await call_next(request)

        if self.enable_security_headers:
            # Prevent XSS attacks
            response.headers["X-Content-Type-Options"] = "nosniff"
            response.headers["X-Frame-Options"] = "DENY"
            response.headers["X-XSS-Protection"] = "1; mode=block"

            # Referrer policy
            response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

            # Content Security Policy (basic)
            response.headers["Content-Security-Policy"] = (
                "default-src 'self'; "
                "script-src 'self' 'unsafe-inline'; "
                "style-src 'self' 'unsafe-inline'; "
                "img-src 'self' data:; "
                "font-src 'self';"
            )

        return response


class TrustedHostMiddleware(BaseHTTPMiddleware):
    """
    Middleware to validate request hosts against a trusted list.

    Helps prevent Host header injection attacks.
    """

    def __init__(self, app, trusted_hosts: list[str] | None = None):
        super().__init__(app)
        self.trusted_hosts = trusted_hosts or ["localhost", "127.0.0.1"]

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Validate request host."""
        host = request.headers.get("host", "").split(":")[0]

        # Skip validation if no trusted hosts configured (for testing)
        if not self.trusted_hosts:
            return await call_next(request)

        if host and host not in self.trusted_hosts:
            logger.warning("Untrusted host attempted access: %s", host)
            return JSONResponse(
                status_code=400,
                content={
                    "error": {"code": "UNTRUSTED_HOST", "message": "Invalid host header", "type": "security_error"}
                },
            )

        return await call_next(request)
