import os
from unittest.mock import patch

import pytest
from src.api.endpoints.branding import (
    DEFAULT_APPLE_TOUCH_ICON_URL,
    DEFAULT_APPLICATION_TITLE,
    DEFAULT_FAVICON_URL,
    DEFAULT_MANIFEST_URL,
)
from src.core.config import get_settings, reset_settings_async


@pytest.mark.asyncio
async def test_branding_endpoint_returns_defaults(async_client) -> None:
    with patch.dict(
        os.environ,
        {
            "BRANDING_APPLICATION_TITLE": "",
            "BRANDING_FAVICON_URL": "",
            "BRANDING_APPLE_TOUCH_ICON_URL": "",
            "BRANDING_MANIFEST_URL": "",
            "BRANDING_ENVIRONMENT_SUFFIX": "",
        },
        clear=False,
    ):
        await reset_settings_async()
        response = await async_client.get("/branding")

    assert response.status_code == 200

    payload = response.json()
    settings = get_settings()

    assert payload["application_title"] == DEFAULT_APPLICATION_TITLE
    assert payload["favicon_url"] == DEFAULT_FAVICON_URL
    assert payload["apple_touch_icon_url"] == DEFAULT_APPLE_TOUCH_ICON_URL
    assert payload["manifest_url"] == DEFAULT_MANIFEST_URL
    assert payload["environment"] == settings.environment
    assert payload["version"] == settings.app_version
    assert payload["environment_suffix"] is None


@pytest.mark.asyncio
async def test_branding_endpoint_applies_overrides(async_client) -> None:
    with patch.dict(
        os.environ,
        {
            "BRANDING_APPLICATION_TITLE": "Custom Title",
            "BRANDING_FAVICON_URL": "/custom.ico",
            "BRANDING_APPLE_TOUCH_ICON_URL": "/custom-touch.png",
            "BRANDING_MANIFEST_URL": "/custom.webmanifest",
            "BRANDING_ENVIRONMENT_SUFFIX": "Preview",
        },
        clear=False,
    ):
        await reset_settings_async()
        response = await async_client.get("/branding")

    assert response.status_code == 200

    payload = response.json()
    settings = get_settings()

    assert payload["application_title"] == "Custom Title"
    assert payload["favicon_url"] == "/custom.ico"
    assert payload["apple_touch_icon_url"] == "/custom-touch.png"
    assert payload["manifest_url"] == "/custom.webmanifest"
    assert payload["environment"] == settings.environment
    assert payload["version"] == settings.app_version
    assert payload["environment_suffix"] == "Preview"
