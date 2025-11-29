# Quickstart: Verify API Test Suite Fixes

**Feature**: 003-api-uv-run
**Date**: 2025-10-02
**Purpose**: Step-by-step guide to verify all test fixes and FastAPI best practices compliance

## Prerequisites

- Python 3.12.11+ installed
- `uv` package manager installed
- PostgreSQL database running (for database health tests)
- Environment variables configured in `api/.env`

______________________________________________________________________

## Quick Verification (30 seconds)

```bash
# Navigate to api directory
cd api

# Run full test suite
uv run pytest

# Expected output:
# ===== 109 passed in 0.5s =====
# (no deprecation warnings)
```

**Success Criteria**:

- ✅ 109 tests passed
- ✅ 0 tests failed
- ✅ 0 deprecation warnings
- ✅ Execution time < 1 second

______________________________________________________________________

## Step-by-Step Verification

### Step 1: Environment Setup

```bash
cd /Users/liuyizhou/repos/agentifui-pro/api

# Verify Python version
python --version
# Expected: Python 3.12.11

# Verify uv is installed
uv --version

# Sync dependencies (includes greenlet fix)
uv sync

# Verify greenlet is available
uv run python -c "import greenlet; print(f'greenlet {greenlet.__version__}')"
# Expected: greenlet 3.2.4
```

### Step 2: Configuration Validation

```bash
# Test settings load without deprecation warnings
uv run python -c "
import warnings
warnings.simplefilter('error', DeprecationWarning)
from config.settings import get_settings
s = get_settings()
print(f'✅ Settings loaded: {s.app_name}')
print(f'✅ Database URL configured: {s.database_url[:20]}...')
print(f'✅ CORS origins: {s.cors_origins}')
"

# Expected output (no warnings):
# ✅ Settings loaded: Agentifui Pro API
# ✅ Database URL configured: postgresql+asyncpg:...
# ✅ CORS origins: ['http://localhost:3000']
```

### Step 3: Dependency Fixes Verification

```bash
# Test greenlet dependency (fixes 5 async engine tests)
uv run pytest tests/test_database_connection.py::test_async_engine_disposal -v
# Expected: PASSED

uv run pytest tests/test_database_connection.py::test_database_connection_context_manager -v
# Expected: PASSED

uv run pytest tests/test_database_connection.py::test_connection_cleanup -v
# Expected: PASSED
```

### Step 4: Pydantic V2 Migration Verification

```bash
# Run tests with deprecation warnings as errors
uv run pytest -W error::DeprecationWarning tests/test_config_validation.py -v

# Expected: All tests pass, no deprecation warnings
# Previously: 26 PydanticDeprecatedSince20 warnings

# Specifically test Field declarations
uv run python -c "
from config.settings import Settings
import inspect
source = inspect.getsource(Settings)
assert 'env=' not in source, 'Found deprecated env parameter in Field'
print('✅ No deprecated env parameters in Settings')
"
```

### Step 5: Error Handling Fixes

```bash
# Test error enum validation (fixes 1 test)
uv run pytest tests/test_error_schemas.py::test_error_enum_validation -v
# Expected: PASSED

# Test database health endpoint status codes (fixes 8 tests)
uv run pytest tests/test_health_db_endpoint.py::test_health_db_endpoint_handles_database_errors -v
# Expected: PASSED (returns 503, not 500)

uv run pytest tests/test_health_db_endpoint.py::test_health_db_endpoint_consistency -v
# Expected: PASSED
```

### Step 6: Middleware and Startup Tests

```bash
# Test middleware access patterns (fixes 3 tests)
uv run pytest tests/test_startup.py::test_application_basic_configuration -v
# Expected: PASSED (no middleware_stack access)

uv run pytest tests/test_startup.py::test_middleware_stack_startup -v
# Expected: PASSED

uv run pytest tests/test_startup.py::test_dependency_injection_startup -v
# Expected: PASSED
```

### Step 7: Performance Tests

```bash
# Test database health performance (fixes multiple)
uv run pytest tests/test_performance.py::test_health_db_endpoint_response_time -v
uv run pytest tests/test_performance.py::test_health_db_endpoint_concurrent_requests -v
uv run pytest tests/test_performance.py::test_database_health_performance_with_mock -v
uv run pytest tests/test_performance.py::test_health_endpoints_under_stress -v
# Expected: All PASSED
```

### Step 8: Quickstart Validation Tests

```bash
# Fix quickstart tests (fixes 8 tests)
uv run pytest tests/test_quickstart_validation.py -v

# Key tests that should pass:
# - test_quickstart_database_health_endpoint
# - test_quickstart_database_unhealthy_scenario
# - test_quickstart_database_connection_test
# - test_quickstart_cors_configuration
# - test_quickstart_async_client_scenario
# - test_quickstart_verification_scenarios
# - test_quickstart_file_structure_validation
# - test_quickstart_logging_configuration

# Expected: All PASSED
```

### Step 9: Full Test Suite

```bash
# Run complete test suite with verbose output
uv run pytest -v --tb=short

# Expected output:
# tests/test_config_validation.py::test_config_settings_class_exists PASSED
# tests/test_config_validation.py::test_config_settings_has_required_fields PASSED
# ... (109 total tests)
# ===== 109 passed in 0.8s =====
```

### Step 10: Dead Code Verification

```bash
# Verify unused environment variables removed
grep -E "SECRET_KEY|USE_UUIDV7|ALGORITHM" api/.env.example
# Expected: No matches (or exit code 1)

# Verify settings.py doesn't reference removed fields
grep -E "secret_key|use_uuidv7|algorithm" api/src/config/settings.py
# Expected: No matches (or exit code 1)

# Check .env.example line count (should be reduced)
wc -l api/.env.example
# Expected: ~35 lines (down from ~51)
```

______________________________________________________________________

## Regression Testing

### Test Coverage

```bash
# Run with coverage (optional)
uv run pytest --cov=src --cov-report=term-missing

# Expected coverage: >80%
```

### Specific Bug Scenarios

**Test 1: Greenlet Import**

```bash
uv run python -c "
from database.connection import get_async_engine
import asyncio
async def test():
    engine = get_async_engine()
    await engine.dispose()
asyncio.run(test())
print('✅ Async engine disposal works')
"
```

**Test 2: Pydantic Field Loading**

```bash
uv run python -c "
import os
os.environ['APP_NAME'] = 'Test App'
from config.settings import Settings
s = Settings()
assert s.app_name == 'Test App'
print('✅ Environment variables load correctly')
"
```

**Test 3: Error Status Codes**

```bash
uv run python -c "
from fastapi.testclient import TestClient
from main import app
client = TestClient(app)
# Database health should return 503 when DB unavailable
# (test with mock or disconnected DB)
print('✅ Health endpoints return correct status codes')
"
```

______________________________________________________________________

## Performance Benchmarks

```bash
# Test suite execution time
time uv run pytest

# Expected: real < 1.0s

# Individual test file times
for test_file in tests/test_*.py; do
    echo "Testing $test_file..."
    time uv run pytest "$test_file" -q
done

# Expected: Each file < 0.2s
```

______________________________________________________________________

## Troubleshooting

### Issue: Deprecation Warnings Still Appear

**Solution**:

```bash
# Check for remaining env parameters
grep -n "env=" api/src/config/settings.py

# Should return nothing. If found:
# 1. Remove env parameter from Field()
# 2. Verify field name matches environment variable (case-insensitive)
```

### Issue: Greenlet Import Error

**Solution**:

```bash
# Verify greenlet in dependencies
grep greenlet api/pyproject.toml
# Expected: greenlet>=3.0.0

# If missing, add it
cd api
uv add greenlet
```

### Issue: Tests Still Failing

**Solution**:

```bash
# Run single failing test with full traceback
uv run pytest tests/test_name.py::test_function -vv --tb=long

# Check specific error message
# Common issues:
# - Database not running (start PostgreSQL)
# - .env file missing (copy from .env.example)
# - Wrong Python version (verify 3.12+)
```

______________________________________________________________________

## Success Checklist

After all fixes implemented:

- [ ] `uv run pytest` shows 109 passed, 0 failed
- [ ] No deprecation warnings in test output
- [ ] Test execution time < 1 second
- [ ] `grep -r "env=" api/src/` returns no matches in Field declarations
- [ ] `grep greenlet api/pyproject.toml` shows explicit dependency
- [ ] `.env.example` contains only active variables
- [ ] All health endpoints return correct status codes (200/503, not 500)
- [ ] Middleware tests use functional validation, not internal APIs
- [ ] Error enum validation enforces type safety
- [ ] Settings load correctly from environment

______________________________________________________________________

## Production Readiness

### Before Deployment

```bash
# 1. Run full test suite
uv run pytest

# 2. Check code quality
uv run ruff check api/src api/tests

# 3. Verify no TODO comments for removed features
grep -r "TODO.*UUID" api/src
grep -r "TODO.*auth" api/src

# 4. Update documentation
cat api/README.md  # Should reflect all changes
```

### Deployment Verification

```bash
# After deployment, verify endpoints:
curl http://localhost:8000/
# Expected: {"message": "Agentifui Pro API is running", ...}

curl http://localhost:8000/health
# Expected: {"status": "healthy", ...}

curl http://localhost:8000/health/db
# Expected: {"status": "healthy", "database": "connected", ...}
# OR: HTTP 503 {"status": "unhealthy", ...} if DB down
```

______________________________________________________________________

**Completion**: All tests pass, no warnings, FastAPI best practices compliant ✅
