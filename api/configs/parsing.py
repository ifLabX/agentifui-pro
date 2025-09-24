"""
Environment variable parsing utilities.

This module provides enhanced parsing logic that prioritizes comma-separated values
for DevOps compatibility while maintaining backward compatibility with JSON arrays.
"""

import json


def parse_comma_separated_list(value: str) -> list[str]:
    """
    Parse comma-separated values (preferred format).

    Args:
        value: Comma-separated string like "value1,value2,value3"

    Returns:
        List of parsed and trimmed values
    """
    if not value:
        return []

    # Split by comma and trim whitespace, filter empty values
    return [item.strip() for item in value.split(",") if item.strip()]


def parse_boolean_from_env(value: str) -> bool:
    """
    Parse boolean from environment variable string.

    Supports various truthy/falsy representations for maximum compatibility.

    Args:
        value: String representation of boolean

    Returns:
        Boolean value
    """
    if not value:
        return False

    value_lower = value.lower().strip()
    true_values = {"true", "1", "yes", "on", "y", "t"}
    return value_lower in true_values


def parse_cors_origins(value: str) -> list[str]:
    """
    Parse CORS origins with comma-separated preference and JSON array fallback.

    Args:
        value: CORS origins as comma-separated or JSON array string

    Returns:
        List of parsed CORS origins
    """
    if not value:
        return []

    # First try JSON array format (backward compatibility)
    try:
        parsed = json.loads(value)
        if isinstance(parsed, list):
            return [origin.strip() for origin in parsed if origin.strip()]
    except json.JSONDecodeError:
        pass

    # Fall back to comma-separated format (preferred)
    return parse_comma_separated_list(value)


def detect_list_format(value: str) -> str:
    """
    Detect the format of a list value string.

    Args:
        value: String to analyze

    Returns:
        Format type: "comma_separated", "json_array", "single_value", "empty", or "malformed_json"
    """
    if not value:
        return "empty"

    value = value.strip()

    # Check for JSON array format
    if value.startswith("[") and value.endswith("]"):
        try:
            parsed = json.loads(value)
            if isinstance(parsed, list):
                return "json_array"
        except json.JSONDecodeError:
            return "malformed_json"

    # Check for comma-separated format
    if "," in value:
        return "comma_separated"

    # Single value (no format markers)
    return "single_value"