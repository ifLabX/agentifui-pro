"""
Health check endpoints for application monitoring.
Implements GET /health and GET /health/ready endpoints.
"""

from datetime import UTC, datetime

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from app.core.config.database import check_database_health
from app.schemas.health import HealthResponse, ReadinessResponse

router = APIRouter(tags=["Health"])


@router.get(
    "/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Basic health check",
    description="Returns basic application health status. Always returns healthy if the application is running.",
)
async def get_health() -> HealthResponse:
    """
    Basic health check endpoint.

    This endpoint always returns a healthy status if the application is running.
    It's designed for basic uptime monitoring and load balancer health checks.

    Returns:
        HealthResponse with status and timestamp
    """
    return HealthResponse(status="healthy", timestamp=datetime.now(UTC))


@router.get(
    "/health/ready",
    response_model=ReadinessResponse,
    responses={
        200: {
            "description": "Application is ready to serve requests",
            "model": ReadinessResponse,
        },
        503: {
            "description": "Application is not ready (e.g., database unavailable)",
            "model": ReadinessResponse,
        },
    },
    summary="Readiness check",
    description="Returns readiness status including database connectivity. Returns 200 when ready, 503 when not ready.",
)
async def get_readiness() -> JSONResponse:
    """
    Readiness check endpoint.

    This endpoint checks if the application is ready to serve requests by
    verifying database connectivity and other critical dependencies.

    Returns:
        200: Application is ready
        503: Application is not ready
    """
    # Check database connectivity
    database_healthy = await check_database_health()

    if database_healthy:
        response = ReadinessResponse.create_ready_response(database_connected=True)
        return JSONResponse(status_code=status.HTTP_200_OK, content=response.model_dump())
    else:
        response = ReadinessResponse.create_not_ready_response(database_connected=False)
        return JSONResponse(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, content=response.model_dump())
