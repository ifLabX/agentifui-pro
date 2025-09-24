"""
Test database configuration composition and field validation.

Tests the DatabaseConfig model with field validation, URL composition,
and backward compatibility with DATABASE_URL format.
"""

import pytest
from pydantic import ValidationError

# These imports will fail until the implementation is complete
try:
    from configs.database import DatabaseConfig
except ImportError:
    # Mock the class for contract testing
    class DatabaseConfig:
        def __init__(self, **kwargs):
            pass


class TestDatabaseConfiguration:
    """Test database configuration model and validation."""

    def test_database_config_from_individual_fields(self):
        """Test creating database config from individual fields."""
        # This test will FAIL until DatabaseConfig is implemented
        config = DatabaseConfig(
            host="localhost",
            port=5432,
            username="test_user",
            password="test_password",
            database="test_db",
            driver="postgresql+asyncpg"
        )

        assert config.host == "localhost"
        assert config.port == 5432
        assert config.username == "test_user"
        assert config.password == "test_password"
        assert config.database == "test_db"
        assert config.driver == "postgresql+asyncpg"

    def test_database_config_url_composition(self):
        """Test automatic database URL composition from fields."""
        config = DatabaseConfig(
            host="localhost",
            port=5432,
            username="test_user",
            password="test_password",
            database="test_db",
            driver="postgresql+asyncpg"
        )

        expected_url = "postgresql+asyncpg://test_user:test_password@localhost:5432/test_db"
        assert config.database_url == expected_url

    def test_database_config_from_database_url(self):
        """Test creating database config from DATABASE_URL (backward compatibility)."""
        database_url = "postgresql+asyncpg://user:pass@example.com:5433/mydb"

        config = DatabaseConfig.from_database_url(database_url)

        assert config.host == "example.com"
        assert config.port == 5433
        assert config.username == "user"
        assert config.password == "pass"
        assert config.database == "mydb"
        assert config.driver == "postgresql+asyncpg"

    def test_database_config_field_validation(self):
        """Test field validation for database configuration."""
        # Test invalid port
        with pytest.raises(ValidationError) as exc_info:
            DatabaseConfig(
                host="localhost",
                port=70000,  # Invalid port
                username="test_user",
                password="test_password",
                database="test_db"
            )

        errors = exc_info.value.errors()
        assert any(error["loc"] == ("port",) for error in errors)

        # Test invalid host
        with pytest.raises(ValidationError) as exc_info:
            DatabaseConfig(
                host="",  # Empty host
                port=5432,
                username="test_user",
                password="test_password",
                database="test_db"
            )

        errors = exc_info.value.errors()
        assert any(error["loc"] == ("host",) for error in errors)

    def test_database_config_default_values(self):
        """Test default values for optional fields."""
        config = DatabaseConfig(
            host="localhost",
            username="test_user",
            password="test_password",
            database="test_db"
        )

        # Should use default values
        assert config.port == 5432  # Default PostgreSQL port
        assert config.driver == "postgresql+asyncpg"  # Default driver
        assert config.timeout_seconds == 30  # Default timeout

    def test_database_config_driver_validation(self):
        """Test driver validation for supported database drivers."""
        # Test valid driver
        config = DatabaseConfig(
            host="localhost",
            port=5432,
            username="test_user",
            password="test_password",
            database="test_db",
            driver="postgresql+asyncpg"
        )
        assert config.driver == "postgresql+asyncpg"

        # Test invalid driver
        with pytest.raises(ValidationError) as exc_info:
            DatabaseConfig(
                host="localhost",
                port=5432,
                username="test_user",
                password="test_password",
                database="test_db",
                driver="invalid-driver"
            )

        errors = exc_info.value.errors()
        assert any(error["loc"] == ("driver",) for error in errors)

    def test_database_config_timeout_validation(self):
        """Test timeout field validation."""
        # Valid timeout
        config = DatabaseConfig(
            host="localhost",
            username="test_user",
            password="test_password",
            database="test_db",
            timeout_seconds=10
        )
        assert config.timeout_seconds == 10

        # Invalid timeout (negative)
        with pytest.raises(ValidationError) as exc_info:
            DatabaseConfig(
                host="localhost",
                username="test_user",
                password="test_password",
                database="test_db",
                timeout_seconds=-5
            )

        errors = exc_info.value.errors()
        assert any(error["loc"] == ("timeout_seconds",) for error in errors)

    def test_database_config_special_characters_in_password(self):
        """Test handling of special characters in password."""
        config = DatabaseConfig(
            host="localhost",
            port=5432,
            username="test_user",
            password="p@ssw0rd!#$%^&*()",
            database="test_db"
        )

        # Password should be URL-encoded in the composed URL
        database_url = config.database_url
        assert "p%40ssw0rd%21%23%24%25%5E%26%2A%28%29" in database_url

    def test_database_config_url_parsing_edge_cases(self):
        """Test parsing edge cases for DATABASE_URL."""
        # URL with special characters
        database_url = "postgresql+asyncpg://user:p@ssw0rd@localhost:5432/test_db"
        config = DatabaseConfig.from_database_url(database_url)

        assert config.username == "user"
        assert config.password == "p@ssw0rd"
        assert config.host == "localhost"
        assert config.database == "test_db"

        # URL without port (should use default)
        database_url = "postgresql+asyncpg://user:pass@localhost/test_db"
        config = DatabaseConfig.from_database_url(database_url)

        assert config.port == 5432  # Default PostgreSQL port

    def test_database_config_serialization(self):
        """Test configuration serialization for logging and debugging."""
        config = DatabaseConfig(
            host="localhost",
            port=5432,
            username="test_user",
            password="sensitive_password",
            database="test_db"
        )

        # Serialization should mask sensitive information
        config_dict = config.model_dump()
        assert config_dict["host"] == "localhost"
        assert config_dict["port"] == 5432
        assert config_dict["database"] == "test_db"

        # Password should be masked or excluded
        assert config_dict.get("password") != "sensitive_password"

    def test_database_config_connection_string_format(self):
        """Test different connection string formats."""
        # Test with different drivers
        drivers = [
            "postgresql+asyncpg",
            "postgresql+psycopg",
            "postgresql"
        ]

        for driver in drivers:
            config = DatabaseConfig(
                host="localhost",
                port=5432,
                username="test_user",
                password="test_password",
                database="test_db",
                driver=driver
            )

            assert config.driver == driver
            assert driver in config.database_url

    def test_database_config_validation_error_messages(self):
        """Test validation error messages are helpful."""
        try:
            DatabaseConfig(
                host="",  # Invalid empty host
                port=70000,  # Invalid port
                username="test_user",
                password="test_password",
                database="test_db"
            )
        except ValidationError as e:
            errors = e.errors()

            # Should have specific error messages
            error_fields = [error["loc"][0] for error in errors]
            assert "host" in error_fields
            assert "port" in error_fields

            # Error messages should be descriptive
            for error in errors:
                assert "msg" in error
                assert len(error["msg"]) > 0