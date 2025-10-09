"""
Contract tests for GET /health endpoint.

These tests validate the health endpoint behavior according to the OpenAPI specification
in contracts/health.yaml. Tests MUST fail until endpoint is implemented.
"""

from datetime import datetime

import pytest
from fastapi.testclient import TestClient


def test_health_endpoint_exists() -> None:
    """Test that /health endpoint exists and is accessible."""
    from main import app

    client = TestClient(app)
    response = client.get("/health")

    # This should NOT be 404 - endpoint must exist
    assert response.status_code != 404, "Health endpoint /health must exist"


def test_health_endpoint_returns_json() -> None:
    """Test that /health endpoint returns valid JSON."""
    from main import app

    client = TestClient(app)
    response = client.get("/health")

    assert response.headers["content-type"] == "application/json"

    # Should be able to parse JSON
    data = response.json()
    assert isinstance(data, dict)


def test_health_endpoint_healthy_response_schema() -> None:
    """Test /health endpoint returns correct schema for healthy status."""
    from main import app

    client = TestClient(app)
    response = client.get("/health")

    # Should return 200 for healthy application
    assert response.status_code == 200

    data = response.json()

    # Required fields according to HealthResponse schema
    assert "status" in data
    assert "timestamp" in data
    assert "version" in data

    # Status should be one of the allowed enum values
    assert data["status"] in ["healthy", "degraded", "unhealthy"]

    # Timestamp should be valid ISO 8601 format
    timestamp = data["timestamp"]
    try:
        datetime.fromisoformat(timestamp)
    except ValueError:
        pytest.fail(f"Invalid timestamp format: {timestamp}")

    # Version should be a string
    assert isinstance(data["version"], str)
    assert data["version"] == "0.1.0"


def test_health_endpoint_uptime_field() -> None:
    """Test /health endpoint includes uptime_seconds field."""
    from main import app

    client = TestClient(app)
    response = client.get("/health")

    data = response.json()

    # uptime_seconds is optional but recommended
    if "uptime_seconds" in data:
        assert isinstance(data["uptime_seconds"], int)
        assert data["uptime_seconds"] >= 0


def test_health_endpoint_error_response_schema() -> None:
    """Test /health endpoint error response format."""
    from main import app

    client = TestClient(app)

    # This test might pass if app is healthy, that's OK
    # We're testing the schema structure, not forcing errors
    response = client.get("/health")

    if response.status_code == 503:
        data = response.json()

        # Should have errors field for unhealthy status
        if data.get("status") == "unhealthy":
            assert "errors" in data
            assert isinstance(data["errors"], list)
            for error in data["errors"]:
                assert isinstance(error, str)


def test_health_endpoint_performance() -> None:
    """Test /health endpoint responds quickly."""
    import time

    from main import app

    client = TestClient(app)

    start_time = time.time()
    response = client.get("/health")
    end_time = time.time()

    response_time = end_time - start_time

    # Health check should be fast (<200ms as per requirements)
    assert response_time < 0.2, f"Health check took {response_time:.3f}s, should be <0.2s"


def test_health_endpoint_no_query_parameters() -> None:
    """Test /health endpoint works without query parameters."""
    from main import app

    client = TestClient(app)
    response = client.get("/health")

    # Should work without any parameters
    assert response.status_code in [200, 503]

    data = response.json()
    assert "status" in data


def test_health_endpoint_idempotent() -> None:
    """Test /health endpoint is idempotent (multiple calls return consistent results)."""
    from main import app

    client = TestClient(app)

    # Make multiple requests
    responses = []
    for _ in range(3):
        response = client.get("/health")
        responses.append(response)

    # All responses should have same status code
    status_codes = [r.status_code for r in responses]
    assert len(set(status_codes)) == 1, f"Inconsistent status codes: {status_codes}"

    # Status field should be consistent
    statuses = [r.json()["status"] for r in responses]
    assert len(set(statuses)) == 1, f"Inconsistent status values: {statuses}"
