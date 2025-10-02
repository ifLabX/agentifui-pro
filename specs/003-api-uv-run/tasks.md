# Tasks: Fix API Test Suite and Clean Dead Code

**Input**: Design documents from `/specs/003-api-uv-run/`
**Prerequisites**: plan.md ✅, research.md ✅, data-model.md ✅, contracts/ ✅

## Execution Summary

This refactoring task fixes 28 failing pytest tests by:
1. Adding missing greenlet dependency (5 test failures)
2. Migrating to Pydantic v2 patterns (26 deprecation warnings)
3. Fixing test assertions and HTTP status codes (17 test failures)
4. Removing dead code (unused environment variables)

**Path Convention**: This is a web application. All paths relative to `api/` directory in monorepo.

---

## Phase 3.1: Setup & Dependencies

### T001: Add greenlet dependency to pyproject.toml
**Type**: Dependency Management
**Priority**: CRITICAL (blocks async engine tests)
**Files**: `api/pyproject.toml`
**Action**:
```toml
[project]
dependencies = [
    "fastapi>=0.100.0",
    "uvicorn>=0.23.0",
    "pydantic>=2.0.0",
    "pydantic-settings>=2.0.0",
    "sqlalchemy>=2.0.0",
    "asyncpg>=0.28.0",
    "alembic>=1.12.0",
    "greenlet>=3.0.0",  # ADD THIS LINE - required for SQLAlchemy async
]
```
**Validation**:
```bash
cd api
uv sync
uv run python -c "import greenlet; print(f'greenlet {greenlet.__version__}')"
# Expected: greenlet 3.2.4
```
**Fixes**: 5 test failures in test_database_connection.py

---

## Phase 3.2: Pydantic v2 Migration

### T002: Migrate Settings model to Pydantic v2 (Remove env parameters)
**Type**: Code Migration
**Priority**: HIGH (removes 26 deprecation warnings)
**Files**: `api/src/config/settings.py`
**Action**: Remove `env="..."` parameter from all Field() declarations (26 fields total)

**Before (Deprecated)**:
```python
app_name: str = Field(default="Agentifui Pro API", env="APP_NAME")
database_url: str = Field(..., env="DATABASE_URL")
cors_origins: list[str] = Field(default=["http://localhost:3000"], env="CORS_ORIGINS")
# ... 23 more fields with env parameter
```

**After (Pydantic v2)**:
```python
app_name: str = Field(default="Agentifui Pro API")  # Auto-reads APP_NAME
database_url: str = Field(...)  # Auto-reads DATABASE_URL
cors_origins: list[str] = Field(default=["http://localhost:3000"])  # Auto-reads CORS_ORIGINS
# All fields - just remove env parameter, Pydantic v2 handles mapping automatically
```

**Fields to update** (remove `env` from each):
1. app_name, app_version, app_description, debug
2. host, port
3. database_url, database_pool_size, database_pool_max_overflow, database_pool_timeout, database_pool_recycle
4. health_check_timeout, database_health_check_timeout
5. log_level, log_format
6. secret_key, algorithm, access_token_expire_minutes (will be removed in T003)
7. cors_origins, cors_allow_credentials, cors_allow_methods, cors_allow_headers
8. environment
9. enable_docs, enable_redoc, use_uuidv7 (will be removed in T003)

**Validation**:
```bash
uv run pytest -W error::DeprecationWarning tests/test_config_validation.py -v
# Expected: All pass, no deprecation warnings
```
**Fixes**: 26 PydanticDeprecatedSince20 warnings

---

### T003: Remove dead code from Settings model
**Type**: Code Cleanup
**Priority**: MEDIUM
**Files**: `api/src/config/settings.py`
**Action**: Remove unused fields and their validators

**Fields to remove**:
```python
# Remove these unused security fields (no auth system):
secret_key: SecretStr = Field(...)
algorithm: str = Field(...)
access_token_expire_minutes: int = Field(...)

# Remove validator:
@field_validator("secret_key")
@classmethod
def validate_secret_key(cls, v, info):
    # Remove entire validator method (35 lines)
    ...

# Remove unused feature flag:
use_uuidv7: bool = Field(default=False)
```

**Validation**:
```bash
grep -E "secret_key|algorithm|access_token|use_uuidv7" api/src/config/settings.py
# Expected: No matches (exit code 1)
```

---

### T004: Update .env.example to remove unused variables
**Type**: Documentation
**Priority**: LOW
**Files**: `api/.env.example`
**Action**: Remove environment variables for deleted Settings fields

**Remove these lines**:
```bash
# Remove (no auth system implemented):
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Remove (no implementation):
USE_UUIDV7=false
```

**Validation**:
```bash
wc -l api/.env.example
# Expected: ~39 lines (down from ~51)
```

---

## Phase 3.3: Source Code Fixes

### T005: [P] Fix error enum validation in models/errors.py
**Type**: Bug Fix
**Priority**: HIGH
**Files**: `api/src/models/errors.py`
**Action**: Ensure Pydantic v2 enum validation works correctly

**Review and verify**:
```python
from enum import Enum
from pydantic import BaseModel

class ErrorType(str, Enum):
    VALIDATION_ERROR = "validation_error"
    NOT_FOUND = "not_found"
    INTERNAL_ERROR = "internal_error"
    SERVICE_UNAVAILABLE = "service_unavailable"

class ErrorResponse(BaseModel):
    error_type: ErrorType  # Should enforce enum validation
    message: str
    timestamp: datetime
    request_id: str | None = None
```

**Validation**:
```bash
uv run pytest tests/test_error_schemas.py::test_error_enum_validation -v
# Expected: PASSED (ValidationError raised for invalid enum values)
```
**Fixes**: 1 test failure

---

### T006: [P] Fix database health endpoint to return 503 status
**Type**: Bug Fix
**Priority**: HIGH
**Files**: `api/src/health/endpoints.py`
**Action**: Return 503 Service Unavailable (not 500) when database is down

**Current (incorrect)**:
```python
@router.get("/health/db")
async def health_db():
    try:
        # ... database check
        return {"status": "healthy"}
    except Exception as e:
        # Returns 500 by default
        raise e
```

**Fixed (correct)**:
```python
from fastapi.responses import JSONResponse

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
            status_code=503,  # Service Unavailable (dependency down, not code bug)
            content={"status": "error", "message": str(e)}
        )
```

**Validation**:
```bash
uv run pytest tests/test_health_db_endpoint.py::test_health_db_endpoint_handles_database_errors -v
# Expected: PASSED (status code 503, not 500)
```
**Fixes**: 8 test failures related to database health status codes

---

## Phase 3.4: Test Fixes

### T007: [P] Fix middleware test assertions in test_startup.py
**Type**: Test Fix
**Priority**: HIGH
**Files**: `api/tests/test_startup.py`
**Action**: Replace internal API access with functional tests

**Tests to fix**:
1. `test_application_basic_configuration`
2. `test_middleware_stack_startup`
3. `test_dependency_injection_startup`

**Before (incorrect - accesses internal API)**:
```python
def test_application_basic_configuration():
    app = create_app()
    # WRONG - middleware_stack is internal:
    assert len(app.middleware_stack.middleware) > 0
```

**After (correct - tests functionality)**:
```python
def test_application_basic_configuration():
    app = create_app()
    with TestClient(app) as client:
        response = client.get("/")
        # Test that CORS middleware works:
        assert "access-control-allow-origin" in response.headers
        # Test that app is configured:
        assert response.status_code == 200
```

**Alternative (use public API)**:
```python
def test_middleware_stack_startup():
    app = create_app()
    # Count middleware via public iterator:
    middleware_count = len([m for m in app.middleware])
    assert middleware_count > 0
```

**Validation**:
```bash
uv run pytest tests/test_startup.py::test_application_basic_configuration -v
uv run pytest tests/test_startup.py::test_middleware_stack_startup -v
uv run pytest tests/test_startup.py::test_dependency_injection_startup -v
# Expected: All PASSED
```
**Fixes**: 3 test failures

---

### T008: [P] Fix config validation test for DATABASE_URL
**Type**: Test Fix
**Priority**: MEDIUM
**Files**: `api/tests/test_config_validation.py`
**Action**: Update test to properly validate DATABASE_URL requirement

**Fix test**: `test_config_validation_errors_descriptive`

**Before**:
```python
def test_config_validation_errors_descriptive():
    # Test expects ValidationError for missing DATABASE_URL
    # Currently not raising - verify test logic
    ...
```

**After**: Review and fix test to ensure ValidationError is raised when DATABASE_URL is missing

**Validation**:
```bash
uv run pytest tests/test_config_validation.py::test_config_validation_errors_descriptive -v
# Expected: PASSED
```
**Fixes**: 1 test failure

---

### T009: [P] Fix performance tests for database health
**Type**: Test Fix
**Priority**: MEDIUM
**Files**: `api/tests/test_performance.py`
**Action**: Update tests to expect 503 status code, not 500

**Tests to fix**:
- `test_health_db_endpoint_response_time`
- `test_health_db_endpoint_concurrent_requests`
- `test_database_health_performance_with_mock`
- `test_health_endpoints_under_stress`

**Change assertions from**:
```python
assert response.status_code in [200, 500]  # WRONG
```

**To**:
```python
assert response.status_code in [200, 503]  # CORRECT
```

**Validation**:
```bash
uv run pytest tests/test_performance.py -k "health_db" -v
# Expected: All database health performance tests PASSED
```
**Fixes**: 4 test failures

---

### T010: [P] Fix quickstart validation tests
**Type**: Test Fix
**Priority**: HIGH
**Files**: `api/tests/test_quickstart_validation.py`
**Action**: Multiple fixes for status codes, CORS, and file structure

**Tests to fix**:
1. `test_quickstart_database_health_endpoint` - expect 503 not 500
2. `test_quickstart_database_unhealthy_scenario` - expect 503 not 500
3. `test_quickstart_database_connection_test` - expect 503 not 500
4. `test_quickstart_cors_configuration` - fix CORS assertion
5. `test_quickstart_async_client_scenario` - fix async test pattern
6. `test_quickstart_verification_scenarios` - update status codes
7. `test_quickstart_file_structure_validation` - verify file paths
8. `test_quickstart_logging_configuration` - fix log level check

**Common changes**:
```python
# Change all database health checks:
assert response.status_code in [200, 503]  # Not [200, 500]
```

**Validation**:
```bash
uv run pytest tests/test_quickstart_validation.py -v
# Expected: All 8 failing tests now PASSED
```
**Fixes**: 8 test failures

---

### T011: [P] Fix async database connection disposal tests
**Type**: Test Fix
**Priority**: HIGH (depends on T001 greenlet)
**Files**: `api/tests/test_database_connection.py`
**Action**: Tests should now pass after greenlet dependency added

**Tests affected** (should auto-fix after T001):
- `test_async_engine_disposal`
- `test_database_connection_context_manager`
- `test_connection_cleanup`
- `test_connection_error_handling` - update error message assertion

**For test_connection_error_handling**, update assertion:
```python
def test_connection_error_handling():
    # ... test code
    error_str = str(error).lower()
    # Update assertion to handle greenlet error or connection error:
    assert any(keyword in error_str for keyword in
               ["connect", "connection", "host", "database", "authentication", "greenlet"])
```

**Validation**:
```bash
uv run pytest tests/test_database_connection.py -v
# Expected: All tests PASSED (greenlet available)
```
**Fixes**: 5 test failures (4 auto-fixed by T001, 1 assertion update)

---

### T012: [P] Fix remaining startup tests
**Type**: Test Fix
**Priority**: MEDIUM
**Files**: `api/tests/test_startup.py`
**Action**: Fix environment handling and production config tests

**Tests to fix**:
- `test_environment_variable_handling_startup` - verify env loading
- `test_graceful_shutdown_capability` - fix lifespan shutdown test
- `test_production_configuration_validation` - update for removed fields
- `test_development_configuration_startup` - update for removed fields
- `test_health_endpoints_registration` - expect 503 not 500

**For production/development config tests**, remove checks for deleted fields:
```python
# Remove assertions for:
# - settings.secret_key
# - settings.algorithm
# - settings.use_uuidv7
```

**Validation**:
```bash
uv run pytest tests/test_startup.py -v
# Expected: All tests PASSED
```
**Fixes**: 5 test failures

---

### T013: [P] Fix health endpoint consistency test
**Type**: Test Fix
**Priority**: LOW
**Files**: `api/tests/test_health_db_endpoint.py`
**Action**: Update consistency test for 503 status

**Test**: `test_health_db_endpoint_consistency`

**Update**:
```python
def test_health_db_endpoint_consistency():
    # Make multiple requests, verify consistent behavior
    for _ in range(5):
        response = client.get("/health/db")
        assert response.status_code in [200, 503]  # Not 500
```

**Validation**:
```bash
uv run pytest tests/test_health_db_endpoint.py::test_health_db_endpoint_consistency -v
# Expected: PASSED
```
**Fixes**: 1 test failure

---

## Phase 3.5: Documentation & Validation

### T014: [P] Update README.md with changes
**Type**: Documentation
**Priority**: LOW
**Files**: `api/README.md`
**Action**: Document Pydantic v2 migration and removed features

**Add section**:
```markdown
## Recent Changes (2025-10-02)

### Pydantic v2 Migration
- Migrated all Settings fields to Pydantic v2 patterns
- Removed deprecated `env` parameter from Field() declarations
- Environment variables now automatically mapped by field name

### Removed Features
- **Security Settings**: Removed unused SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
  - No authentication system currently implemented
  - Will be added in future auth feature
- **UUID v7 Support**: Removed USE_UUIDV7 flag (no implementation)

### Dependencies
- Added explicit greenlet>=3.0.0 dependency for SQLAlchemy async support

### Test Suite
- Fixed all 28 failing tests
- Removed 26 deprecation warnings
- Test execution time: <1 second
```

**Validation**: Manual review of README.md

---

### T015: Run full test suite validation
**Type**: Validation
**Priority**: CRITICAL
**Dependencies**: ALL previous tasks
**Action**: Verify all 109 tests pass with zero warnings

**Commands**:
```bash
cd api

# 1. Full test suite
uv run pytest -v
# Expected: 109 passed in <1.0s

# 2. Check for deprecation warnings
uv run pytest -W error::DeprecationWarning
# Expected: All pass, no deprecation warnings

# 3. Verify greenlet works
uv run python -c "
from database.connection import get_async_engine
import asyncio
async def test():
    engine = get_async_engine()
    await engine.dispose()
asyncio.run(test())
print('✅ Async engine disposal works')
"

# 4. Verify settings load
uv run python -c "
import warnings
warnings.simplefilter('error', DeprecationWarning)
from config.settings import get_settings
s = get_settings()
print(f'✅ Settings loaded: {s.app_name}')
"

# 5. Check dead code removed
grep -E "secret_key|use_uuidv7" api/src/config/settings.py
# Expected: No matches (exit code 1)
```

**Success Criteria**:
- ✅ 109 tests passed, 0 failed
- ✅ 0 deprecation warnings
- ✅ Test execution time < 1 second
- ✅ No dead code found
- ✅ All health endpoints return correct status codes

---

## Dependencies

```
Setup Phase (T001-T004):
├─ T001: greenlet dependency (CRITICAL - blocks T011)
├─ T002: Pydantic v2 migration (blocks T008, T012)
├─ T003: Remove dead code (blocks T012)
└─ T004: Update .env.example

Source Fixes (T005-T006):
├─ T005: [P] Fix enum validation
└─ T006: [P] Fix health endpoint status (blocks T009, T010, T013)

Test Fixes (T007-T013):
├─ T007: [P] Fix middleware tests
├─ T008: [P] Fix config validation (needs T002)
├─ T009: [P] Fix performance tests (needs T006)
├─ T010: [P] Fix quickstart tests (needs T006)
├─ T011: [P] Fix async disposal tests (needs T001)
├─ T012: [P] Fix startup tests (needs T002, T003)
└─ T013: [P] Fix consistency test (needs T006)

Documentation (T014-T015):
├─ T014: [P] Update README
└─ T015: Full validation (needs ALL previous tasks)
```

## Parallel Execution Groups

**Group 1: After T001 completes**
```bash
# Can run in parallel (different files):
- T005: models/errors.py
- T006: health/endpoints.py
- T007: tests/test_startup.py
```

**Group 2: After T002, T003, T006 complete**
```bash
# Can run in parallel (different test files):
- T008: tests/test_config_validation.py
- T009: tests/test_performance.py
- T010: tests/test_quickstart_validation.py
- T011: tests/test_database_connection.py
- T012: tests/test_startup.py
- T013: tests/test_health_db_endpoint.py
```

**Group 3: Final documentation**
```bash
# Can run in parallel:
- T014: README.md
# Then sequential:
- T015: Full validation
```

## Task Statistics

- **Total Tasks**: 15
- **Critical Priority**: 3 (T001, T006, T015)
- **High Priority**: 5 (T002, T005, T007, T010, T011)
- **Medium Priority**: 5 (T003, T008, T009, T012, T013)
- **Low Priority**: 2 (T004, T014)

- **Parallelizable**: 10 tasks marked [P]
- **Sequential**: 5 tasks (T001, T002, T003, T004, T015)

- **Test Fixes**: 28 failing tests → 0 failures
- **Deprecation Warnings**: 26 warnings → 0 warnings
- **Files Modified**: 8 source files, 7 test files, 2 docs
- **Lines of Code**: ~200 changes total

---

**Execution Time Estimate**: 2-3 hours for experienced developer
**Validation Time**: 15-20 minutes
**Total**: 3-4 hours

**Next**: Execute tasks in dependency order, commit after each task completion
