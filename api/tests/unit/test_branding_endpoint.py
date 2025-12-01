from types import SimpleNamespace

import pytest
from src.api.endpoints import branding
from src.api.endpoints.branding import (
    DEFAULT_APPLE_TOUCH_ICON_URL,
    DEFAULT_APPLICATION_TITLE,
    DEFAULT_FAVICON_URL,
    DEFAULT_MANIFEST_URL,
)


@pytest.mark.asyncio
async def test_branding_endpoint_returns_defaults() -> None:
    settings = SimpleNamespace(
        branding_application_title=None,
        branding_favicon_url=None,
        branding_apple_touch_icon_url=None,
        branding_manifest_url=None,
        branding_environment_suffix=None,
        app_version="0.1.0",
        environment="staging",
    )

    result = await branding.get_branding(settings=settings)

    assert result.application_title == DEFAULT_APPLICATION_TITLE
    assert result.favicon_url == DEFAULT_FAVICON_URL
    assert result.apple_touch_icon_url == DEFAULT_APPLE_TOUCH_ICON_URL
    assert result.manifest_url == DEFAULT_MANIFEST_URL
    assert result.environment_suffix is None
    assert result.version == "0.1.0"
    assert result.environment == "staging"


@pytest.mark.asyncio
async def test_branding_endpoint_uses_setting_overrides() -> None:
    settings = SimpleNamespace(
        branding_application_title="Custom UI",
        branding_favicon_url="/custom.ico",
        branding_apple_touch_icon_url="/touch.png",
        branding_manifest_url="/site.webmanifest",
        branding_environment_suffix="Preview",
        app_version="9.9.9",
        environment="production",
    )

    result = await branding.get_branding(settings=settings)

    assert result.application_title == "Custom UI"
    assert result.favicon_url == "/custom.ico"
    assert result.apple_touch_icon_url == "/touch.png"
    assert result.manifest_url == "/site.webmanifest"
    assert result.environment_suffix == "Preview"
    assert result.version == "9.9.9"
    assert result.environment == "production"
