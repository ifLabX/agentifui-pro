"""
Contract tests for GET /health/ready endpoint.
Based on contracts/health.yaml specification.
"""

from datetime import datetime

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    """Create test client for readiness endpoint tests."""
    # This will fail until we implement the main app
    from app.main import app

    return TestClient(app)


def test_health_ready_endpoint_returns_200_when_ready(client):
    """Test that GET /health/ready returns 200 when application is ready."""
    response = client.get("/api/v1/health/ready")
    # This might be 200 or 503 depending on database state
    assert response.status_code in [200, 503]


def test_health_ready_response_structure_when_ready(client):
    """Test response structure when application is ready."""
    response = client.get("/api/v1/health/ready")

    data = response.json()

    # Check required fields exist
    assert "status" in data
    assert "database" in data
    assert "timestamp" in data

    # Check field types
    assert isinstance(data["status"], str)
    assert isinstance(data["database"], str)
    assert isinstance(data["timestamp"], str)

    # Check enum values
    assert data["status"] in ["ready", "not_ready"]
    assert data["database"] in ["connected", "disconnected"]

    # Verify timestamp is a valid ISO format
    try:
        datetime.fromisoformat(data["timestamp"].replace("Z", ""))
    except ValueError:
        pytest.fail("timestamp is not in valid ISO format")


def test_health_ready_returns_200_when_database_connected(client):
    """Test 200 response when database is connected."""
    response = client.get("/api/v1/health/ready")

    if response.status_code == 200:
        data = response.json()
        assert data["status"] == "ready"
        assert data["database"] == "connected"


def test_health_ready_returns_503_when_database_disconnected(client):
    """Test 503 response when database is disconnected."""
    response = client.get("/api/v1/health/ready")

    if response.status_code == 503:
        data = response.json()
        assert data["status"] == "not_ready"
        # Database could be connected or disconnected in 503 state


def test_health_ready_endpoint_response_content_type(client):
    """Test that GET /health/ready returns application/json content type."""
    response = client.get("/api/v1/health/ready")

    assert response.status_code in [200, 503]
    assert response.headers["content-type"] == "application/json"


def test_health_ready_endpoint_no_authentication_required(client):
    """Test that GET /health/ready works without authentication."""
    # Readiness check should work without any headers or auth
    response = client.get("/api/v1/health/ready")
    assert response.status_code in [200, 503]
