"""
Tests for tenant context middleware validation.
"""

import uuid

from fastapi.testclient import TestClient


def test_tenant_query_param_rejected(client: TestClient) -> None:
    """Query parameters must not supply tenant identifiers."""
    response = client.get("/health", params={"tenant_id": "123"})

    assert response.status_code == 400
    body = response.json()
    assert body["message"] == "tenant_id must be provided via the x-tenant-id header"


def test_invalid_tenant_header_rejected(client: TestClient) -> None:
    """Invalid tenant header values should fail fast."""
    response = client.get("/health", headers={"x-tenant-id": "not-a-uuid"})

    assert response.status_code == 400
    assert "must be a valid UUID" in response.json()["message"]


def test_valid_tenant_header_allows_request(client: TestClient) -> None:
    """Valid headers should pass through without blocking."""
    response = client.get("/health", headers={"x-tenant-id": str(uuid.uuid4())})

    assert response.status_code in (200, 503)
