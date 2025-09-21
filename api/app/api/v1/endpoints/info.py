"""
Application information endpoint.
Implements GET /info endpoint for application metadata.
"""

from fastapi import APIRouter, status

from app.core.config.settings import get_settings
from app.schemas.info import InfoResponse

router = APIRouter(tags=["Information"])


@router.get(
    "/info",
    response_model=InfoResponse,
    status_code=status.HTTP_200_OK,
    summary="Application information",
    description="Returns application metadata including name, version, and environment information.",
)
async def get_info() -> InfoResponse:
    """
    Get application information.

    Returns metadata about the application including:
    - Application name and version
    - Current environment (development/production)
    - Python and FastAPI versions

    This endpoint is useful for:
    - Deployment verification
    - Environment validation
    - Version tracking
    - Debugging and support

    Returns:
        InfoResponse with application metadata
    """
    settings = get_settings()

    return InfoResponse.create_from_settings(
        name=settings.project_name, version=settings.project_version, debug=settings.debug
    )
