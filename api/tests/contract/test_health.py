"""
Contract tests for GET /health endpoint.
Based on contracts/health.yaml specification.
"""

from datetime import datetime

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    """Create test client for health endpoint tests."""
    # This will fail until we implement the main app
    from app.main import app

    return TestClient(app)


def test_health_endpoint_returns_200(client):
    """Test that GET /health returns 200 status code."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200


def test_health_endpoint_response_structure(client):
    """Test that GET /health returns correct response structure."""
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    data = response.json()

    # Check required fields exist
    assert "status" in data
    assert "timestamp" in data

    # Check field types and values
    assert data["status"] == "healthy"
    assert isinstance(data["timestamp"], str)

    # Verify timestamp is a valid ISO format
    try:
        datetime.fromisoformat(data["timestamp"].replace("Z", ""))
    except ValueError:
        pytest.fail("timestamp is not in valid ISO format")


def test_health_endpoint_response_content_type(client):
    """Test that GET /health returns application/json content type."""
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"


def test_health_endpoint_no_authentication_required(client):
    """Test that GET /health works without authentication."""
    # Health check should work without any headers or auth
    response = client.get("/api/v1/health")
    assert response.status_code == 200
