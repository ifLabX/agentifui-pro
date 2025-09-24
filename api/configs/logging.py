"""
Structured logging configuration for FastAPI application.

This module provides comprehensive logging setup with structured output,
multiple handlers, and environment-specific configuration.
"""

import json
import logging
import logging.config
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

from configs.settings import get_settings


class JSONFormatter(logging.Formatter):
    """
    Custom JSON formatter for structured logging.

    Formats log records as JSON objects with consistent structure
    and additional metadata for monitoring and analysis.
    """

    def __init__(self, *args, **kwargs):
        """Initialize JSON formatter."""
        super().__init__(*args, **kwargs)
        self.hostname = self._get_hostname()

    def _get_hostname(self) -> str:
        """Get hostname for log metadata."""
        try:
            import socket

            return socket.gethostname()
        except Exception:
            return "unknown"

    def format(self, record: logging.LogRecord) -> str:
        """
        Format log record as JSON.

        Args:
            record: Log record to format

        Returns:
            JSON-formatted log string
        """
        # Base log entry structure
        log_entry = {
            "timestamp": datetime.utcfromtimestamp(record.created).isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
            "hostname": self.hostname,
            "process": record.process,
            "thread": record.thread,
        }

        # Add exception information if present
        if record.exc_info:
            log_entry["exception"] = {
                "type": record.exc_info[0].__name__ if record.exc_info[0] else None,
                "message": str(record.exc_info[1]) if record.exc_info[1] else None,
                "traceback": self.formatException(record.exc_info) if record.exc_info else None,
            }

        # Add extra fields from record
        extra_fields = {}
        for key, value in record.__dict__.items():
            if key not in {
                "name",
                "msg",
                "args",
                "levelname",
                "levelno",
                "pathname",
                "filename",
                "module",
                "exc_info",
                "exc_text",
                "stack_info",
                "lineno",
                "funcName",
                "created",
                "msecs",
                "relativeCreated",
                "thread",
                "threadName",
                "processName",
                "process",
                "message",
                "asctime",
            }:
                extra_fields[key] = value

        if extra_fields:
            log_entry["extra"] = extra_fields

        return json.dumps(log_entry, default=str, ensure_ascii=False)


class HealthCheckFilter(logging.Filter):
    """
    Filter to reduce noise from health check endpoints.

    Filters out health check requests in production to reduce log volume
    while maintaining them in development for debugging.
    """

    def __init__(self, name: str = "", filter_health_checks: bool = True):
        """
        Initialize health check filter.

        Args:
            name: Filter name
            filter_health_checks: Whether to filter out health check logs
        """
        super().__init__(name)
        self.filter_health_checks = filter_health_checks

    def filter(self, record: logging.LogRecord) -> bool:
        """
        Filter log records.

        Args:
            record: Log record to evaluate

        Returns:
            True if record should be logged, False otherwise
        """
        if not self.filter_health_checks:
            return True

        # Filter out health check endpoint requests
        message = record.getMessage().lower()
        health_patterns = ["get /health", "get /health/db", "health endpoint", "health check"]

        return not any(pattern in message for pattern in health_patterns)


def setup_logging(
    log_level: Optional[str] = None,
    log_format: Optional[str] = None,
    enable_json: bool = False,
    log_file: Optional[str] = None,
    filter_health_checks: bool = True,
) -> None:
    """
    Configure application logging.

    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_format: Log format string (ignored if enable_json is True)
        enable_json: Whether to use JSON formatting
        log_file: Optional log file path
        filter_health_checks: Whether to filter health check logs
    """
    settings = get_settings()

    # Use settings values as defaults
    log_level = log_level or settings.log_level
    log_format = log_format or settings.log_format

    # Determine if we should use JSON formatting
    if enable_json or settings.environment == "production":
        enable_json = True

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level.upper()))

    # Clear existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, log_level.upper()))

    if enable_json:
        console_handler.setFormatter(JSONFormatter())
    else:
        console_handler.setFormatter(logging.Formatter(log_format))

    # Add health check filter if enabled
    if filter_health_checks and settings.environment == "production":
        console_handler.addFilter(HealthCheckFilter(filter_health_checks=True))

    root_logger.addHandler(console_handler)

    # File handler (optional)
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(getattr(logging, log_level.upper()))

        if enable_json:
            file_handler.setFormatter(JSONFormatter())
        else:
            file_handler.setFormatter(logging.Formatter(log_format))

        root_logger.addHandler(file_handler)

    # Configure specific loggers
    configure_framework_loggers(log_level)

    # Log startup message
    logger = logging.getLogger(__name__)
    logger.info(
        "Logging configured",
        extra={
            "log_level": log_level,
            "json_format": enable_json,
            "environment": settings.environment,
            "filter_health_checks": filter_health_checks,
        },
    )


def configure_framework_loggers(log_level: str) -> None:
    """
    Configure logging for third-party frameworks.

    Args:
        log_level: Base logging level
    """
    # SQLAlchemy logging
    sqlalchemy_level = "INFO" if log_level == "DEBUG" else "WARNING"
    logging.getLogger("sqlalchemy.engine").setLevel(getattr(logging, sqlalchemy_level))
    logging.getLogger("sqlalchemy.pool").setLevel(getattr(logging, sqlalchemy_level))
    logging.getLogger("sqlalchemy.dialects").setLevel(logging.WARNING)

    # Alembic logging
    logging.getLogger("alembic").setLevel(logging.INFO)

    # FastAPI/Uvicorn logging
    logging.getLogger("uvicorn.access").setLevel(logging.INFO)
    logging.getLogger("uvicorn.error").setLevel(logging.INFO)
    logging.getLogger("fastapi").setLevel(logging.INFO)

    # Reduce noise from HTTP clients
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)


def get_logging_config() -> dict[str, Any]:
    """
    Get logging configuration dictionary.

    Returns:
        Logging configuration dict compatible with logging.config.dictConfig
    """
    settings = get_settings()
    enable_json = settings.environment == "production"

    config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": settings.log_format,
            },
            "json": {
                "()": JSONFormatter,
            },
        },
        "filters": {
            "health_check": {
                "()": HealthCheckFilter,
                "filter_health_checks": settings.environment == "production",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": settings.log_level,
                "formatter": "json" if enable_json else "default",
                "filters": ["health_check"] if settings.environment == "production" else [],
                "stream": "ext://sys.stdout",
            },
        },
        "loggers": {
            "": {  # Root logger
                "level": settings.log_level,
                "handlers": ["console"],
            },
            "sqlalchemy.engine": {
                "level": "INFO" if settings.log_level == "DEBUG" else "WARNING",
                "handlers": ["console"],
                "propagate": False,
            },
            "sqlalchemy.pool": {
                "level": "INFO" if settings.log_level == "DEBUG" else "WARNING",
                "handlers": ["console"],
                "propagate": False,
            },
            "uvicorn.access": {
                "level": "INFO",
                "handlers": ["console"],
                "propagate": False,
            },
        },
    }

    return config


def configure_logging_from_dict() -> None:
    """Configure logging using dictionary configuration."""
    config = get_logging_config()
    logging.config.dictConfig(config)


# Context manager for temporary log level changes
class LogLevelContext:
    """
    Context manager for temporarily changing log levels.

    Useful for debugging specific operations or reducing noise
    during testing.
    """

    def __init__(self, logger_name: str, level: str):
        """
        Initialize log level context.

        Args:
            logger_name: Name of logger to modify
            level: Temporary log level
        """
        self.logger = logging.getLogger(logger_name)
        self.original_level = self.logger.level
        self.new_level = getattr(logging, level.upper())

    def __enter__(self):
        """Enter context and set new log level."""
        self.logger.setLevel(self.new_level)
        return self.logger

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context and restore original log level."""
        self.logger.setLevel(self.original_level)


# Utility function for adding structured data to log records
def log_with_context(logger: logging.Logger, level: str, message: str, **context) -> None:
    """
    Log message with additional context data.

    Args:
        logger: Logger instance
        level: Log level (debug, info, warning, error, critical)
        message: Log message
        **context: Additional context data to include in log
    """
    log_method = getattr(logger, level.lower())
    log_method(message, extra=context)
