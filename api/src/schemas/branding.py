"""
Branding response models.
"""

from pydantic import BaseModel, ConfigDict, Field


class BrandingResponse(BaseModel):
    """
    Branding response for frontend assets and environment metadata.
    """

    application_title: str = Field(..., description="Human-readable application title for UI branding.")
    favicon_url: str = Field(..., description="Primary favicon URL path.")
    apple_touch_icon_url: str | None = Field(
        None, description="Optional Apple touch icon URL for home screen shortcuts."
    )
    manifest_url: str | None = Field(None, description="Optional manifest URL for PWA configuration.")
    environment_suffix: str | None = Field(
        None, description="Optional suffix shown alongside the application title (e.g., Staging)."
    )
    version: str = Field(..., description="Application version identifier.")
    environment: str = Field(..., description="Deployment environment name.")

    model_config = ConfigDict(frozen=True)
