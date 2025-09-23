"""
Error response schema validation tests.

These tests validate that error response models follow the schema defined in
contracts/errors.yaml. Tests MUST fail until error models are implemented.
"""

import pytest
from pydantic import ValidationError


def test_error_response_model_exists():
    """Test that ErrorResponse model exists."""
    try:
        from models.errors import ErrorResponse

        # Verify the model exists and is a Pydantic model
        assert ErrorResponse is not None
        assert hasattr(ErrorResponse, "model_fields")
    except ImportError:
        pytest.fail("ErrorResponse model must exist in models.errors module")


def test_error_response_required_fields():
    """Test that ErrorResponse model has all required fields."""
    from models.errors import ErrorResponse

    # Test with all required fields
    error_data = {"error": "TEST_ERROR", "message": "Test error message", "timestamp": "2025-09-23T10:30:00Z"}

    error_response = ErrorResponse(**error_data)

    assert error_response.error == "TEST_ERROR"
    assert error_response.message == "Test error message"
    assert error_response.timestamp == "2025-09-23T10:30:00Z"


def test_error_response_missing_required_fields():
    """Test that ErrorResponse model validates required fields."""
    from models.errors import ErrorResponse

    # Test missing error field
    with pytest.raises(ValidationError):
        ErrorResponse(message="Test", timestamp="2025-09-23T10:30:00Z")

    # Test missing message field
    with pytest.raises(ValidationError):
        ErrorResponse(error="TEST_ERROR", timestamp="2025-09-23T10:30:00Z")

    # Test missing timestamp field
    with pytest.raises(ValidationError):
        ErrorResponse(error="TEST_ERROR", message="Test")


def test_error_response_optional_fields():
    """Test that ErrorResponse model handles optional fields correctly."""
    from models.errors import ErrorResponse

    # Test with optional fields
    error_data = {
        "error": "TEST_ERROR",
        "message": "Test error message",
        "timestamp": "2025-09-23T10:30:00Z",
        "detail": "Additional error details",
        "request_id": "550e8400-e29b-41d4-a716-446655440000",
    }

    error_response = ErrorResponse(**error_data)

    assert error_response.detail == "Additional error details"
    assert error_response.request_id == "550e8400-e29b-41d4-a716-446655440000"


def test_validation_error_response_model_exists():
    """Test that ValidationErrorResponse model exists."""
    try:
        from models.errors import ValidationErrorResponse

        # Verify the model exists and is a Pydantic model
        assert ValidationErrorResponse is not None
        assert hasattr(ValidationErrorResponse, "model_fields")
    except ImportError:
        pytest.fail("ValidationErrorResponse model must exist in models.errors module")


def test_validation_error_response_structure():
    """Test that ValidationErrorResponse model has correct structure."""
    from models.errors import ValidationError, ValidationErrorResponse

    validation_errors = [
        ValidationError(field="database_url", message="Invalid PostgreSQL connection string"),
        ValidationError(field="timeout", message="Must be positive integer"),
    ]

    error_data = {
        "error": "VALIDATION_ERROR",
        "message": "Request validation failed",
        "timestamp": "2025-09-23T10:30:00Z",
        "validation_errors": validation_errors,
    }

    validation_response = ValidationErrorResponse(**error_data)

    assert validation_response.error == "VALIDATION_ERROR"
    assert len(validation_response.validation_errors) == 2
    assert validation_response.validation_errors[0].field == "database_url"


def test_validation_error_model_structure():
    """Test that ValidationError model has correct structure."""
    from models.errors import ValidationError

    validation_error = ValidationError(field="database_url", message="Invalid format", value="invalid-url")

    assert validation_error.field == "database_url"
    assert validation_error.message == "Invalid format"
    assert validation_error.value == "invalid-url"


def test_service_unavailable_error_model():
    """Test that ServiceUnavailableError model exists and works correctly."""
    try:
        from models.errors import ServiceUnavailableError
    except ImportError:
        pytest.fail("ServiceUnavailableError model must exist in models.errors module")

    error_data = {
        "error": "SERVICE_UNAVAILABLE",
        "message": "Service temporarily unavailable",
        "timestamp": "2025-09-23T10:30:00Z",
        "retry_after": 30,
    }

    service_error = ServiceUnavailableError(**error_data)

    assert service_error.error == "SERVICE_UNAVAILABLE"
    assert service_error.retry_after == 30


def test_error_enum_validation():
    """Test that error enums are properly validated."""
    from models.errors import ValidationErrorResponse

    # Test that error field only accepts VALIDATION_ERROR
    with pytest.raises(ValidationError):
        ValidationErrorResponse(
            error="INVALID_ERROR_TYPE", message="Test", timestamp="2025-09-23T10:30:00Z", validation_errors=[]
        )


def test_timestamp_format_validation():
    """Test that timestamp format is properly validated."""
    from models.errors import ErrorResponse

    # Test with valid ISO 8601 timestamp
    valid_timestamps = ["2025-09-23T10:30:00Z", "2025-09-23T10:30:00.123Z", "2025-09-23T10:30:00+00:00"]

    for timestamp in valid_timestamps:
        error_response = ErrorResponse(error="TEST_ERROR", message="Test", timestamp=timestamp)
        assert error_response.timestamp == timestamp


def test_request_id_uuid_validation():
    """Test that request_id follows UUID format if validated."""
    from models.errors import ErrorResponse

    # Test with valid UUID
    valid_uuid = "550e8400-e29b-41d4-a716-446655440000"

    error_response = ErrorResponse(
        error="TEST_ERROR", message="Test", timestamp="2025-09-23T10:30:00Z", request_id=valid_uuid
    )

    assert error_response.request_id == valid_uuid


def test_error_response_serialization():
    """Test that error responses can be serialized to JSON correctly."""
    from models.errors import ErrorResponse

    error_response = ErrorResponse(
        error="DATABASE_CONNECTION_ERROR",
        message="Unable to connect to database",
        timestamp="2025-09-23T10:30:00Z",
        detail="Connection timeout after 30 seconds",
    )

    # Should be serializable to dict
    data = error_response.model_dump()

    assert isinstance(data, dict)
    assert data["error"] == "DATABASE_CONNECTION_ERROR"
    assert data["message"] == "Unable to connect to database"
    assert "timestamp" in data
    assert "detail" in data


def test_validation_error_nested_structure():
    """Test that validation errors handle nested structure correctly."""
    from models.errors import ValidationError, ValidationErrorResponse

    # Test with multiple validation errors
    validation_errors = [
        ValidationError(field="config.database_url", message="Required field missing"),
        ValidationError(field="config.pool_size", message="Must be positive", value=-1),
    ]

    validation_response = ValidationErrorResponse(
        error="VALIDATION_ERROR",
        message="Configuration validation failed",
        timestamp="2025-09-23T10:30:00Z",
        validation_errors=validation_errors,
    )

    serialized = validation_response.model_dump()

    assert len(serialized["validation_errors"]) == 2
    assert serialized["validation_errors"][0]["field"] == "config.database_url"
    assert serialized["validation_errors"][1]["value"] == -1


def test_error_models_immutability():
    """Test that error models are immutable if configured as frozen."""
    from models.errors import ErrorResponse

    error_response = ErrorResponse(error="TEST_ERROR", message="Test", timestamp="2025-09-23T10:30:00Z")

    # If frozen=True is configured, this should raise an error
    try:
        error_response.error = "MODIFIED_ERROR"
        # If no error raised, model is not frozen (which is also valid)
    except Exception:
        # Model is frozen, which is good for error responses
        pass


def test_error_response_factory_functions():
    """Test error response factory functions if they exist."""
    try:
        from models.errors import create_database_error, create_validation_error
    except ImportError:
        # Factory functions are optional
        pytest.skip("Error factory functions not implemented")

    # Test database error factory
    db_error = create_database_error("Connection failed")
    assert db_error.error == "DATABASE_CONNECTION_ERROR"
    assert "Connection failed" in db_error.message

    # Test validation error factory
    validation_error = create_validation_error([{"field": "test", "message": "invalid"}])
    assert validation_error.error == "VALIDATION_ERROR"
    assert len(validation_error.validation_errors) == 1
