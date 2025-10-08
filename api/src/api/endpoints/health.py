"""
Health check endpoints for application monitoring.

This module implements health check endpoints following the OpenAPI
specification in contracts/health.yaml for container orchestration.
"""

import time
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import get_settings
from core.db import check_database_connection, get_database_info, get_db_session
from schemas.health import (
    ConnectionPoolInfo,
    DatabaseHealthResponse,
    HealthResponse,
    MigrationStatus,
    create_healthy_database_response,
    create_healthy_response,
    create_unhealthy_database_response,
    create_unhealthy_response,
)

router = APIRouter(prefix="/health", tags=["health"])

# Application start time for uptime calculation
APP_START_TIME = time.time()


@router.get(
    "",
    response_model=HealthResponse,
    responses={
        200: {"description": "Application is healthy"},
        503: {"description": "Application is unhealthy", "model": HealthResponse},
    },
    summary="Application Health Check",
    description="Returns the overall health status of the FastAPI application",
)
async def get_application_health():
    """
    Get application health status.

    Returns overall application health including version, uptime,
    and basic application status without database connectivity checks.

    Returns:
        HealthResponse: Application health status
    """
    try:
        settings = get_settings()
        current_time = time.time()
        uptime_seconds = int(current_time - APP_START_TIME)

        # Basic health checks (can be extended with more checks)
        errors: list[str] = []

        # Check if critical settings are available
        if not settings.app_name:
            errors.append("Application name not configured")

        if not settings.app_version:
            errors.append("Application version not configured")

        # Return healthy or unhealthy based on checks
        if errors:
            response = create_unhealthy_response(
                version=settings.app_version,
                errors=errors,
                uptime_seconds=uptime_seconds,
            )
            return JSONResponse(status_code=503, content=response.model_dump())

        response = create_healthy_response(
            version=settings.app_version,
            uptime_seconds=uptime_seconds,
        )
        return JSONResponse(status_code=200, content=response.model_dump())

    except Exception as e:
        # Return unhealthy status for any unexpected errors
        # Safely get version without failing if settings are unavailable
        version = "unknown"
        try:
            version = get_settings().app_version
        except Exception:
            pass  # Use 'unknown' if settings fail to load

        response = create_unhealthy_response(
            version=version,
            errors=[f"Health check failed: {str(e)}"],
            uptime_seconds=int(time.time() - APP_START_TIME),
        )
        return JSONResponse(status_code=503, content=response.model_dump())


@router.get(
    "/db",
    response_model=DatabaseHealthResponse,
    responses={
        200: {"description": "Database is healthy"},
        503: {
            "description": "Database is unhealthy",
            "model": DatabaseHealthResponse,
        },
    },
    summary="Database Health Check",
    description="Returns the health status of the PostgreSQL database connection",
)
async def get_database_health(
    db: Annotated[AsyncSession, Depends(get_db_session)],
):
    """
    Get database health status.

    Performs comprehensive database connectivity and performance checks
    including connection pool status, response time, and migration status.

    Args:
        db: Database session dependency

    Returns:
        DatabaseHealthResponse: Database health status with metrics
    """
    try:
        settings = get_settings()
        start_time = time.time()

        # Check basic database connectivity
        is_connected = await check_database_connection()

        if not is_connected:
            response = create_unhealthy_database_response(
                errors=["Database connection failed"],
            )
            return JSONResponse(status_code=503, content=response.model_dump())

        # Get detailed database information
        db_info = await get_database_info()
        response_time_ms = int((time.time() - start_time) * 1000)

        if not db_info.get("connected", False):
            error_msg = db_info.get("error", "Unknown database error")
            response = create_unhealthy_database_response(
                errors=[f"Database error: {error_msg}"],
                response_time_ms=response_time_ms,
            )
            return JSONResponse(status_code=503, content=response.model_dump())

        # Create connection pool info if available
        connection_pool = None
        if db_info.get("pool_size") is not None:
            connection_pool = ConnectionPoolInfo(
                active_connections=db_info.get("checked_out_connections", 0),
                pool_size=db_info.get("pool_size", 0),
            )

        # Check migration status (placeholder for future Alembic integration)
        migration_status = MigrationStatus.UNKNOWN

        # Return healthy database response
        response = create_healthy_database_response(
            connection_pool=connection_pool,
            response_time_ms=response_time_ms,
            migration_status=migration_status,
        )
        return JSONResponse(status_code=200, content=response.model_dump())

    except Exception as e:
        # Calculate response time even for errors
        response_time_ms = int((time.time() - start_time) * 1000)

        response = create_unhealthy_database_response(
            errors=[f"Database health check failed: {str(e)}"],
            response_time_ms=response_time_ms,
        )
        return JSONResponse(status_code=503, content=response.model_dump())
