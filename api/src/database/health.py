"""
Database health monitoring utilities.

This module provides utilities for monitoring database connection health,
connection pool status, and database performance metrics.
"""

import asyncio
import logging
import time
from typing import Any, Optional

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncEngine

from config.settings import get_settings
from database.connection import get_async_engine

logger = logging.getLogger(__name__)


class DatabaseHealthMonitor:
    """
    Database health monitoring utilities.

    Provides methods to check database connectivity, monitor connection pool
    status, and measure database response times.
    """

    def __init__(self, engine: Optional[AsyncEngine] = None):
        """
        Initialize database health monitor.

        Args:
            engine: Optional SQLAlchemy async engine. If not provided,
                   will use the default engine from get_async_engine()
        """
        self.engine = engine or get_async_engine()
        self.settings = get_settings()

    async def check_database_health(self) -> dict[str, Any]:
        """
        Comprehensive database health check.

        Returns:
            Dict containing database health status, connection info,
            response time, and pool statistics
        """
        health_status = {
            "connected": False,
            "response_time_ms": None,
            "connection_pool": None,
            "database_info": None,
            "errors": [],
        }

        try:
            # Test basic connectivity and measure response time
            start_time = time.time()

            async with self.engine.connect() as conn:
                # Simple query to test connectivity
                result = await conn.execute(text("SELECT 1 as test"))
                test_value = result.scalar()

                if test_value == 1:
                    health_status["connected"] = True

                # Measure response time
                response_time = (time.time() - start_time) * 1000
                health_status["response_time_ms"] = round(response_time, 2)

                # Get database version and info
                try:
                    version_result = await conn.execute(text("SELECT version()"))
                    version = version_result.scalar()
                    health_status["database_info"] = {
                        "version": version.split(",")[0] if version else "Unknown",
                        "driver": "asyncpg",
                    }
                except Exception as e:
                    logger.warning("Could not retrieve database version: %s", e)
                    health_status["database_info"] = {"version": "Unknown", "driver": "asyncpg"}

        except SQLAlchemyError as e:
            logger.exception("Database health check failed")
            health_status["errors"].append(f"Database connection error: {str(e)}")
        except Exception as e:
            logger.exception("Unexpected error during health check")
            health_status["errors"].append(f"Unexpected error: {str(e)}")

        # Get connection pool information
        try:
            pool_info = self.get_connection_pool_info()
            health_status["connection_pool"] = pool_info
        except Exception as e:
            logger.warning("Could not retrieve pool information: %s", e)
            health_status["errors"].append(f"Pool info error: {str(e)}")

        return health_status

    def get_connection_pool_info(self) -> dict[str, Any]:
        """
        Get connection pool statistics.

        Returns:
            Dict containing pool size, active connections, and other metrics
        """
        pool_info = {
            "pool_size": None,
            "active_connections": None,
            "checked_out_connections": None,
            "overflow_connections": None,
            "invalid_connections": None,
        }

        try:
            pool = self.engine.pool

            if hasattr(pool, "size"):
                pool_info["pool_size"] = pool.size()
            if hasattr(pool, "checkedin"):
                pool_info["active_connections"] = pool.checkedin()
            if hasattr(pool, "checkedout"):
                pool_info["checked_out_connections"] = pool.checkedout()
            if hasattr(pool, "overflow"):
                pool_info["overflow_connections"] = pool.overflow()
            if hasattr(pool, "invalidated"):
                pool_info["invalid_connections"] = pool.invalidated()

        except Exception as e:
            logger.warning("Could not retrieve detailed pool metrics: %s", e)
            # Fallback to basic pool information
            if hasattr(self.engine, "pool") and hasattr(self.engine.pool, "_creator"):
                pool_info["pool_size"] = "Available"
                pool_info["active_connections"] = "Monitoring"

        return pool_info

    async def check_database_connectivity(self) -> bool:
        """
        Simple connectivity check.

        Returns:
            True if database is reachable, False otherwise
        """
        try:
            async with self.engine.connect() as conn:
                result = await conn.execute(text("SELECT 1"))
                return result.scalar() == 1
        except Exception as e:
            logger.exception("Database connectivity check failed")
            return False

    async def measure_response_time(self, query: str = "SELECT 1") -> Optional[float]:
        """
        Measure database response time for a specific query.

        Args:
            query: SQL query to execute for timing measurement

        Returns:
            Response time in milliseconds, or None if failed
        """
        try:
            start_time = time.time()

            async with self.engine.connect() as conn:
                await conn.execute(text(query))

            response_time = (time.time() - start_time) * 1000
            return round(response_time, 2)

        except Exception as e:
            logger.exception("Response time measurement failed")
            return None

    async def test_connection_pool(self, concurrent_connections: int = 5) -> dict[str, Any]:
        """
        Test connection pool behavior under load.

        Args:
            concurrent_connections: Number of concurrent connections to test

        Returns:
            Dict containing test results and pool performance metrics
        """
        test_results = {
            "concurrent_connections_tested": concurrent_connections,
            "successful_connections": 0,
            "failed_connections": 0,
            "average_response_time_ms": None,
            "max_response_time_ms": None,
            "min_response_time_ms": None,
            "errors": [],
        }

        async def test_single_connection():
            """Test a single database connection."""
            try:
                start_time = time.time()
                async with self.engine.connect() as conn:
                    await conn.execute(text("SELECT 1"))
                response_time = (time.time() - start_time) * 1000
                return True, response_time
            except Exception as e:
                return False, None

        # Run concurrent connection tests
        tasks = [test_single_connection() for _ in range(concurrent_connections)]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        response_times = []

        for result in results:
            if isinstance(result, Exception):
                test_results["failed_connections"] += 1
                test_results["errors"].append(str(result))
            else:
                success, response_time = result
                if success:
                    test_results["successful_connections"] += 1
                    if response_time is not None:
                        response_times.append(response_time)
                else:
                    test_results["failed_connections"] += 1

        # Calculate response time statistics
        if response_times:
            test_results["average_response_time_ms"] = round(sum(response_times) / len(response_times), 2)
            test_results["max_response_time_ms"] = round(max(response_times), 2)
            test_results["min_response_time_ms"] = round(min(response_times), 2)

        return test_results


# Convenience functions for standalone usage
async def check_database_health() -> dict[str, Any]:
    """
    Standalone function to check database health.

    Returns:
        Dict containing comprehensive database health information
    """
    monitor = DatabaseHealthMonitor()
    return await monitor.check_database_health()


async def check_database_connectivity() -> bool:
    """
    Standalone function to check basic database connectivity.

    Returns:
        True if database is reachable, False otherwise
    """
    monitor = DatabaseHealthMonitor()
    return await monitor.check_database_connectivity()


async def get_connection_pool_status() -> dict[str, Any]:
    """
    Standalone function to get connection pool status.

    Returns:
        Dict containing connection pool information
    """
    monitor = DatabaseHealthMonitor()
    return monitor.get_connection_pool_info()
