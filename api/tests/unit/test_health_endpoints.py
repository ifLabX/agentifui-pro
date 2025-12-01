import json
from types import SimpleNamespace

import pytest
from src.api.endpoints import health
from src.schemas.health import MigrationStatus


def test_find_project_root_returns_none_for_missing_marker() -> None:
    assert health._find_project_root(marker="does-not-exist.txt") is None  # type: ignore[attr-defined]


@pytest.mark.asyncio
async def test_application_health_reports_missing_config(monkeypatch: pytest.MonkeyPatch) -> None:
    settings = SimpleNamespace(app_name="", app_version="")
    monkeypatch.setattr(health, "get_settings", lambda: settings)

    response = await health.get_application_health()
    body = json.loads(response.body)

    assert response.status_code == 503
    assert body["errors"]


@pytest.mark.asyncio
async def test_application_health_handles_unexpected_error(monkeypatch: pytest.MonkeyPatch) -> None:
    def _raise() -> None:
        raise ValueError("boom")

    monkeypatch.setattr(health, "get_settings", _raise)

    response = await health.get_application_health()
    body = json.loads(response.body)

    assert response.status_code == 503
    assert any("boom" in error for error in body["errors"])


@pytest.mark.asyncio
async def test_database_health_handles_connection_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    async def _fail_connection() -> bool:
        return False

    monkeypatch.setattr(health, "check_database_connection", _fail_connection)

    response = await health.get_database_health()
    body = json.loads(response.body)

    assert response.status_code == 503
    assert "Database connection failed" in body["errors"][0]


@pytest.mark.asyncio
async def test_database_health_handles_info_error(monkeypatch: pytest.MonkeyPatch) -> None:
    async def _connected() -> bool:
        return True

    async def _info_error() -> dict:
        return {"connected": False, "error": "boom"}

    monkeypatch.setattr(health, "check_database_connection", _connected)
    monkeypatch.setattr(health, "get_database_info", _info_error)

    response = await health.get_database_health()
    body = json.loads(response.body)

    assert response.status_code == 503
    assert "boom" in body["errors"][0]


@pytest.mark.asyncio
async def test_get_migration_status_returns_unknown_when_config_missing(monkeypatch: pytest.MonkeyPatch) -> None:
    def _missing_config():
        raise FileNotFoundError()

    monkeypatch.setattr(health, "_load_alembic_config", _missing_config)  # type: ignore[attr-defined]

    status = await health._get_migration_status()  # type: ignore[attr-defined]

    assert status == MigrationStatus.UNKNOWN


@pytest.mark.asyncio
async def test_redis_health_handles_timeout(monkeypatch: pytest.MonkeyPatch) -> None:
    settings = SimpleNamespace(redis_health_check_timeout=0.1)
    monkeypatch.setattr(health, "get_settings", lambda: settings)

    async def _timeout(timeout_seconds: float) -> bool:
        raise TimeoutError("slow")

    monkeypatch.setattr(health, "ping_redis", _timeout)

    response = await health.get_redis_health()
    body = json.loads(response.body)

    assert response.status_code == 503
    assert "slow" in body["errors"][0]
