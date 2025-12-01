import json
from collections.abc import Mapping

import pytest
from fastapi import HTTPException
from pydantic import BaseModel
from pydantic import ValidationError as PydanticValidationError
from sqlalchemy.exc import SQLAlchemyError
from src.core.config import reset_settings, reset_settings_async
from src.core.exceptions import TenantContextError
from src.middleware.error_handler import ErrorHandlerMiddleware
from starlette.requests import Request


def _make_request(headers: Mapping[str, str] | None = None) -> Request:
    header_bytes = []
    for key, value in (headers or {}).items():
        header_bytes.append((key.lower().encode(), value.encode()))

    scope = {
        "type": "http",
        "asgi": {"version": "3.0", "spec_version": "2.1"},
        "http_version": "1.1",
        "method": "GET",
        "path": "/",
        "raw_path": b"/",
        "root_path": "",
        "scheme": "http",
        "query_string": b"",
        "headers": header_bytes,
        "client": ("testserver", 80),
        "server": ("testserver", 80),
    }
    return Request(scope)


@pytest.fixture
def middleware(monkeypatch: pytest.MonkeyPatch) -> ErrorHandlerMiddleware:
    monkeypatch.setenv("DEBUG", "0")
    reset_settings()
    return ErrorHandlerMiddleware(lambda scope, receive, send: None)


@pytest.mark.asyncio
async def test_http_exception_translated(middleware: ErrorHandlerMiddleware) -> None:
    request = _make_request({"x-request-id": "req-123"})
    response = await middleware._handle_http_exception(request, HTTPException(status_code=404, detail="gone"))  # type: ignore[attr-defined]
    body = json.loads(response.body)

    assert response.status_code == 404
    assert body["error"] == "NOT_FOUND_ERROR"
    assert body["request_id"] == "req-123"


@pytest.mark.asyncio
async def test_validation_errors_are_formatted(middleware: ErrorHandlerMiddleware) -> None:
    class _Payload(BaseModel):
        value: int

    with pytest.raises(PydanticValidationError) as exc:
        _Payload.model_validate({"value": "bad"})

    response = await middleware._handle_validation_error(_make_request(), exc.value)  # type: ignore[attr-defined]

    body = json.loads(response.body)

    assert response.status_code == 422
    assert body["error"] == "VALIDATION_ERROR"
    assert body["validation_errors"][0]["field"] == "value"


@pytest.mark.asyncio
async def test_database_errors_are_normalized(middleware: ErrorHandlerMiddleware) -> None:
    response = await middleware._handle_database_error(_make_request(), SQLAlchemyError("broken"))  # type: ignore[attr-defined]
    body = json.loads(response.body)

    assert response.status_code == 503
    assert body["error"] == "DATABASE_CONNECTION_ERROR"
    assert body["detail"] is None


@pytest.mark.asyncio
async def test_tenant_context_error_returns_validation(middleware: ErrorHandlerMiddleware) -> None:
    response = await middleware._handle_tenant_context_error(_make_request(), TenantContextError("missing tenant"))  # type: ignore[attr-defined]
    body = json.loads(response.body)

    assert response.status_code == 400
    assert body["error"] == "VALIDATION_ERROR"
    assert "missing tenant" in body["message"]


@pytest.mark.asyncio
async def test_unexpected_errors_include_detail_when_debug(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DEBUG", "1")
    await reset_settings_async()
    middleware = ErrorHandlerMiddleware(lambda scope, receive, send: None)

    request = _make_request()
    request.state.request_id = "state-id"
    response = await middleware._handle_unexpected_error(request, ValueError("boom"))  # type: ignore[attr-defined]
    body = json.loads(response.body)

    assert response.status_code == 500
    assert body["error"] == "INTERNAL_SERVER_ERROR"
    assert "boom" in (body.get("detail") or "")
    assert body["request_id"] == "state-id"
