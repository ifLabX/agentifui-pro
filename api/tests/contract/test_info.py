"""
Contract tests for GET /info endpoint.
Based on contracts/info.yaml specification.
"""

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    """Create test client for info endpoint tests."""
    # This will fail until we implement the main app
    from app.main import app

    return TestClient(app)


def test_info_endpoint_returns_200(client):
    """Test that GET /info returns 200 status code."""
    response = client.get("/api/v1/info")
    assert response.status_code == 200


def test_info_endpoint_response_structure(client):
    """Test that GET /info returns correct response structure."""
    response = client.get("/api/v1/info")

    assert response.status_code == 200
    data = response.json()

    # Check required fields exist
    assert "name" in data
    assert "version" in data
    assert "environment" in data

    # Check field types
    assert isinstance(data["name"], str)
    assert isinstance(data["version"], str)
    assert isinstance(data["environment"], str)

    # Check enum values for environment
    assert data["environment"] in ["development", "production"]


def test_info_endpoint_optional_fields(client):
    """Test optional fields in /info response."""
    response = client.get("/api/v1/info")

    assert response.status_code == 200
    data = response.json()

    # Optional fields should be strings if present
    if "python_version" in data:
        assert isinstance(data["python_version"], str)

    if "fastapi_version" in data:
        assert isinstance(data["fastapi_version"], str)


def test_info_endpoint_expected_values(client):
    """Test that /info returns expected application information."""
    response = client.get("/api/v1/info")

    assert response.status_code == 200
    data = response.json()

    # Check expected application name
    assert data["name"] == "AgentifUI-Pro Backend"

    # Version should follow semantic versioning pattern
    version = data["version"]
    assert len(version.split(".")) >= 2  # At least major.minor

    # Environment should be development for tests
    assert data["environment"] in ["development", "production"]


def test_info_endpoint_response_content_type(client):
    """Test that GET /info returns application/json content type."""
    response = client.get("/api/v1/info")

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"


def test_info_endpoint_no_authentication_required(client):
    """Test that GET /info works without authentication."""
    # Info endpoint should work without any headers or auth
    response = client.get("/api/v1/info")
    assert response.status_code == 200
