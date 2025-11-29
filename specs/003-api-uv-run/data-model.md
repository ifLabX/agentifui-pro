# Data Models: API Configuration and Error Handling

**Feature**: 003-api-uv-run
**Date**: 2025-10-02
**Purpose**: Document existing data models requiring fixes for Pydantic v2 migration

## Overview

This refactoring task does not introduce new data models. It fixes existing models to comply with Pydantic v2 best practices and FastAPI recommendations.

______________________________________________________________________

## 1. Settings Model (Configuration)

**File**: `api/src/config/settings.py`
**Purpose**: Application configuration loaded from environment variables
**Framework**: Pydantic BaseSettings

### Current Structure (Needs Migration)

```python
from pydantic import Field, field_validator, ConfigDict
from pydantic.types import SecretStr
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Application Settings
    app_name: str = Field(default="Agentifui Pro API", env="APP_NAME")  # ❌ Remove env
    app_version: str = Field(default="0.1.0", env="APP_VERSION")  # ❌ Remove env
    app_description: str = Field(default="Backend API", env="APP_DESCRIPTION")  # ❌ Remove env
    debug: bool = Field(default=False, env="DEBUG")  # ❌ Remove env

    # Database Configuration
    database_url: str = Field(..., env="DATABASE_URL")  # ❌ Remove env
    database_pool_size: int = Field(default=10, env="DATABASE_POOL_SIZE", gt=0, le=100)  # ❌ Remove env
    # ... 20+ more fields with deprecated env parameter

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        frozen=True,
        extra="ignore",
    )
```

### Fixed Structure (Pydantic v2 Compliant)

```python
from pydantic import Field, field_validator, ConfigDict
from pydantic.types import SecretStr
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Application Settings
    app_name: str = Field(default="Agentifui Pro API")  # ✅ Automatic APP_NAME mapping
    app_version: str = Field(default="0.1.0")  # ✅ Automatic APP_VERSION mapping
    app_description: str = Field(default="Backend API")
    debug: bool = Field(default=False)

    # Database Configuration
    database_url: str = Field(...)  # ✅ Required, automatic DATABASE_URL mapping
    database_pool_size: int = Field(default=10, gt=0, le=100)
    database_pool_max_overflow: int = Field(default=20, ge=0, le=100)
    database_pool_timeout: int = Field(default=30, gt=0, le=300)
    database_pool_recycle: int = Field(default=3600, gt=0)

    # Health Check Configuration
    health_check_timeout: int = Field(default=5, gt=0, le=30)
    database_health_check_timeout: int = Field(default=10, gt=0, le=60)

    # Logging Configuration
    log_level: str = Field(default="INFO")
    log_format: str = Field(default="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    # CORS Settings
    cors_origins: list[str] = Field(default=["http://localhost:3000"])
    cors_allow_credentials: bool = Field(default=True)
    cors_allow_methods: list[str] = Field(default=["*"])
    cors_allow_headers: list[str] = Field(default=["*"])

    # Environment
    environment: str = Field(default="development")

    # Feature Flags
    enable_docs: bool = Field(default=True)
    enable_redoc: bool = Field(default=True)

    # Validators (keep existing, already Pydantic v2 compliant)
    @field_validator("database_url")
    @classmethod
    def validate_database_url(cls, v):
        if not v.startswith(("postgresql://", "postgresql+asyncpg://")):
            raise ValueError("Database URL must be a PostgreSQL connection string")
        return v

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v):
        allowed_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in allowed_levels:
            raise ValueError(f"Log level must be one of: {allowed_levels}")
        return v.upper()

    @field_validator("environment")
    @classmethod
    def validate_environment(cls, v):
        allowed_envs = ["development", "staging", "production"]
        if v.lower() not in allowed_envs:
            raise ValueError(f"Environment must be one of: {allowed_envs}")
        return v.lower()

    # CORS validators (keep existing list parsing logic)
    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            import json
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return [origin.strip() for origin in v.split(",")]
        return v

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        frozen=True,
        extra="ignore",
    )
```

### Fields to Remove (Dead Code)

**Unused Security Settings** (no auth system implemented):

```python
# REMOVE THESE:
secret_key: SecretStr = Field(default="...", env="SECRET_KEY")
algorithm: str = Field(default="HS256", env="ALGORITHM")
access_token_expire_minutes: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
```

**Unused Feature Flags**:

```python
# REMOVE THIS:
use_uuidv7: bool = Field(default=False, env="USE_UUIDV7")  # No implementation
```

### Environment Variable Mapping

Pydantic v2 BaseSettings automatically maps:

- `app_name` field → `APP_NAME` environment variable (case-insensitive)
- `database_url` field → `DATABASE_URL` environment variable
- `cors_origins` field → `CORS_ORIGINS` environment variable

No explicit `env` parameter needed!

______________________________________________________________________

## 2. Error Models

**File**: `api/src/models/errors.py`
**Purpose**: Standardized error response schemas
**Status**: Review enum validation

### Error Response Model

```python
from enum import Enum
from pydantic import BaseModel, Field
from datetime import datetime

class ErrorType(str, Enum):
    """Error type enumeration"""
    VALIDATION_ERROR = "validation_error"
    NOT_FOUND = "not_found"
    INTERNAL_ERROR = "internal_error"
    SERVICE_UNAVAILABLE = "service_unavailable"

class ErrorResponse(BaseModel):
    """Standard error response"""
    error_type: ErrorType  # Should enforce enum validation
    message: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    request_id: str | None = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "error_type": "validation_error",
                "message": "Invalid input data",
                "timestamp": "2025-10-02T12:00:00Z",
                "request_id": "req_123"
            }
        }
    )
```

**Validation Test** (should enforce enum):

```python
# This should raise ValidationError:
ErrorResponse(error_type="invalid_type", message="test")
```

**Fix Required**: Verify enum validation works in Pydantic v2

______________________________________________________________________

## 3. Health Models

**File**: `api/src/health/models.py`
**Purpose**: Health check response schemas
**Status**: Verify, likely correct

### Health Response Model

```python
from pydantic import BaseModel, Field

class HealthResponse(BaseModel):
    """Basic health check response"""
    status: str = Field(..., description="Health status: healthy or unhealthy")
    uptime: float = Field(..., description="Application uptime in seconds")
    timestamp: str = Field(..., description="Current timestamp")

class DatabaseHealthResponse(BaseModel):
    """Database health check response"""
    status: str  # "healthy" or "unhealthy"
    database: str  # "connected" or "disconnected"
    connection_pool: dict | None = None
    response_time_ms: float | None = None
    migration_status: str | None = None
```

**No Changes Required**: Models are already Pydantic v2 compliant

______________________________________________________________________

## 4. Database Models (Future)

**File**: `api/src/models/base.py`
**Purpose**: SQLAlchemy base model
**Status**: Verify UUID configuration

Currently uses standard UUIDs. `USE_UUIDV7` flag exists but unused.

**Decision**: Remove USE_UUIDV7 flag and related code (dead feature)

______________________________________________________________________

## Migration Checklist

### Settings Model (settings.py)

- [ ] Remove `env` parameter from all Field declarations (26 fields)
- [ ] Remove unused security fields (SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES)
- [ ] Remove unused feature flag (USE_UUIDV7)
- [ ] Verify all validators still work
- [ ] Test environment variable loading
- [ ] Confirm no deprecation warnings

### Error Models (errors.py)

- [ ] Verify ErrorType enum validation works
- [ ] Test ValidationError is raised for invalid enum values
- [ ] Ensure Pydantic v2 compatibility

### Health Models (models.py)

- [ ] Verify no changes needed
- [ ] Confirm compatibility with updated endpoints

### Environment Files

- [ ] Update .env.example to remove unused variables
- [ ] Document removed variables in README.md
- [ ] Verify all remaining variables are used in code

______________________________________________________________________

## Validation Strategy

After migration:

```bash
# 1. Verify no deprecation warnings
uv run pytest -W error::DeprecationWarning

# 2. Test settings loading
uv run python -c "from config.settings import get_settings; s = get_settings(); print(s.app_name)"

# 3. Test enum validation
uv run pytest tests/test_error_schemas.py::test_error_enum_validation -v

# 4. Run full test suite
uv run pytest -v
```

**Success Criteria**:

- ✅ 0 deprecation warnings
- ✅ All 109 tests pass
- ✅ Settings load correctly from environment
- ✅ Enum validation enforces type safety

______________________________________________________________________

**Next**: Create quickstart.md for test verification guide
