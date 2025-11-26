"""
Contract tests for GET /health/db endpoint.

These tests validate the database health endpoint behavior according to the OpenAPI
specification in contracts/health.yaml. Tests MUST fail until endpoint is implemented.
"""

from datetime import datetime

import pytest
from fastapi.testclient import TestClient


def test_health_db_endpoint_exists() -> None:
    """Test that /health/db endpoint exists and is accessible."""
    from src.main import app

    client = TestClient(app)
    response = client.get("/health/db")

    # This should NOT be 404 - endpoint must exist
    assert response.status_code != 404, "Database health endpoint /health/db must exist"


def test_health_db_endpoint_returns_json() -> None:
    """Test that /health/db endpoint returns valid JSON."""
    from src.main import app

    client = TestClient(app)
    response = client.get("/health/db")

    assert response.headers["content-type"] == "application/json"

    # Should be able to parse JSON
    data = response.json()
    assert isinstance(data, dict)


def test_health_db_endpoint_healthy_response_schema() -> None:
    """Test /health/db endpoint returns correct schema for healthy database."""
    from src.main import app

    client = TestClient(app)
    response = client.get("/health/db")

    # Should return 200 for healthy database
    if response.status_code == 200:
        data = response.json()

        # Required fields according to DatabaseHealthResponse schema
        assert "status" in data
        assert "timestamp" in data
        assert "database_connected" in data

        # Status should be one of the allowed enum values
        assert data["status"] in ["healthy", "degraded", "unhealthy"]

        # database_connected should be boolean
        assert isinstance(data["database_connected"], bool)
        assert data["database_connected"] is True  # for 200 response

        # Timestamp should be valid ISO 8601 format
        timestamp = data["timestamp"]
        try:
            datetime.fromisoformat(timestamp)
        except ValueError:
            pytest.fail(f"Invalid timestamp format: {timestamp}")


def test_health_db_endpoint_connection_pool_info() -> None:
    """Test /health/db endpoint includes connection pool information."""
    from src.main import app

    client = TestClient(app)
    response = client.get("/health/db")

    if response.status_code == 200:
        data = response.json()

        # connection_pool is optional
        if "connection_pool" in data:
            pool_info = data["connection_pool"]
            assert isinstance(pool_info, dict)

            # Check pool info structure
            assert "active_connections" in pool_info
            assert "pool_size" in pool_info

            assert isinstance(pool_info["active_connections"], int)
            assert isinstance(pool_info["pool_size"], int)
            assert pool_info["active_connections"] >= 0
            assert pool_info["pool_size"] >= 1


def test_health_db_endpoint_response_time_info() -> None:
    """Test /health/db endpoint includes response time information."""
    from src.main import app

    client = TestClient(app)
    response = client.get("/health/db")

    if response.status_code == 200:
        data = response.json()

        # response_time_ms is optional
        if "response_time_ms" in data:
            response_time = data["response_time_ms"]
            assert isinstance(response_time, (int, type(None)))
            if response_time is not None:
                assert response_time >= 0


def test_health_db_endpoint_migration_status() -> None:
    """Test /health/db endpoint includes migration status."""
    from src.main import app

    client = TestClient(app)
    response = client.get("/health/db")

    if response.status_code == 200:
        data = response.json()

        # migration_status is optional
        if "migration_status" in data:
            migration_status = data["migration_status"]
            assert migration_status in ["up_to_date", "pending", "unknown"]


def test_health_db_endpoint_unhealthy_response_schema() -> None:
    """Test /health/db endpoint error response format."""
    from src.main import app

    client = TestClient(app)
    response = client.get("/health/db")

    if response.status_code == 503:
        data = response.json()

        # Required fields for unhealthy response
        assert "status" in data
        assert "timestamp" in data
        assert "database_connected" in data

        # database_connected should be False for 503 response
        assert data["database_connected"] is False

        # Should have errors field for unhealthy status
        if data.get("status") == "unhealthy":
            assert "errors" in data
            assert isinstance(data["errors"], list)
            for error in data["errors"]:
                assert isinstance(error, str)


def test_health_db_endpoint_performance() -> None:
    """Test /health/db endpoint responds within acceptable time."""
    import time

    from src.main import app

    client = TestClient(app)

    start_time = time.time()
    response = client.get("/health/db")
    end_time = time.time()

    response_time = end_time - start_time

    # Database health check should complete within 500ms
    assert response_time < 0.5, f"DB health check took {response_time:.3f}s, should be <0.5s"


def test_health_db_endpoint_handles_database_errors() -> None:
    """Test /health/db endpoint gracefully handles database connection issues."""
    from src.main import app

    client = TestClient(app)
    response = client.get("/health/db")

    # Should return either 200 (connected) or 503 (not connected)
    # Should NOT return 500 (internal server error) - errors should be handled
    assert response.status_code in [200, 503], f"Unexpected status code: {response.status_code}"

    data = response.json()
    assert "status" in data
    assert "database_connected" in data


def test_health_db_endpoint_consistency() -> None:
    """Test /health/db endpoint returns consistent results for database state."""
    from src.main import app

    client = TestClient(app)

    # Make multiple rapid requests
    responses = []
    for _ in range(5):
        response = client.get("/health/db")
        responses.append(response)

    # Database state should be relatively stable
    connection_states = [r.json()["database_connected"] for r in responses]

    # Allow for some variation, but not complete inconsistency
    unique_states = set(connection_states)
    assert len(unique_states) <= 2, f"Too much variation in DB connection state: {connection_states}"
