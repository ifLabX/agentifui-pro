"""
Pydantic schemas for application info endpoint.
Based on contracts/info.yaml specification.
"""

import sys
from enum import Enum
from typing import Optional

import fastapi
from pydantic import BaseModel, Field


class Environment(str, Enum):
    """Application environment enumeration."""

    DEVELOPMENT = "development"
    PRODUCTION = "production"


class InfoResponse(BaseModel):
    """
    Response schema for GET /info endpoint.

    Returns application metadata and version information.
    """

    name: str = Field(description="Application name", example="AgentifUI-Pro Backend")
    version: str = Field(description="Application version", example="1.0.0")
    environment: Environment = Field(description="Current environment (development or production)")
    python_version: Optional[str] = Field(default=None, description="Python version", example="3.12.0")
    fastapi_version: Optional[str] = Field(default=None, description="FastAPI version", example="0.104.1")

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "AgentifUI-Pro Backend",
                "version": "1.0.0",
                "environment": "development",
                "python_version": "3.12.0",
                "fastapi_version": "0.104.1",
            }
        }
    }

    @classmethod
    def create_from_settings(cls, name: str, version: str, debug: bool) -> "InfoResponse":
        """
        Create an info response from application settings.

        Args:
            name: Application name
            version: Application version
            debug: Whether debug mode is enabled

        Returns:
            InfoResponse with application information
        """
        return cls(
            name=name,
            version=version,
            environment=Environment.DEVELOPMENT if debug else Environment.PRODUCTION,
            python_version=f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
            fastapi_version=fastapi.__version__,
        )
