"""
Branding endpoint exposing environment and version metadata.
"""

from fastapi import Request, Response
from src.core.config import Settings, get_settings
from src.core.router import public_router
from src.schemas.branding import BrandingResponse

router = public_router("/branding", tags=["branding"])

DEFAULT_APPLICATION_TITLE = "AgentifUI"
DEFAULT_FAVICON_URL = "/favicon.ico"
DEFAULT_APPLE_TOUCH_ICON_URL = "/apple-touch-icon.png"
DEFAULT_MANIFEST_URL = "/manifest.json"


def _build_branding_response(settings: Settings, tenant_id: str | None = None) -> BrandingResponse:
    """
    Assemble branding payload, keeping tenant context available for future overrides.
    """
    return BrandingResponse(
        application_title=settings.branding_application_title or DEFAULT_APPLICATION_TITLE,
        favicon_url=settings.branding_favicon_url or DEFAULT_FAVICON_URL,
        apple_touch_icon_url=settings.branding_apple_touch_icon_url or DEFAULT_APPLE_TOUCH_ICON_URL,
        manifest_url=settings.branding_manifest_url or DEFAULT_MANIFEST_URL,
        environment_suffix=settings.branding_environment_suffix,
        version=settings.app_version,
        environment=settings.environment,
    )


@router.get(
    "",
    response_model=BrandingResponse,
    summary="Get branding metadata",
    description="Returns branding assets, environment suffix, and version for the frontend.",
)
async def get_branding(request: Request, response: Response) -> BrandingResponse:
    """
    Return branding information and environment metadata for frontend consumers.
    """
    settings = get_settings()
    tenant_id = getattr(request.state, "tenant_id", None)

    branding_payload = _build_branding_response(settings=settings, tenant_id=tenant_id)

    response.headers["X-App-Version"] = settings.app_version
    response.headers["X-App-Env"] = settings.environment

    return branding_payload
