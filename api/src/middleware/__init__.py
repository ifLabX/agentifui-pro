"""
Middleware package initialization.

This module provides FastAPI middleware components.
"""

from src.middleware.error_handler import ErrorHandlerMiddleware, setup_error_handling

__all__ = [
    "ErrorHandlerMiddleware",
    "setup_error_handling",
]
