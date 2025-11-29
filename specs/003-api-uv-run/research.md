# Research: FastAPI Best Practices for Test Suite Fixes

**Feature**: 003-api-uv-run
**Date**: 2025-10-02
**Sources**: Context7 (/tiangolo/fastapi), pytest documentation, Pydantic v2 migration guide

## Executive Summary

Research into fixing 28 failing pytest tests revealed six root causes requiring fixes aligned with FastAPI best practices:

1. Missing greenlet dependency (5 failures)
1. Pydantic v2 migration incomplete (26 deprecation warnings)
1. Incorrect test assertions accessing internal APIs (3 failures)
1. Wrong HTTP status codes for service unavailability (8 failures)
1. Enum validation not enforcing properly (1 failure)
1. Dead code present (unused environment variables)

All fixes follow official FastAPI documentation patterns from Context7.

______________________________________________________________________

## 1. FastAPI Settings Management

### Decision: Use @lru_cache for Settings Singleton

**Official Pattern** (from Context7 /tiangolo/fastapi):

```python
from functools import lru_cache
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Awesome API"
    admin_email: str
    items_per_user: int = 50

@lru_cache
def get_settings() -> Settings:
    return Settings()
```

**Rationale**:

- ✅ Official FastAPI recommendation for settings singleton
- ✅ Prevents re-reading .env file on every access
- ✅ Thread-safe and performant
- ✅ Compatible with dependency injection testing via `app.dependency_overrides`

**Current Implementation Status**: ✅ Already implemented correctly in `api/src/config/settings.py`

**Alternative Considered**: Direct instantiation (`settings = Settings()`)

- ❌ Rejected: Not compatible with test overrides
- ❌ Performance: Re-reads env files without caching

______________________________________________________________________

## 2. Pydantic v2 Migration

### Decision: Remove Deprecated `env` Parameter from Field()

**Problem**: Using deprecated Pydantic v1 patterns causing 26 warnings:

```python
# OLD (Pydantic v1 - DEPRECATED):
app_name: str = Field(default="API", env="APP_NAME")
```

**Solution**: Pydantic v2 BaseSettings automatically maps field names to environment variables:

```python
# NEW (Pydantic v2 - CORRECT):
app_name: str = Field(default="API")
# Automatically reads APP_NAME env var (uppercase field name)
```

**Breaking Changes Identified**:

1. **Field env parameter** → Remove entirely, use field name

1. **ConfigDict replaces Config class**:

   ```python
   # OLD:
   class Config:
       env_file = ".env"

   # NEW:
   model_config = ConfigDict(env_file=".env")
   ```

1. **Validator syntax** → Use `@field_validator` decorator (already correct)

**Migration Checklist** (for settings.py):

- [ ] Remove `env` parameter from all 26 Field declarations
- [ ] Verify field names match env variable names (case-insensitive match works)
- [ ] Test all validators still work with new syntax
- [ ] Confirm no deprecation warnings remain

**Reference**: Context7 snippets showing Pydantic v2 BaseSettings patterns

______________________________________________________________________

## 3. SQLAlchemy Async Engine Requirements

### Decision: Add greenlet>=3.0.0 as Explicit Dependency

**Root Cause**: SQLAlchemy async engine requires greenlet for async context management:

```
ValueError: the greenlet library is required to use this function. No module named 'greenlet'
```

**Current State**:

- ✅ greenlet 3.2.4 present in uv.lock (transitive dependency)
- ❌ NOT declared in pyproject.toml dependencies
- ❌ Causes 5 test failures in async engine disposal and connection tests

**Fix**:

```toml
# api/pyproject.toml
[project]
dependencies = [
    "fastapi>=0.100.0",
    "sqlalchemy>=2.0.0",
    "asyncpg>=0.28.0",
    "greenlet>=3.0.0",  # ADD THIS - required for SQLAlchemy async
    # ... other deps
]
```

**Rationale**:

- Explicit > implicit for critical runtime dependencies
- Prevents breakage if transitive dependency chain changes
- Makes requirement clear to all developers

**Validation**: After adding dependency:

```bash
uv sync
uv run python -c "import greenlet; print(greenlet.__version__)"
uv run pytest tests/test_database_connection.py -v
```

______________________________________________________________________

## 4. FastAPI Middleware Access Patterns

### Decision: Do Not Access `app.middleware_stack` (Internal API)

**Problem**: Tests failing with `AttributeError: 'NoneType' object has no attribute 'middleware'`

**Root Cause**: `middleware_stack` is internal FastAPI implementation detail, not public API

**Incorrect Pattern** (current tests):

```python
# WRONG - internal API:
assert len(app.middleware_stack.middleware) > 0
```

**Correct Patterns**:

**Option 1**: Test functionality, not internals:

```python
# Test that middleware works, not that it exists:
response = client.get("/")
assert "access-control-allow-origin" in response.headers  # CORS middleware working
```

**Option 2**: Use public `app.middleware` iterator:

```python
# Count middleware via public API:
middleware_count = len([m for m in app.middleware])
assert middleware_count > 0
```

**Affected Tests**:

- `test_startup.py::test_application_basic_configuration`
- `test_startup.py::test_middleware_stack_startup`
- `test_startup.py::test_dependency_injection_startup`

**Fix Strategy**: Replace internal access with functional tests

______________________________________________________________________

## 5. HTTP Status Codes for Service Unavailability

### Decision: Use 503 for Database Unavailability (Not 500)

**HTTP Status Code Semantics**:

- **500 Internal Server Error**: Server bug, code error, unhandled exception
- **503 Service Unavailable**: Temporary condition, service dependency down

**Problem**: Database health checks returning 500 instead of 503

**Correct Pattern**:

```python
# src/health/endpoints.py
@router.get("/health/db")
async def health_db():
    try:
        is_connected = await check_database_connection()
        if is_connected:
            return {"status": "healthy", "database": "connected"}
        else:
            return JSONResponse(
                status_code=503,  # Service Unavailable
                content={"status": "unhealthy", "database": "disconnected"}
            )
    except Exception as e:
        return JSONResponse(
            status_code=503,  # Service Unavailable (dependency down)
            content={"status": "error", "message": str(e)}
        )
```

**Rationale**:

- Database down is temporary, not a code bug
- Monitoring systems treat 503 differently (don't alert as code error)
- Load balancers can retry 503 requests

**Affected Tests** (expecting 503, getting 500):

- `test_health_db_endpoint.py::test_health_db_endpoint_handles_database_errors`
- `test_health_db_endpoint.py::test_health_db_endpoint_consistency`
- `test_performance.py::test_health_db_endpoint_*` (multiple)
- `test_quickstart_validation.py::test_quickstart_database_*` (multiple)

______________________________________________________________________

## 6. FastAPI Test Client Best Practices

### Decision: Use TestClient with Proper Lifecycle Management

**Official Pattern** (from Context7):

```python
from fastapi.testclient import TestClient

app = FastAPI()

@app.get("/")
async def read_main():
    return {"msg": "Hello World"}

# Preferred: Context manager for automatic cleanup
with TestClient(app) as client:
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}

# Alternative: Manual cleanup
client = TestClient(app)
try:
    response = client.get("/")
    assert response.status_code == 200
finally:
    client.__exit__(None, None, None)
```

**Key Insights**:

- TestClient provides synchronous interface to async endpoints
- Handles lifespan events (startup/shutdown) automatically
- Context manager ensures proper cleanup

**Current Usage**: Mostly correct, verify all tests use context manager

______________________________________________________________________

## 7. Dependency Injection Testing

### Decision: Use `app.dependency_overrides` for Test Mocks

**Official Pattern** (from Context7):

```python
from fastapi import FastAPI, Depends

app = FastAPI()

def get_settings():
    return Settings()

# In tests:
def test_with_mock_settings():
    def get_test_settings():
        return Settings(database_url="sqlite:///:memory:")

    app.dependency_overrides[get_settings] = get_test_settings

    with TestClient(app) as client:
        response = client.get("/info")
        # ... assertions

    # CRITICAL: Clean up after test
    app.dependency_overrides = {}
```

**Best Practices**:

- Override dependencies, don't modify code
- Always reset `app.dependency_overrides = {}` after each test
- Use fixtures for common overrides

**Current Status**: Check if any tests need this pattern for database mocking

______________________________________________________________________

## 8. Dead Code Identification

### Environment Variables Not Used in Code

**Candidates for Removal**:

1. **SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES**

   - Marked "for future use"
   - No authentication system implemented
   - Complex validation logic unused
   - **Decision**: Remove or move to separate auth feature spec

1. **USE_UUIDV7**

   - Feature flag with no corresponding code
   - No UUID generation using v7 found
   - **Decision**: Remove entirely

**Keep (Active Use)**:

- DATABASE_URL, APP_NAME, APP_VERSION (used in main.py, settings.py)
- CORS\_\* (used in middleware configuration)
- LOG_LEVEL, LOG_FORMAT (used in logging config)
- HEALTH_CHECK_TIMEOUT (used in health endpoints)

**Cleanup Impact**:

- Reduces .env.example from 51 lines to ~35 lines
- Simplifies Settings model by ~15 fields
- Removes unused validation logic

______________________________________________________________________

## 9. Pydantic Enum Validation

### Decision: Ensure Proper Enum Validation in v2

**Problem**: `test_error_schemas.py::test_error_enum_validation` not raising ValidationError

**Check**: Verify error models use proper Pydantic v2 enum patterns:

```python
from enum import Enum
from pydantic import BaseModel

class ErrorType(str, Enum):
    VALIDATION_ERROR = "validation_error"
    NOT_FOUND = "not_found"
    INTERNAL_ERROR = "internal_error"

class ErrorResponse(BaseModel):
    error_type: ErrorType  # Should validate enum values
    message: str
```

**Test Should Validate**:

```python
with pytest.raises(ValidationError):
    ErrorResponse(error_type="invalid_value", message="test")
```

**Fix Strategy**: Review models/errors.py for proper enum validation

______________________________________________________________________

## 10. Test Isolation and Cleanup

### Best Practices for Test Reliability

1. **Database Cleanup**: Use transactions that rollback
1. **Dependency Overrides**: Reset after each test
1. **Engine Disposal**: Properly clean up async engines
1. **Fixture Scope**: Use `scope="function"` for isolation

**Pattern**:

```python
import pytest
from fastapi.testclient import TestClient

@pytest.fixture(scope="function")
def client():
    """Isolated test client per test function"""
    with TestClient(app) as c:
        yield c
    # Automatic cleanup via context manager
    app.dependency_overrides = {}  # Reset overrides
```

______________________________________________________________________

## Summary of Decisions

| Area | Decision | Impact |
|------|----------|--------|
| Settings | Keep @lru_cache pattern | ✅ No change needed |
| Pydantic | Remove env param from Fields | 🔧 Fix 26 warnings |
| Dependencies | Add greenlet explicitly | 🔧 Fix 5 test failures |
| Middleware Tests | Use functional tests | 🔧 Fix 3 test failures |
| HTTP Status | Use 503 for DB down | 🔧 Fix 8 test failures |
| Dead Code | Remove unused env vars | 🧹 Cleanup |
| Enum Validation | Verify Pydantic v2 patterns | 🔧 Fix 1 test failure |
| Test Patterns | Use dependency_overrides | ✅ Best practice |

**Total Test Fixes**: 28 failures across 6 categories
**Deprecation Warnings**: 26 (all from Pydantic v2 migration)
**Code Quality**: Significant improvement through dead code removal

______________________________________________________________________

**Next Phase**: Design data models and contracts (Phase 1)
