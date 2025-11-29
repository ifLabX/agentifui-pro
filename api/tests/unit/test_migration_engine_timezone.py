import asyncio
import importlib
import sys
from contextlib import nullcontext
from types import ModuleType, SimpleNamespace


def _stub_alembic_modules(monkeypatch) -> None:
    ctx_module = ModuleType("alembic.context")
    ctx_config = SimpleNamespace(
        config_file_name=None,
        set_main_option=lambda *args, **kwargs: None,
        get_main_option=lambda *args, **kwargs: "",
    )
    ctx_module.config = ctx_config
    ctx_module.configure = lambda *args, **kwargs: None
    ctx_module.is_offline_mode = lambda: True
    ctx_module.begin_transaction = lambda: nullcontext()
    ctx_module.run_migrations = lambda: None

    alembic_module = ModuleType("alembic")
    alembic_module.context = ctx_module

    monkeypatch.setitem(sys.modules, "alembic", alembic_module)
    monkeypatch.setitem(sys.modules, "alembic.context", ctx_module)


class _FakeConnection:
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False

    async def run_sync(self, fn):
        return fn(None)


class _FakeEngine:
    def __init__(self):
        self.connection = _FakeConnection()

    def connect(self):
        return self.connection

    async def dispose(self):
        return None


def test_migration_engine_uses_utc_timezone(monkeypatch) -> None:
    _stub_alembic_modules(monkeypatch)
    env = importlib.import_module("migrations.env")

    captured: dict[str, object] = {}

    def fake_create_async_engine(url: str, **kwargs: object) -> _FakeEngine:
        captured["url"] = url
        captured["kwargs"] = kwargs
        return _FakeEngine()

    monkeypatch.setattr(env, "create_async_engine", fake_create_async_engine)
    monkeypatch.setattr(env, "do_run_migrations", lambda conn: None)
    monkeypatch.setattr(
        env,
        "settings",
        SimpleNamespace(
            database_url="postgresql+asyncpg://user:pass@localhost:5432/testdb",
            app_name="Test App",
        ),
    )

    asyncio.run(env.run_async_migrations())

    server_settings = captured["kwargs"]["connect_args"]["server_settings"]  # type: ignore[index]
    assert server_settings["TimeZone"] == "UTC"  # type: ignore[index]
    assert server_settings["application_name"] == "Test App"  # type: ignore[index]
    assert captured["url"] == "postgresql+asyncpg://user:pass@localhost:5432/testdb"
