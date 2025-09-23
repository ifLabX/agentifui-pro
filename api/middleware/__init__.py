"""
Middleware package initialization.

This module provides FastAPI middleware components.
"""

from middleware.error_handler import ErrorHandlerMiddleware, setup_error_handling

__all__ = [
    "ErrorHandlerMiddleware",
    "setup_error_handling",
]
