"""
Test environment variable parsing with comma-separated vs JSON array formats.

Tests the enhanced parsing logic that prioritizes comma-separated values
for DevOps compatibility while maintaining backward compatibility with JSON arrays.
"""

from tests.conftest import mock_environment_variables

# These imports will fail until the implementation is complete
try:
    from configs.parsing import (
        detect_list_format,
        parse_boolean_from_env,
        parse_comma_separated_list,
        parse_cors_origins,
    )
except ImportError:
    # Mock the functions for contract testing
    def parse_comma_separated_list(value):
        return []

    def parse_boolean_from_env(value):
        return False

    def parse_cors_origins(value):
        return []

    def detect_list_format(value):
        return "unknown"


class TestEnvironmentVariableParsing:
    """Test environment variable parsing functions and format detection."""

    def test_parse_comma_separated_list(self):
        """Test parsing comma-separated values (preferred format)."""
        # This test will FAIL until parsing functions are implemented

        # Simple comma-separated list
        result = parse_comma_separated_list("value1,value2,value3")
        expected = ["value1", "value2", "value3"]
        assert result == expected

        # List with spaces (should be trimmed)
        result = parse_comma_separated_list("value1, value2 , value3")
        expected = ["value1", "value2", "value3"]
        assert result == expected

        # Single value (no commas)
        result = parse_comma_separated_list("single_value")
        expected = ["single_value"]
        assert result == expected

        # Empty string
        result = parse_comma_separated_list("")
        expected = []
        assert result == expected

    def test_parse_cors_origins_comma_separated(self):
        """Test CORS origins parsing with comma-separated format."""
        origins_string = "http://localhost:3000,http://localhost:3001,https://app.example.com"

        result = parse_cors_origins(origins_string)
        expected = ["http://localhost:3000", "http://localhost:3001", "https://app.example.com"]
        assert result == expected

    def test_parse_cors_origins_json_array_backward_compatibility(self):
        """Test CORS origins parsing with JSON array format (backward compatibility)."""
        origins_json = '["http://localhost:3000", "http://localhost:3001", "https://app.example.com"]'

        result = parse_cors_origins(origins_json)
        expected = ["http://localhost:3000", "http://localhost:3001", "https://app.example.com"]
        assert result == expected

    def test_parse_cors_origins_mixed_format_handling(self):
        """Test handling of mixed or malformed formats."""
        # Malformed JSON should fall back to comma-separated parsing
        malformed_json = '["http://localhost:3000", "incomplete'
        result = parse_cors_origins(malformed_json)

        # Should treat as single value since it's not valid JSON or comma-separated
        assert isinstance(result, list)
        assert len(result) >= 1

        # Empty array JSON
        empty_json = "[]"
        result = parse_cors_origins(empty_json)
        assert result == []

        # Single item JSON array
        single_json = '["http://localhost:3000"]'
        result = parse_cors_origins(single_json)
        assert result == ["http://localhost:3000"]

    def test_detect_list_format(self):
        """Test format detection for list values."""
        # Comma-separated format
        result = detect_list_format("value1,value2,value3")
        assert result == "comma_separated"

        # JSON array format
        result = detect_list_format('["value1", "value2", "value3"]')
        assert result == "json_array"

        # Single value (no format markers)
        result = detect_list_format("single_value")
        assert result == "single_value"

        # Empty string
        result = detect_list_format("")
        assert result == "empty"

        # Mixed format (JSON-like but with issues)
        result = detect_list_format('["value1", "value2",')
        assert result == "malformed_json"

    def test_parse_boolean_from_env(self):
        """Test boolean parsing from environment variables."""
        # True values
        true_values = ["true", "True", "TRUE", "1", "yes", "Yes", "YES", "on", "ON"]
        for value in true_values:
            result = parse_boolean_from_env(value)
            assert result is True, f"Failed for value: {value}"

        # False values
        false_values = ["false", "False", "FALSE", "0", "no", "No", "NO", "off", "OFF", ""]
        for value in false_values:
            result = parse_boolean_from_env(value)
            assert result is False, f"Failed for value: {value}"

    def test_environment_variable_parsing_integration(self):
        """Test integration of parsing with actual environment variables."""
        config = {
            "CORS_ORIGINS": "http://localhost:3000,http://localhost:3001",
            "FEATURE_FLAGS": "auth_v2,enhanced_logging,rate_limiting",
            "DEBUG": "true",
            "ENABLE_METRICS": "1",
        }

        with mock_environment_variables(config):
            # Test CORS origins parsing
            cors_result = parse_cors_origins(config["CORS_ORIGINS"])
            assert cors_result == ["http://localhost:3000", "http://localhost:3001"]

            # Test feature flags parsing
            flags_result = parse_comma_separated_list(config["FEATURE_FLAGS"])
            assert flags_result == ["auth_v2", "enhanced_logging", "rate_limiting"]

            # Test boolean parsing
            debug_result = parse_boolean_from_env(config["DEBUG"])
            assert debug_result is True

            metrics_result = parse_boolean_from_env(config["ENABLE_METRICS"])
            assert metrics_result is True

    def test_cors_origins_validation(self):
        """Test validation of CORS origins after parsing."""
        # Valid origins
        valid_origins = "http://localhost:3000,https://app.example.com"
        result = parse_cors_origins(valid_origins)

        # Should parse successfully
        assert len(result) == 2
        assert all(origin.startswith(("http://", "https://")) for origin in result)

        # Invalid origins (for production)
        invalid_origins = "localhost:3000,example.com"  # Missing protocol
        result = parse_cors_origins(invalid_origins)

        # Should still parse but may need validation at higher level
        assert len(result) == 2

    def test_special_characters_in_lists(self):
        """Test handling of special characters in list values."""
        # URLs with query parameters
        urls = "http://localhost:3000?debug=true,https://app.example.com/admin?auth=1"
        result = parse_comma_separated_list(urls)

        assert len(result) == 2
        assert "debug=true" in result[0]
        assert "auth=1" in result[1]

        # Values with spaces and special characters
        complex_values = "value-1,value_2,value with spaces,value@domain.com"
        result = parse_comma_separated_list(complex_values)

        assert len(result) == 4
        assert "value with spaces" in result
        assert "value@domain.com" in result

    def test_empty_and_whitespace_handling(self):
        """Test handling of empty values and whitespace."""
        # Empty values in list
        with_empties = "value1,,value2,  ,value3"
        result = parse_comma_separated_list(with_empties)

        # Should filter out empty values
        expected = ["value1", "value2", "value3"]
        assert result == expected

        # Only whitespace
        whitespace_only = "   ,  ,    "
        result = parse_comma_separated_list(whitespace_only)
        assert result == []

    def test_large_list_parsing_performance(self):
        """Test performance with large comma-separated lists."""
        # Generate large list
        large_list = ",".join([f"value{i}" for i in range(1000)])

        result = parse_comma_separated_list(large_list)

        assert len(result) == 1000
        assert result[0] == "value0"
        assert result[-1] == "value999"

    def test_json_array_edge_cases(self):
        """Test edge cases for JSON array parsing."""
        # Nested arrays (should not be supported)
        nested_json = '[["inner1", "inner2"], "outer"]'
        result = parse_cors_origins(nested_json)

        # Should handle gracefully (may flatten or reject)
        assert isinstance(result, list)

        # Mixed types in JSON array
        mixed_json = '["string", 123, true]'
        result = parse_cors_origins(mixed_json)

        # Should convert all to strings or handle appropriately
        assert isinstance(result, list)

        # JSON with extra whitespace
        spaced_json = ' [ "value1" , "value2" ] '
        result = parse_cors_origins(spaced_json)
        assert result == ["value1", "value2"]

    def test_migration_warning_detection(self):
        """Test detection of configurations that should trigger migration warnings."""
        # JSON array format should suggest migration to comma-separated
        json_format = '["http://localhost:3000", "http://localhost:3001"]'
        format_type = detect_list_format(json_format)

        assert format_type == "json_array"

        # This would trigger a migration warning in the main application
        # to suggest using comma-separated format instead

    def test_environment_specific_parsing_requirements(self):
        """Test environment-specific parsing requirements."""
        # Development environment - more lenient
        dev_config = {
            "ENVIRONMENT": "development",
            "CORS_ORIGINS": "http://localhost:3000,http://127.0.0.1:3001",  # HTTP allowed in dev
        }

        with mock_environment_variables(dev_config):
            result = parse_cors_origins(dev_config["CORS_ORIGINS"])
            assert len(result) == 2
            assert all("http://" in origin for origin in result)

        # Production environment - stricter requirements would be enforced at higher level
        prod_config = {
            "ENVIRONMENT": "production",
            "CORS_ORIGINS": "https://app.example.com,https://admin.example.com",  # HTTPS required
        }

        with mock_environment_variables(prod_config):
            result = parse_cors_origins(prod_config["CORS_ORIGINS"])
            assert len(result) == 2
            assert all(origin.startswith("https://") for origin in result)
