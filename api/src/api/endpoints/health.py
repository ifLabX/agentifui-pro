"""
Health check endpoints for application monitoring.

This module implements health check endpoints following the OpenAPI
specification in contracts/health.yaml for container orchestration.
"""

import logging
import time
from pathlib import Path

from alembic.config import Config
from alembic.runtime.migration import MigrationContext
from alembic.script import ScriptDirectory
from alembic.util.exc import CommandError
from fastapi.responses import JSONResponse
from redis.exceptions import RedisError
from sqlalchemy.exc import SQLAlchemyError
from src.core.config import get_settings
from src.core.db import check_database_connection, get_async_engine, get_database_info
from src.core.redis import ping_redis
from src.core.router import public_router
from src.schemas.health import (
    ConnectionPoolInfo,
    DatabaseHealthResponse,
    HealthResponse,
    MigrationStatus,
    RedisHealthResponse,
    create_healthy_database_response,
    create_healthy_redis_response,
    create_healthy_response,
    create_unhealthy_database_response,
    create_unhealthy_redis_response,
    create_unhealthy_response,
)

router = public_router("/health", tags=["health"])

# Application start time for uptime calculation
APP_START_TIME = time.time()
logger = logging.getLogger(__name__)


def _find_project_root(marker: str = "alembic.ini") -> Path | None:
    """
    Walk upward from this file to locate the project root by marker file.
    """
    current = Path(__file__).resolve().parent
    for candidate in (current, *current.parents):
        if (candidate / marker).is_file():
            return candidate
    return None


def _load_alembic_config() -> Config:
    """
    Build an Alembic Config with absolute paths to avoid CWD sensitivity.

    Returns:
        Config: Alembic configuration pointing at this service's migration scripts
    """
    project_root = _find_project_root()
    if project_root is None:
        raise FileNotFoundError("Unable to locate alembic.ini for migration status check")

    config = Config(str(project_root / "alembic.ini"))
    config.set_main_option("script_location", str(project_root / "migrations"))
    config.set_main_option("sqlalchemy.url", get_settings().database_url)
    config.attributes["configure_logger"] = False
    return config


async def _get_migration_status() -> MigrationStatus:
    """
    Determine whether the database is at the latest Alembic head revision.
    """
    try:
        alembic_config = _load_alembic_config()
        script_dir = ScriptDirectory.from_config(alembic_config)
        head_revision = script_dir.get_current_head()
    except (FileNotFoundError, CommandError) as exc:  # pragma: no cover - defensive; falls back to UNKNOWN
        logger.warning("Failed to resolve Alembic head revision: %s", exc)
        return MigrationStatus.UNKNOWN
    except Exception as exc:  # pragma: no cover - defensive; falls back to UNKNOWN
        logger.exception("Unexpected error resolving Alembic head revision")
        return MigrationStatus.UNKNOWN

    try:
        engine = get_async_engine()
        async with engine.connect() as connection:
            current_revision = await connection.run_sync(
                lambda sync_conn: MigrationContext.configure(connection=sync_conn).get_current_revision()
            )
    except SQLAlchemyError as exc:  # pragma: no cover - defensive; falls back to UNKNOWN
        logger.warning("Failed to resolve current migration revision: %s", exc)
        return MigrationStatus.UNKNOWN
    except Exception as exc:  # pragma: no cover - defensive; falls back to UNKNOWN
        logger.exception("Unexpected error resolving current migration revision")
        return MigrationStatus.UNKNOWN

    if not head_revision or not current_revision:
        return MigrationStatus.UNKNOWN

    if current_revision == head_revision:
        return MigrationStatus.UP_TO_DATE

    return MigrationStatus.PENDING


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
async def get_application_health() -> JSONResponse:
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
async def get_database_health() -> JSONResponse:
    """
    Get database health status.

    Performs comprehensive database connectivity and performance checks
    including connection pool status, response time, and migration status.

    Returns:
        DatabaseHealthResponse: Database health status with metrics
    """
    try:
        start_time = time.time()
        settings = get_settings()

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

        migration_status = await _get_migration_status()

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


@router.get(
    "/redis",
    response_model=RedisHealthResponse,
    responses={
        200: {"description": "Redis is healthy"},
        503: {
            "description": "Redis is unhealthy",
            "model": RedisHealthResponse,
        },
    },
    summary="Redis Health Check",
    description="Returns the health status of the Redis cache connection",
)
async def get_redis_health() -> JSONResponse:
    """
    Get Redis health status.

    Performs a Redis PING with timeout to verify connectivity and latency.

    Returns:
        RedisHealthResponse: Redis health status with metrics
    """
    start_time = time.time()
    settings = get_settings()
    error_msg: str | None = None
    is_connected = False

    try:
        is_connected = await ping_redis(timeout_seconds=settings.redis_health_check_timeout)
        if not is_connected:
            error_msg = "Redis ping failed"
    except (TimeoutError, RedisError) as e:
        error_msg = f"Redis health check failed: {str(e)}"
    except Exception as e:
        error_msg = f"Unexpected Redis error: {str(e)}"

    response_time_ms = int((time.time() - start_time) * 1000)

    if is_connected:
        response = create_healthy_redis_response(response_time_ms=response_time_ms)
        return JSONResponse(status_code=200, content=response.model_dump())

    response = create_unhealthy_redis_response(
        errors=[error_msg or "Unknown Redis error"],
        response_time_ms=response_time_ms,
    )
    return JSONResponse(status_code=503, content=response.model_dump())
