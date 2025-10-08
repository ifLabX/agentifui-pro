"""
Shared API dependencies.

This file only re-exports existing dependencies for convenience.
No new functionality is added.
"""

from core.db import get_db_session

__all__ = ["get_db_session"]
