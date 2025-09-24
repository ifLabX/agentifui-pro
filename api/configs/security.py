"""
Security validation for configuration management.

This module provides enhanced security validation that enforces stricter rules
in production environments while being more lenient in development.
"""

import re
from typing import Any


class SecurityValidator:
    """Security validation for environment-specific configuration rules."""

    @staticmethod
    def validate_environment(settings) -> dict[str, Any]:
        """
        Validate environment-specific security requirements.

        Args:
            settings: EnvironmentSettings instance

        Returns:
            Validation result with details
        """
        result = {
            "valid": True,
            "environment": settings.environment,
            "secret_key": {},
            "database": {},
            "cors": {},
            "production_requirements": {},
            "warnings": [],
            "recommendations": [],
        }

        # Validate secret key
        secret_key_result = validate_secret_key_strength(settings.secret_key.get_secret_value(), settings.environment)
        result["secret_key"] = secret_key_result
        if not secret_key_result["valid"]:
            result["valid"] = False

        # Validate database password if available
        if hasattr(settings.database, "password"):
            db_password_result = validate_password_strength(settings.database.password, settings.environment)
            result["database"] = db_password_result
            if not db_password_result["valid"]:
                result["valid"] = False

        # Validate CORS origins
        cors_result = validate_cors_origins(settings.cors_origins, settings.environment)
        result["cors"] = cors_result
        if not cors_result["valid"]:
            result["valid"] = False

        # Production-specific requirements
        if settings.environment == "production":
            prod_result = validate_production_requirements(settings)
            result["production_requirements"] = prod_result
            if not prod_result["met"]:
                result["valid"] = False

        # Collect warnings and recommendations
        for section in ["secret_key", "database", "cors"]:
            if section in result and "warnings" in result[section]:
                result["warnings"].extend(result[section]["warnings"])
            if section in result and "recommendations" in result[section]:
                result["recommendations"].extend(result[section]["recommendations"])

        return result

    @staticmethod
    def validate_environment_transition(from_env: str, to_env: str, settings) -> dict[str, Any]:
        """
        Validate environment transition requirements.

        Args:
            from_env: Source environment
            to_env: Target environment
            settings: EnvironmentSettings instance

        Returns:
            Transition validation result
        """
        result = {
            "valid": True,
            "from_environment": from_env,
            "to_environment": to_env,
            "warnings": [],
            "recommendations": [],
            "checklist": [],
        }

        # Direct dev to prod transition warning
        if from_env == "development" and to_env == "production":
            result["warnings"].append(
                "Direct transition from development to production detected. "
                "Consider using staging environment for validation."
            )

        # Environment-specific validation
        env_validation = SecurityValidator.validate_environment(settings)
        if not env_validation["valid"]:
            result["valid"] = False
            result["warnings"].extend(env_validation.get("warnings", []))

        # Transition checklist for production
        if to_env == "production":
            checklist = [
                "secret_key_updated" if env_validation["secret_key"].get("valid") else "secret_key_needs_update",
                (
                    "database_password_secured"
                    if env_validation["database"].get("valid")
                    else "database_password_needs_securing"
                ),
                "debug_disabled" if not settings.debug else "debug_needs_disabling",
                "https_enforced"
                if all(origin.startswith("https://") or "localhost" in origin for origin in settings.cors_origins)
                else "https_needs_enforcement",
                "logging_configured" if settings.log_level == "INFO" else "logging_needs_configuration",
            ]
            result["checklist"] = checklist

        return result


def validate_production_requirements(settings) -> dict[str, Any]:
    """
    Validate production-specific security requirements.

    Args:
        settings: EnvironmentSettings instance

    Returns:
        Production requirements validation result
    """
    result = {"met": True, "issues": []}

    # Debug must be disabled in production
    if settings.debug:
        result["met"] = False
        result["issues"].append("Debug mode must be disabled in production")

    # Secret key must be strong
    secret_key_result = validate_secret_key_strength(settings.secret_key.get_secret_value(), "production")
    if not secret_key_result["valid"]:
        result["met"] = False
        result["issues"].extend(secret_key_result["issues"])

    # CORS origins should use HTTPS
    for origin in settings.cors_origins:
        if origin.startswith("http://") and "localhost" not in origin and "127.0.0.1" not in origin:
            result["met"] = False
            result["issues"].append(f"HTTP origin not secure for production: {origin}")

    return result


def validate_secret_key_strength(key: str, environment: str) -> dict[str, Any]:
    """
    Validate secret key strength based on environment.

    Args:
        key: Secret key to validate
        environment: Target environment

    Returns:
        Secret key validation result
    """
    result = {"valid": True, "issues": [], "warnings": [], "recommendations": []}

    # Common weak keys
    weak_keys = [
        "your-secret-key-here-change-in-production",
        "dev-secure-string-for-development-only-change-in-production-32",
        "secret",
        "password",
        "changeme",
        "dev-secret",
        "test-secret",
    ]

    if environment == "production":
        # Production requires strong keys
        if key in weak_keys:
            result["valid"] = False
            result["issues"].append("Production requires secure secret key, not default values")

        if len(key) < 32:
            result["valid"] = False
            result["issues"].append("Production secret key must be at least 32 characters long")

        # Check for complexity
        if not _has_sufficient_complexity(key):
            result["recommendations"].append("Consider using a more complex secret key with mixed characters")

    elif environment == "staging":
        # Staging has moderate requirements
        if key in weak_keys:
            result["valid"] = False
            result["issues"].append("Staging should use secure secret key, not defaults")

        if len(key) < 16:
            result["valid"] = False
            result["issues"].append("Staging secret key should be at least 16 characters long")

    else:  # development
        # Development is lenient but gives warnings
        if key in weak_keys:
            result["warnings"].append("Using default secret key - acceptable for development only")

        if len(key) < 12:
            result["warnings"].append("Consider using a longer secret key even in development")

    return result


def validate_password_strength(password: str, environment: str) -> dict[str, Any]:
    """
    Validate database password strength based on environment.

    Args:
        password: Password to validate
        environment: Target environment

    Returns:
        Password validation result
    """
    result = {"valid": True, "issues": [], "warnings": [], "recommendations": []}

    if environment == "production":
        # Production requires strong passwords
        if len(password) < 12:
            result["valid"] = False
            result["issues"].append("Production database password must be at least 12 characters long")

        if not _has_sufficient_complexity(password):
            result["valid"] = False
            result["issues"].append("Production database password must have sufficient complexity")

        # Common weak passwords
        weak_passwords = ["password", "123", "admin", "root", "postgres", "test"]
        if password.lower() in weak_passwords:
            result["valid"] = False
            result["issues"].append("Production database password cannot be a common weak password")

    elif environment == "staging":
        # Staging has moderate requirements
        if len(password) < 8:
            result["valid"] = False
            result["issues"].append("Staging database password should be at least 8 characters long")

    else:  # development
        # Development is lenient
        if len(password) < 4:
            result["warnings"].append("Consider using a longer database password")

    return result


def validate_cors_origins(origins: list[str], environment: str) -> dict[str, Any]:
    """
    Validate CORS origins based on environment.

    Args:
        origins: List of CORS origins
        environment: Target environment

    Returns:
        CORS validation result
    """
    result = {"valid": True, "issues": [], "warnings": [], "recommendations": []}

    if environment == "production":
        # Production should use HTTPS
        for origin in origins:
            if origin.startswith("http://") and "localhost" not in origin:
                result["valid"] = False
                result["issues"].append(f"Production should use HTTPS origins: {origin}")

        # Should not allow wildcard origins in production
        if "*" in origins:
            result["valid"] = False
            result["issues"].append("Wildcard CORS origins not recommended for production")

    elif environment == "staging":
        # Staging recommendations
        for origin in origins:
            if origin.startswith("http://") and "localhost" not in origin:
                result["warnings"].append(f"Consider using HTTPS for staging origin: {origin}")

    return result


def _has_sufficient_complexity(text: str) -> bool:
    """Check if text has sufficient complexity (mixed character types)."""
    has_lower = bool(re.search(r"[a-z]", text))
    has_upper = bool(re.search(r"[A-Z]", text))
    has_digit = bool(re.search(r"\d", text))
    has_special = bool(re.search(r"[^a-zA-Z0-9]", text))

    # At least 3 of 4 character types for sufficient complexity
    complexity_score = sum([has_lower, has_upper, has_digit, has_special])
    return complexity_score >= 3
