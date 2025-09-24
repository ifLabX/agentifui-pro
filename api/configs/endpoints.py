"""
Configuration endpoints for runtime configuration management and validation.

This module provides endpoints for validating configuration, testing database
connectivity, and retrieving configuration status information.
"""

import time
from typing import Annotated, Any, Optional

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, ValidationError

from configs.database import DatabaseConfig
from configs.parsing import detect_list_format
from configs.settings import EnvironmentSettings, get_settings
from configs.validation import ConfigurationValidator
from database.connection import ConnectionManager, get_connection_manager

router = APIRouter(prefix="/config", tags=["configuration"])

# Dependency instances
settings_dependency = Depends(get_settings)
connection_manager_dependency = Depends(get_connection_manager)


class DatabaseTestRequest(BaseModel):
    """Request model for testing custom database configuration."""

    host: str = Field(..., description="Database host")
    port: int = Field(..., ge=1, le=65535, description="Database port")
    username: str = Field(..., description="Database username")
    password: str = Field(..., description="Database password")
    database: str = Field(..., description="Database name")
    min_pool_size: int = Field(default=5, ge=1, le=50)
    max_pool_size: int = Field(default=20, ge=5, le=100)
    timeout_seconds: int = Field(default=30, ge=1, le=300)


class ValidationResultSection(BaseModel):
    """Validation result for a specific configuration section."""

    valid: bool = Field(..., description="Section validation status")
    issues: list[str] = Field(default_factory=list, description="Issues found")
    warnings: list[str] = Field(default_factory=list, description="Warnings")


class CorsValidationResult(ValidationResultSection):
    """CORS-specific validation result."""

    origins_format: str = Field(..., description="Detected format: comma_separated, json_array, or mixed")


class ProductionRequirements(BaseModel):
    """Production environment requirements check."""

    met: bool = Field(..., description="Whether production requirements are met")
    missing: list[str] = Field(default_factory=list, description="Missing requirements")


class SecurityValidationResult(ValidationResultSection):
    """Security-specific validation result."""

    production_requirements: Optional[ProductionRequirements] = Field(None, description="Production requirements check")


class ValidationResults(BaseModel):
    """Detailed validation results by category."""

    database: ValidationResultSection = Field(..., description="Database validation")
    cors: CorsValidationResult = Field(..., description="CORS validation")
    security: SecurityValidationResult = Field(..., description="Security validation")
    feature_flags: ValidationResultSection = Field(..., description="Feature flags validation")


class ConfigValidationResponse(BaseModel):
    """Response model for configuration validation."""

    valid: bool = Field(..., description="Overall validation status")
    environment: str = Field(..., description="Current environment")
    validation_results: ValidationResults = Field(..., description="Detailed validation results")
    warnings: list[str] = Field(default_factory=list, description="Configuration warnings")
    recommendations: list[str] = Field(default_factory=list, description="Configuration recommendations")
    timestamp: str = Field(..., description="Validation timestamp")


class ConnectionStatus(BaseModel):
    """Connection status information."""

    connected: bool = Field(..., description="Database connection status")
    response_time_ms: int = Field(..., description="Response time in milliseconds")
    last_check: str = Field(..., description="Timestamp of last check")
    error: Optional[str] = Field(None, description="Error message if connection failed")
    database_version: Optional[str] = Field(None, description="Database version")
    database_name: Optional[str] = Field(None, description="Current database name")


class DatabaseStatusResponse(BaseModel):
    """Response model for database status information."""

    configuration: dict[str, Any] = Field(..., description="Database configuration (secure)")
    connection_status: ConnectionStatus = Field(..., description="Connection status information")
    configuration_source: str = Field(
        ..., description="Configuration source: individual_fields, database_url, or mixed"
    )
    pool_status: dict[str, Any] = Field(..., description="Connection pool status")


class TestedConfiguration(BaseModel):
    """Tested database configuration information (secure)."""

    host: str = Field(..., description="Database host")
    port: int = Field(..., description="Database port")
    database: str = Field(..., description="Database name")
    driver: str = Field(..., description="Database driver")


class DatabaseInfo(BaseModel):
    """Database information for successful connections."""

    version: str = Field(..., description="Database version")
    name: Optional[str] = Field(None, description="Database name")


class ErrorDetails(BaseModel):
    """Error details for failed connections."""

    error_type: str = Field(..., description="Error classification")
    message: str = Field(..., description="Error message")
    suggestions: list[str] = Field(default_factory=list, description="Suggestions for fixing the error")


class DatabaseTestResponse(BaseModel):
    """Response model for database test results."""

    success: bool = Field(..., description="Test result")
    response_time_ms: int = Field(..., description="Response time in milliseconds")
    tested_configuration: TestedConfiguration = Field(..., description="Configuration that was tested")
    database_info: Optional[DatabaseInfo] = Field(None, description="Database info if successful")
    error_details: Optional[ErrorDetails] = Field(None, description="Error details if failed")
    timestamp: str = Field(..., description="Test timestamp")


@router.get(
    "/validate",
    response_model=ConfigValidationResponse,
    summary="Validate Configuration",
    description="Performs comprehensive validation of current configuration with environment-specific rules",
)
async def validate_configuration() -> ConfigValidationResponse:
    """
    Validate current configuration with detailed error reporting and recommendations.

    Performs comprehensive validation including:
    - Security validation with environment-specific rules
    - Database configuration validation
    - CORS origins validation
    - Production readiness checks

    Returns:
        ConfigValidationResponse: Detailed validation results
    """
    try:
        # Try to create settings to catch any validation errors
        try:
            settings = EnvironmentSettings()
        except ValidationError as ve:
            # Return 400 for configuration validation errors
            validation_errors = []
            for error in ve.errors():
                field = ".".join(str(loc) for loc in error["loc"])
                validation_errors.append(f"{field}: {error['msg']}")

            return JSONResponse(
                status_code=400,
                content={
                    "error": "Configuration validation failed",
                    "message": "Environment configuration contains validation errors",
                    "validation_errors": validation_errors,
                },
            )

        # Also try to access settings.database to trigger any validation errors
        try:
            _ = settings.database
        except ValidationError as ve:
            # Return 400 for configuration validation errors
            validation_errors = []
            for error in ve.errors():
                field = ".".join(str(loc) for loc in error["loc"])
                validation_errors.append(f"{field}: {error['msg']}")

            return JSONResponse(
                status_code=400,
                content={
                    "error": "Configuration validation failed",
                    "message": "Database configuration contains validation errors",
                    "validation_errors": validation_errors,
                },
            )

        # Perform comprehensive configuration validation
        validation_result = ConfigurationValidator.validate_configuration(settings)

        # Database validation
        database_result = ValidationResultSection(
            valid=validation_result.get("database", {}).get("valid", True),
            issues=validation_result.get("database", {}).get("issues", []),
            warnings=validation_result.get("database", {}).get("warnings", []),
        )

        # CORS validation with format detection
        cors_origins_str = ",".join(settings.cors_origins) if settings.cors_origins else ""
        detected_format = detect_list_format(cors_origins_str)

        # Map internal format names to contract expected names
        format_mapping = {
            "empty": "comma_separated",
            "single_value": "comma_separated",
            "comma_separated": "comma_separated",
            "json_array": "json_array",
            "malformed_json": "mixed",
        }
        origins_format = format_mapping.get(detected_format, "comma_separated")

        cors_result = CorsValidationResult(
            valid=validation_result.get("cors", {}).get("valid", True),
            issues=validation_result.get("cors", {}).get("issues", []),
            warnings=validation_result.get("cors", {}).get("warnings", []),
            origins_format=origins_format,
        )

        # Security validation with production requirements
        security_section = validation_result.get("secret_key", {})
        production_reqs = None

        if settings.environment == "production":
            # Check production requirements
            missing_reqs = []
            secret_key = settings.secret_key.get_secret_value()

            if len(secret_key) < 32:
                missing_reqs.append("Secret key must be at least 32 characters")
            if any(
                origin.startswith("http://")
                and not origin.startswith("http://localhost")
                and not origin.startswith("http://127.0.0.1")
                for origin in settings.cors_origins
            ):
                missing_reqs.append("Production should use HTTPS origins")

            production_reqs = ProductionRequirements(met=len(missing_reqs) == 0, missing=missing_reqs)

        security_result = SecurityValidationResult(
            valid=security_section.get("valid", True),
            issues=security_section.get("issues", []),
            warnings=security_section.get("warnings", []),
            production_requirements=production_reqs,
        )

        # Feature flags validation (placeholder for future expansion)
        feature_flags_result = ValidationResultSection(valid=True, issues=[], warnings=[])

        validation_results = ValidationResults(
            database=database_result, cors=cors_result, security=security_result, feature_flags=feature_flags_result
        )

        # Check for validation errors and return 400 if any critical issues
        if not validation_result["valid"]:
            return JSONResponse(
                status_code=400,
                content={
                    "error": "Configuration validation failed",
                    "message": "One or more configuration sections have validation errors",
                    "validation_errors": [
                        error.get("message", str(error)) for error in validation_result.get("errors", [])
                    ],
                },
            )

        # Generate warnings and recommendations
        warnings = []
        recommendations = []

        # Add warnings from validation result
        warnings.extend(validation_result.get("warnings", []))

        # Add recommendations from validation result
        recommendations.extend(validation_result.get("recommendations", []))

        # Check for JSON array format and recommend migration
        if origins_format == "json_array":
            recommendations.append(
                "Consider migrating CORS origins from JSON array format "
                "to comma-separated format for better compatibility"
            )

        return ConfigValidationResponse(
            valid=validation_result["valid"],
            environment=settings.environment,
            validation_results=validation_results,
            warnings=warnings,
            recommendations=recommendations,
            timestamp=time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
        )

    except HTTPException:
        # Re-raise HTTP exceptions (like 400 for validation errors)
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Configuration validation failed: {str(e)}")


@router.get(
    "/database/status",
    response_model=DatabaseStatusResponse,
    summary="Database Configuration Status",
    description="Returns current database configuration and connection status with pool metrics",
)
async def get_database_status(settings: EnvironmentSettings = settings_dependency) -> DatabaseStatusResponse:
    """
    Get comprehensive database configuration and connection status.

    Provides detailed information about:
    - Current database configuration (secure, no passwords)
    - Connection pool status and metrics
    - Database connectivity and performance

    Args:
        settings: Current environment settings

    Returns:
        DatabaseStatusResponse: Database status information
    """
    try:
        start_time = time.time()

        # Try to get or create connection manager
        try:
            # Create a temporary connection manager for testing
            connection_manager = ConnectionManager(settings.database)
            await connection_manager.initialize()

            # Get health check information from connection manager
            health_result = await connection_manager.health_check()

            # Get pool status
            pool_status = await connection_manager.get_pool_status()

            # Close the temporary connection manager
            await connection_manager.close()

        except Exception as conn_error:
            # Handle connection failures gracefully
            response_time_ms = int((time.time() - start_time) * 1000)
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime())

            # Determine configuration source
            config_source = _determine_configuration_source(settings)

            connection_status = ConnectionStatus(
                connected=False,
                response_time_ms=response_time_ms,
                last_check=timestamp,
                error=str(conn_error),
                database_version=None,
                database_name=None,
            )

            return DatabaseStatusResponse(
                configuration=settings.database.model_dump_secure(),
                connection_status=connection_status,
                configuration_source=config_source,
                pool_status={
                    "size": 0,
                    "active": 0,
                    "checked_out": 0,
                    "min_size": settings.database.min_pool_size,
                    "max_size": settings.database.max_pool_size,
                },
            )

        response_time_ms = int((time.time() - start_time) * 1000)
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime())

        # Determine configuration source
        config_source = _determine_configuration_source(settings)

        connection_status = ConnectionStatus(
            connected=health_result.get("connected", False),
            response_time_ms=response_time_ms,
            last_check=timestamp,
            error=health_result.get("error"),
            database_version=health_result.get("database_version"),
            database_name=health_result.get("database_name"),
        )

        return DatabaseStatusResponse(
            configuration=health_result.get("configuration", {}),
            connection_status=connection_status,
            configuration_source=config_source,
            pool_status=pool_status,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database status check failed: {str(e)}")


@router.post(
    "/database/test",
    response_model=DatabaseTestResponse,
    summary="Test Database Configuration",
    description="Tests a custom database configuration without affecting the current connection pool",
)
async def test_database_configuration(
    test_config: Annotated[DatabaseTestRequest | None, Body()] = None,  # noqa: PT028
) -> DatabaseTestResponse:
    """
    Test a custom database configuration for connectivity and performance.

    Creates a temporary connection using the provided configuration
    to validate connectivity without affecting the current application
    database connection pool.

    Args:
        test_config: Database configuration to test

    Returns:
        DatabaseTestResponse: Test results with timing and error information
    """
    try:
        start_time = time.time()

        # If no test config provided, use current settings
        if test_config is None:
            # Use current configuration
            current_settings = EnvironmentSettings()
            temp_db_config = current_settings.database
            tested_config = TestedConfiguration(
                host=temp_db_config.host,
                port=temp_db_config.port,
                database=temp_db_config.database_name,
                driver=temp_db_config.driver,
            )
        else:
            # Create temporary database configuration
            temp_db_config = DatabaseConfig(
                host=test_config.host,
                port=test_config.port,
                username=test_config.username,
                password=test_config.password,
                database_name=test_config.database,
                min_pool_size=test_config.min_pool_size,
                max_pool_size=test_config.max_pool_size,
                timeout_seconds=test_config.timeout_seconds,
            )
            tested_config = TestedConfiguration(
                host=test_config.host,
                port=test_config.port,
                database=test_config.database,
                driver="postgresql+asyncpg",  # Default driver
            )

        # Create temporary connection manager for testing
        temp_manager = ConnectionManager(temp_db_config)

        try:
            # Initialize and test the connection
            await temp_manager.initialize()

            # Perform health check to get database information
            health_result = await temp_manager.health_check()

            response_time_ms = int((time.time() - start_time) * 1000)
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime())

            if health_result.get("connected", False):
                database_info = DatabaseInfo(
                    version=health_result.get("database_version", "Unknown"), name=health_result.get("database_name")
                )

                return DatabaseTestResponse(
                    success=True,
                    response_time_ms=response_time_ms,
                    tested_configuration=tested_config,
                    database_info=database_info,
                    timestamp=timestamp,
                )
            else:
                # Classify error type based on the health result
                error_type = health_result.get("error_type", "connection_failed")
                suggestions = _get_error_suggestions(error_type, health_result.get("error", ""))
                error_details = ErrorDetails(
                    error_type=error_type,
                    message=health_result.get("error", "Connection failed"),
                    suggestions=suggestions,
                )

                return DatabaseTestResponse(
                    success=False,
                    response_time_ms=response_time_ms,
                    tested_configuration=tested_config,
                    error_details=error_details,
                    timestamp=timestamp,
                )

        finally:
            # Always clean up temporary connection manager
            await temp_manager.close()

    except Exception as e:
        response_time_ms = int((time.time() - start_time) * 1000)
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime())

        # Create tested configuration info even for errors
        if test_config is not None:
            tested_config = TestedConfiguration(
                host=test_config.host, port=test_config.port, database=test_config.database, driver="postgresql+asyncpg"
            )
        else:
            # Use current configuration for testing
            try:
                current_settings = EnvironmentSettings()
                db_config = current_settings.database
                tested_config = TestedConfiguration(
                    host=db_config.host, port=db_config.port, database=db_config.database_name, driver=db_config.driver
                )
            except Exception:
                # Fallback if current config is broken
                tested_config = TestedConfiguration(
                    host="unknown", port=5432, database="unknown", driver="postgresql+asyncpg"
                )

        # Classify error based on exception message
        error_message = str(e)
        if "timeout" in error_message.lower():
            error_type = "timeout"
        elif "authentication" in error_message.lower() or "password" in error_message.lower():
            error_type = "authentication_failed"
        elif "connection" in error_message.lower() and (
            "refused" in error_message.lower() or "failed" in error_message.lower()
        ):
            error_type = "connection_failed"
        elif "database" in error_message.lower() and (
            "not exist" in error_message.lower() or "not found" in error_message.lower()
        ):
            error_type = "database_not_found"
        else:
            error_type = "unknown"

        suggestions = _get_error_suggestions(error_type, error_message)
        error_details = ErrorDetails(
            error_type=error_type, message=f"Database test failed: {str(e)}", suggestions=suggestions
        )

        return DatabaseTestResponse(
            success=False,
            response_time_ms=response_time_ms,
            tested_configuration=tested_config,
            error_details=error_details,
            timestamp=timestamp,
        )


def _determine_configuration_source(settings: EnvironmentSettings) -> str:
    """
    Determine the configuration source for database settings.

    Args:
        settings: Environment settings instance

    Returns:
        Configuration source: "individual_fields", "database_url", or "mixed"
    """
    # Check if individual fields are being used
    has_individual_fields = settings._has_individual_database_fields()

    # Check if DATABASE_URL is set
    has_database_url = settings.database_url is not None

    if has_individual_fields and has_database_url:
        return "mixed"
    elif has_individual_fields:
        return "individual_fields"
    else:
        return "database_url"


def _get_error_suggestions(error_type: str, error_message: str) -> list[str]:
    """
    Get actionable suggestions based on error type and message.

    Args:
        error_type: Classified error type
        error_message: Original error message

    Returns:
        List of actionable suggestions
    """
    suggestions_map = {
        "timeout": [
            "Check if the database host is reachable",
            "Verify network connectivity and firewall settings",
            "Increase the connection timeout value",
            "Ensure the database server is running",
        ],
        "connection_failed": [
            "Verify the database host and port are correct",
            "Check if the database server is running",
            "Ensure network connectivity to the database server",
            "Verify firewall settings allow database connections",
        ],
        "authentication_failed": [
            "Check the database username and password",
            "Verify the user has permission to connect",
            "Ensure the database user exists",
            "Check authentication method configuration",
        ],
        "database_not_found": [
            "Verify the database name is correct",
            "Check if the database exists on the server",
            "Ensure the user has access to the specified database",
        ],
    }

    return suggestions_map.get(
        error_type,
        [
            "Check all database connection parameters",
            "Verify the database server is accessible",
            "Review the error message for specific details",
        ],
    )
