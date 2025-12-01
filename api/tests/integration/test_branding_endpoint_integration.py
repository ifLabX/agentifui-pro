import pytest
from src.api.endpoints.branding import DEFAULT_APPLICATION_TITLE, DEFAULT_FAVICON_URL
from src.core.config import get_settings


@pytest.mark.asyncio
async def test_branding_endpoint_returns_payload(async_client) -> None:
    response = await async_client.get("/branding")

    assert response.status_code == 200

    payload = response.json()
    settings = get_settings()

    expected_title = settings.branding_application_title or DEFAULT_APPLICATION_TITLE
    expected_favicon = settings.branding_favicon_url or DEFAULT_FAVICON_URL

    assert payload["application_title"] == expected_title
    assert payload["favicon_url"] == expected_favicon
    assert payload["environment"] == settings.environment
    assert payload["version"] == settings.app_version
    assert payload["environment_suffix"] == settings.branding_environment_suffix
