"""
Performance tests for health endpoints.

These tests validate that health endpoints respond within acceptable time limits
and can handle concurrent requests without degradation.
"""

import asyncio
import statistics
import time
from concurrent.futures import ThreadPoolExecutor
from unittest.mock import patch

import httpx
import pytest
from fastapi.testclient import TestClient


def test_health_endpoint_response_time() -> None:
    """Test that /health endpoint responds within 200ms."""
    from src.main import app

    client = TestClient(app)

    # Warm up the endpoint
    client.get("/health")

    # Measure response time
    start_time = time.time()
    response = client.get("/health")
    end_time = time.time()

    response_time = (end_time - start_time) * 1000

    assert response.status_code == 200
    assert response_time < 200, f"Health endpoint took {response_time:.2f}ms, should be <200ms"


def test_health_db_endpoint_response_time(mock_database_health: dict[str, bool | int | str]) -> None:
    """Test that /health/db endpoint responds within 500ms."""
    from src.main import app

    client = TestClient(app)

    # Warm up the endpoint
    try:
        client.get("/health/db")
    except Exception:
        # Endpoint might fail due to no database, that's OK for timing test
        pass

    # Measure response time
    start_time = time.time()
    response = client.get("/health/db")
    end_time = time.time()

    response_time = (end_time - start_time) * 1000

    # Accept both 200 (connected) and 503 (not connected) for timing test
    assert response.status_code in [200, 503]
    assert response_time < 500, f"DB health endpoint took {response_time:.2f}ms, should be <500ms"


def test_health_endpoint_concurrent_requests() -> None:
    """Test health endpoint performance under concurrent load."""
    from src.main import app

    client = TestClient(app)

    def make_request() -> dict[str, int | float]:
        """Make a single request and return response time."""
        start_time = time.time()
        response = client.get("/health")
        end_time = time.time()
        return {"status_code": response.status_code, "response_time_ms": (end_time - start_time) * 1000}

    # Test with 10 concurrent requests
    num_requests = 10
    with ThreadPoolExecutor(max_workers=num_requests) as executor:
        futures = [executor.submit(make_request) for _ in range(num_requests)]
        results = [future.result() for future in futures]

    # Analyze results
    response_times = [r["response_time_ms"] for r in results]
    successful_requests = sum(1 for r in results if r["status_code"] == 200)

    # All requests should succeed
    assert successful_requests == num_requests, f"Only {successful_requests}/{num_requests} requests succeeded"

    # Average response time should still be reasonable
    avg_response_time = statistics.mean(response_times)
    max_response_time = max(response_times)

    assert avg_response_time < 200, f"Average response time {avg_response_time:.2f}ms exceeds 200ms"
    assert max_response_time < 500, f"Max response time {max_response_time:.2f}ms exceeds 500ms"


@pytest.mark.asyncio
async def test_async_health_endpoint_performance() -> None:
    """Test health endpoint performance using async client."""
    from src.main import app

    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        # Warm up
        await client.get("/health")

        # Measure single request
        start_time = time.time()
        response = await client.get("/health")
        end_time = time.time()

        response_time = (end_time - start_time) * 1000

        assert response.status_code == 200
        assert response_time < 200, f"Async health endpoint took {response_time:.2f}ms, should be <200ms"


@pytest.mark.asyncio
async def test_async_concurrent_health_requests() -> None:
    """Test concurrent async requests to health endpoint."""
    from src.main import app

    async def make_async_request(client: httpx.AsyncClient) -> dict[str, int | float]:
        """Make async request and return response time."""
        start_time = time.time()
        response = await client.get("/health")
        end_time = time.time()
        return {"status_code": response.status_code, "response_time_ms": (end_time - start_time) * 1000}

    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        # Test with 20 concurrent async requests
        tasks = [make_async_request(client) for _ in range(20)]
        results = await asyncio.gather(*tasks)

    # Analyze results
    response_times = [r["response_time_ms"] for r in results]
    successful_requests = sum(1 for r in results if r["status_code"] == 200)

    assert successful_requests == 20, f"Only {successful_requests}/20 async requests succeeded"

    avg_response_time = statistics.mean(response_times)
    max_response_time = max(response_times)

    assert avg_response_time < 200, f"Async average response time {avg_response_time:.2f}ms exceeds 200ms"
    assert max_response_time < 500, f"Async max response time {max_response_time:.2f}ms exceeds 500ms"


def test_health_endpoint_memory_usage() -> None:
    """Test that health endpoint doesn't have memory leaks under load."""
    import os

    import psutil
    from src.main import app

    client = TestClient(app)

    # Get initial memory usage
    process = psutil.Process(os.getpid())
    initial_memory = process.memory_info().rss

    # Make many requests to check for memory leaks
    for _ in range(100):
        response = client.get("/health")
        assert response.status_code == 200

    # Check memory usage after requests
    final_memory = process.memory_info().rss
    memory_increase = final_memory - initial_memory

    # Allow up to 10MB increase (reasonable for test overhead)
    max_allowed_increase = 10 * 1024 * 1024  # 10MB

    assert memory_increase < max_allowed_increase, (
        f"Memory increased by {memory_increase / 1024 / 1024:.2f}MB, "
        f"which exceeds {max_allowed_increase / 1024 / 1024}MB limit"
    )


def test_error_response_performance() -> None:
    """Test that error responses are also fast."""
    from src.main import app

    client = TestClient(app)

    # Test 404 response time
    start_time = time.time()
    response = client.get("/nonexistent-endpoint")
    end_time = time.time()

    response_time = (end_time - start_time) * 1000

    assert response.status_code == 404
    assert response_time < 100, f"404 error response took {response_time:.2f}ms, should be <100ms"


@pytest.mark.asyncio
async def test_database_health_performance_with_mock() -> None:
    """Test database health endpoint performance with mocked database."""
    from unittest.mock import AsyncMock

    from src.main import app

    # Mock successful database connection
    with (
        patch("src.api.endpoints.health.check_database_connection", new_callable=AsyncMock) as mock_conn,
        patch("src.api.endpoints.health.get_database_info", new_callable=AsyncMock) as mock_info,
    ):
        mock_conn.return_value = True
        mock_info.return_value = {
            "connected": True,
            "pool_size": 10,
            "checked_out_connections": 2,
            "version": "PostgreSQL 14.0",
        }

        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
            start_time = time.time()
            response = await client.get("/health/db")
            end_time = time.time()

            response_time = (end_time - start_time) * 1000

            assert response.status_code == 200
            assert response_time < 200, f"Mocked DB health took {response_time:.2f}ms, should be <200ms"


def test_health_endpoints_under_stress(mock_database_health: dict[str, bool | int | str]) -> None:
    """Stress test both health endpoints with rapid requests."""
    from src.main import app

    client = TestClient(app)

    def stress_test_endpoint(endpoint: str, expected_max_time: float) -> None:
        """Stress test a specific endpoint."""
        response_times: list[float] = []
        errors = 0

        for _ in range(50):  # 50 rapid requests
            try:
                start_time = time.time()
                response = client.get(endpoint)
                end_time = time.time()

                response_time = (end_time - start_time) * 1000
                response_times.append(response_time)

                # Accept both success and expected failure codes
                if endpoint == "/health":
                    assert response.status_code == 200
                elif endpoint == "/health/db":
                    assert response.status_code in [200, 503]

            except Exception:
                errors += 1

        # Analyze stress test results
        if response_times:
            avg_time = statistics.mean(response_times)
            max_time = max(response_times)
            p95_time = sorted(response_times)[int(len(response_times) * 0.95)]

            assert avg_time < expected_max_time, (
                f"{endpoint} average time {avg_time:.2f}ms exceeds {expected_max_time}ms under stress"
            )
            assert p95_time < expected_max_time * 2, (
                f"{endpoint} 95th percentile time {p95_time:.2f}ms too high under stress"
            )

        # Allow some errors under extreme stress, but not too many
        error_rate = errors / 50
        assert error_rate < 0.1, f"{endpoint} error rate {error_rate:.2%} too high under stress"

    # Stress test both endpoints
    stress_test_endpoint("/health", 200)
    stress_test_endpoint("/health/db", 500)
