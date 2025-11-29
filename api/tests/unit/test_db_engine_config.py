from types import SimpleNamespace

from src.core import db


def _fake_settings() -> SimpleNamespace:
    return SimpleNamespace(
        app_name="Test API",
        database_url="postgresql+asyncpg://user:pass@localhost:5432/test",
        database_pool_size=5,
        database_pool_max_overflow=10,
        database_pool_timeout=30,
        database_pool_recycle=1800,
        debug=False,
    )


def test_async_engine_uses_utc_timezone(monkeypatch) -> None:
    db.reset_engine()
    settings = _fake_settings()
    captured: dict[str, object] = {}

    def fake_create_async_engine(url: str, **kwargs: object) -> object:
        captured["url"] = url
        captured["kwargs"] = kwargs

        class _FakeEngine:
            pool = None

        return _FakeEngine()

    monkeypatch.setattr(db, "create_async_engine", fake_create_async_engine)
    monkeypatch.setattr(db, "get_settings", lambda: settings)

    try:
        engine = db.get_async_engine()
        assert engine is not None

        server_settings = captured["kwargs"]["connect_args"]["server_settings"]  # type: ignore[index]
        assert server_settings["TimeZone"] == "UTC"  # type: ignore[index]
        assert server_settings["application_name"] == settings.app_name  # type: ignore[index]
        assert captured["url"] == settings.database_url
    finally:
        db.reset_engine()


def test_testing_engine_uses_utc_timezone(monkeypatch) -> None:
    settings = _fake_settings()
    captured: dict[str, object] = {}

    def fake_create_async_engine(url: str, **kwargs: object) -> str:
        captured["url"] = url
        captured["kwargs"] = kwargs
        return "engine"

    monkeypatch.setattr(db, "create_async_engine", fake_create_async_engine)
    monkeypatch.setattr(db, "get_settings", lambda: settings)

    engine = db.get_async_engine_for_testing()

    server_settings = captured["kwargs"]["connect_args"]["server_settings"]  # type: ignore[index]
    assert server_settings["TimeZone"] == "UTC"  # type: ignore[index]
    assert server_settings["application_name"] == settings.app_name  # type: ignore[index]
    assert captured["url"] == settings.database_url
    assert engine == "engine"
