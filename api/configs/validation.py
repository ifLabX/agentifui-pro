"""
Configuration validation utilities.

This module provides comprehensive configuration validation with detailed
error messages and recovery suggestions.
"""

from typing import Any

from .security import SecurityValidator


class ConfigurationValidator:
    """Comprehensive configuration validation."""

    @staticmethod
    def validate_configuration(settings) -> dict[str, Any]:
        """
        Validate complete configuration with detailed error reporting.

        Args:
            settings: EnvironmentSettings instance

        Returns:
            Comprehensive validation result
        """
        result = {"valid": True, "errors": [], "warnings": [], "recommendations": []}

        # Security validation
        security_result = SecurityValidator.validate_environment(settings)
        if not security_result["valid"]:
            result["valid"] = False

        # Merge security results
        for section_name, section_result in security_result.items():
            if isinstance(section_result, dict) and "issues" in section_result:
                for issue in section_result["issues"]:
                    result["errors"].append(
                        {
                            "field": section_name,
                            "message": issue,
                            "suggestion": _get_suggestion_for_field(section_name, issue),
                        }
                    )

        # Add warnings and recommendations
        result["warnings"].extend(security_result.get("warnings", []))
        result["recommendations"].extend(security_result.get("recommendations", []))

        return result


def _get_suggestion_for_field(field: str, issue: str) -> str:
    """Get actionable suggestion for a specific field issue."""
    suggestions = {
        "secret_key": {
            "length": "Generate a secret key with at least 32 characters using: openssl rand -base64 32",
            "default": "Replace with a randomly generated secret key for security",
            "complexity": "Use a mix of letters, numbers, and special characters",
        },
        "database": {
            "password": "Use a strong password with at least 12 characters, mixed case, numbers and symbols",
            "length": "Increase password length to meet security requirements",
            "weak": "Avoid common passwords like 'password', 'admin', or '123'",
        },
        "cors": {
            "https": "Use HTTPS origins in production: https://yourdomain.com instead of http://",
            "wildcard": "Specify exact origins instead of wildcards for better security",
        },
    }

    # Match issue to suggestion
    field_suggestions = suggestions.get(field, {})

    for key, suggestion in field_suggestions.items():
        if key.lower() in issue.lower():
            return suggestion

    # Default suggestion
    return f"Review and update {field} configuration according to security best practices"
