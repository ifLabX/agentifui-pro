from types import SimpleNamespace

import pytest
from fastapi import Request, Response
from src.api.endpoints import branding


@pytest.mark.asyncio
async def test_branding_endpoint_returns_defaults(monkeypatch: pytest.MonkeyPatch) -> None:
    settings = SimpleNamespace(
        branding_application_title=None,
        branding_favicon_url=None,
        branding_apple_touch_icon_url=None,
        branding_manifest_url=None,
        branding_environment_suffix=None,
        app_version="0.1.0",
        environment="staging",
    )
    monkeypatch.setattr(branding, "get_settings", lambda: settings)

    response = Response()

    result = await branding.get_branding(response=response)

    assert result.application_title == "AgentifUI"
    assert result.favicon_url == "/favicon.ico"
    assert result.apple_touch_icon_url == "/apple-touch-icon.png"
    assert result.manifest_url == "/manifest.json"
    assert result.environment_suffix is None
    assert result.version == "0.1.0"
    assert result.environment == "staging"
    assert response.headers["X-App-Version"] == "0.1.0"
    assert response.headers["X-App-Env"] == "staging"


@pytest.mark.asyncio
async def test_branding_endpoint_uses_setting_overrides(monkeypatch: pytest.MonkeyPatch) -> None:
    settings = SimpleNamespace(
        branding_application_title="Custom UI",
        branding_favicon_url="/custom.ico",
        branding_apple_touch_icon_url="/touch.png",
        branding_manifest_url="/site.webmanifest",
        branding_environment_suffix="Preview",
        app_version="9.9.9",
        environment="production",
    )
    monkeypatch.setattr(branding, "get_settings", lambda: settings)

    response = Response()

    result = await branding.get_branding(response=response)

    assert result.application_title == "Custom UI"
    assert result.favicon_url == "/custom.ico"
    assert result.apple_touch_icon_url == "/touch.png"
    assert result.manifest_url == "/site.webmanifest"
    assert result.environment_suffix == "Preview"
    assert result.version == "9.9.9"
    assert result.environment == "production"
    assert response.headers["X-App-Version"] == "9.9.9"
    assert response.headers["X-App-Env"] == "production"
