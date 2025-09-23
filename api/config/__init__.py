"""
Configuration package initialization.

This module provides application configuration management.
"""
from config.settings import Settings, get_settings

__all__ = [
    "Settings",
    "get_settings",
]