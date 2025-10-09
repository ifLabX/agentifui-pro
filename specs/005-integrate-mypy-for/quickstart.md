# Quickstart: Mypy Type Checking Validation

## Purpose

This guide provides step-by-step validation procedures to verify that mypy static type checking is correctly integrated and functioning as expected.

## Prerequisites

- Python 3.12+ installed
- `uv` package manager installed
- Access to `api/` directory
- Git repository initialized

## Validation Phases

### Phase 1: Installation Verification

**Objective**: Confirm mypy is installed and accessible

```bash
# Navigate to API directory
cd api

# Verify mypy is in dev dependencies
grep -A 5 "\[dependency-groups\]" pyproject.toml | grep mypy

# Expected output: "mypy>=1.8.0"

# Verify mypy executable is available
uv run mypy --version

# Expected output: "mypy 1.8.0 (compiled: yes)" or similar
```

**Success Criteria**:
- ✅ mypy found in pyproject.toml dev dependencies
- ✅ mypy version 1.8.0 or higher
- ✅ No command execution errors

---

### Phase 2: Configuration Validation

**Objective**: Verify mypy configuration is correctly set up

```bash
# Check configuration section exists
grep -A 20 "\[tool.mypy\]" pyproject.toml

# Expected output should include:
# - strict = true
# - plugins = ["pydantic.mypy"]
# - python_version = "3.12"
# - mypy_path = "src"
```

**Manual Verification Checklist**:
- [ ] `[tool.mypy]` section exists in pyproject.toml
- [ ] `strict = true` is set
- [ ] `plugins = ["pydantic.mypy"]` is configured
- [ ] `python_version = "3.12"` matches project requirement
- [ ] `mypy_path` and `packages` point to "src"
- [ ] `exclude` contains "migrations/" pattern
- [ ] Module overrides exist for migrations and asyncpg

---

### Phase 3: Basic Execution Test

**Objective**: Verify mypy can run on the codebase

```bash
# Run mypy on the entire codebase
cd api
uv run mypy .

# Observe output - should either:
# 1. "Success: no issues found in N source files"
# 2. List of type errors with file:line:column format
#
# Should NOT show:
# - Configuration errors
# - Plugin loading errors
# - Fatal crashes
```

**Success Criteria**:
- ✅ Mypy executes without fatal errors (exit code 0 or 1, not 2)
- ✅ If errors found, they are type errors, not configuration errors
- ✅ Error messages show file paths, line numbers, error codes
- ✅ Summary line shows "checked N source files"

---

### Phase 4: Cache Functionality Test

**Objective**: Verify incremental caching works correctly

```bash
# First run (cold cache)
rm -rf .mypy_cache/
time uv run mypy .

# Record time (should be ~10-30 seconds for full check)
# Example: "real    0m12.450s"

# Second run (warm cache, no changes)
time uv run mypy .

# Record time (should be significantly faster, ~2-5 seconds)
# Example: "real    0m3.123s"

# Verify cache directory created
ls -la .mypy_cache/

# Expected: Directory exists with subdirectories
```

**Success Criteria**:
- ✅ `.mypy_cache/` directory created after first run
- ✅ Cache contains `3.12/` subdirectory (Python version)
- ✅ Second run is 5-10x faster than first run
- ✅ Both runs produce identical results

**Performance Benchmarks**:
- Cold cache: <30 seconds for ~15 files
- Warm cache: <5 seconds for no changes
- Speedup factor: >5x

---

### Phase 5: Type Error Detection Test

**Objective**: Verify mypy correctly detects type errors

```bash
# Create test file with intentional type error
cat > src/test_type_error.py << 'EOF'
def get_number() -> int:
    return "this is a string, not an int"

def greet(name: str) -> str:
    return 123  # Wrong return type

async def fetch_data() -> int:
    return "not an integer"
EOF

# Run mypy
uv run mypy src/test_type_error.py

# Expected output:
# src/test_type_error.py:2: error: Incompatible return value type (got "str", expected "int")  [return-value]
# src/test_type_error.py:5: error: Incompatible return value type (got "int", expected "str")  [return-value]
# src/test_type_error.py:8: error: Incompatible return value type (got "str", expected "int")  [return-value]
# Found 3 errors in 1 file (checked 1 source file)

# Clean up test file
rm src/test_type_error.py
```

**Success Criteria**:
- ✅ All 3 type errors detected
- ✅ Error messages include error codes `[return-value]`
- ✅ Error messages show correct file and line numbers
- ✅ Exit code is 1 (type errors found)

---

### Phase 6: Strict Mode Validation

**Objective**: Verify strict mode is enforced

```bash
# Create test file without type annotations
cat > src/test_strict_mode.py << 'EOF'
def process_data(data):  # No type annotations
    return data

class User:  # No type annotations on methods
    def __init__(self, name):
        self.name = name
EOF

# Run mypy
uv run mypy src/test_strict_mode.py

# Expected output should include errors like:
# Function is missing a type annotation  [no-untyped-def]
# Function is missing a return type annotation  [no-untyped-def]

# Clean up
rm src/test_strict_mode.py
```

**Success Criteria**:
- ✅ Errors reported for missing type annotations
- ✅ Error codes include `[no-untyped-def]` or similar
- ✅ Strict mode prevents untyped code

---

### Phase 7: Pydantic Plugin Test

**Objective**: Verify Pydantic plugin is working

```bash
# Create test file with Pydantic model
cat > src/test_pydantic.py << 'EOF'
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    email: str

# Valid usage
user = User(id=1, name="Alice", email="alice@example.com")

# Invalid usage - wrong type
invalid_user = User(id="not_an_int", name="Bob", email="bob@example.com")
EOF

# Run mypy
uv run mypy src/test_pydantic.py

# Expected: Error on line with invalid_user
# Argument "id" has incompatible type "str"; expected "int"  [arg-type]

# Clean up
rm src/test_pydantic.py
```

**Success Criteria**:
- ✅ Pydantic model instantiation type-checked
- ✅ Invalid field types detected
- ✅ Error code is `[arg-type]`
- ✅ Plugin provides accurate type information

---

### Phase 8: Async Pattern Validation

**Objective**: Verify async/await type checking

```bash
# Create test file with async patterns
cat > src/test_async.py << 'EOF'
from collections.abc import AsyncIterator

async def arange(n: int) -> AsyncIterator[int]:
    for i in range(n):
        yield i

async def get_value() -> int:
    return 42

async def main() -> None:
    # Valid: await coroutine
    value: int = await get_value()

    # Invalid: await non-awaitable
    result = await 123
EOF

# Run mypy
uv run mypy src/test_async.py

# Expected: Error on "await 123" line
# Incompatible types in "await" (actual type "int", expected type "Awaitable[Any]")

# Clean up
rm src/test_async.py
```

**Success Criteria**:
- ✅ Async generator type correctly inferred
- ✅ Coroutine await validated
- ✅ Invalid await detected
- ✅ AsyncIterator vs Coroutine types distinguished

---

### Phase 9: Exclusion Test

**Objective**: Verify migration files are excluded

```bash
# Check if migrations exist
ls migrations/versions/ 2>/dev/null || echo "No migrations yet"

# If migrations exist, run mypy on entire codebase
uv run mypy .

# Verify no errors from migrations directory
# If migrations have type issues, they should be ignored

# Alternative: Create test migration
mkdir -p migrations/versions
cat > migrations/versions/test_migration.py << 'EOF'
# This file has no type annotations - would fail strict mode
def upgrade():
    pass

def downgrade():
    pass
EOF

# Run mypy
uv run mypy .

# Expected: No errors from test_migration.py

# Clean up
rm migrations/versions/test_migration.py
```

**Success Criteria**:
- ✅ Migration files not reported in error list
- ✅ Migration files not included in "checked N source files" count
- ✅ Exclusion pattern working correctly

---

### Phase 10: Pre-commit Hook Test

**Objective**: Verify pre-commit hook runs mypy

```bash
# Check if Husky is installed
ls -la .husky/pre-commit

# Create test file with type error
cat > api/src/test_precommit.py << 'EOF'
def broken_function() -> int:
    return "string not int"
EOF

# Stage the file
git add api/src/test_precommit.py

# Attempt commit (should fail)
git commit -m "test: type error detection"

# Expected behavior:
# - Pre-commit hook runs
# - Mypy detects error
# - Commit is blocked
# - Error message displayed

# Clean up (unstage file)
git reset HEAD api/src/test_precommit.py
rm api/src/test_precommit.py
```

**Success Criteria**:
- ✅ Pre-commit hook executes mypy
- ✅ Type errors block commit
- ✅ Error messages displayed in console
- ✅ Commit allowed after fixing errors

---

### Phase 11: Performance Validation

**Objective**: Verify performance meets expectations

```bash
# Measure cold cache performance
rm -rf .mypy_cache/
time uv run mypy .

# Record time - should be <30s for ~15 files

# Measure warm cache performance (no changes)
time uv run mypy .

# Record time - should be <5s

# Measure incremental performance (single file change)
touch src/models/base.py  # Trigger mtime change
time uv run mypy .

# Record time - should be <5s
```

**Performance Acceptance Criteria**:
- ✅ Cold cache full check: <30 seconds (for ~15 files)
- ✅ Warm cache no changes: <5 seconds
- ✅ Incremental single file: <5 seconds
- ✅ Speedup factor: >5x (warm vs cold)

---

## Final Validation Checklist

### Configuration
- [ ] Mypy installed in dev dependencies (≥1.8.0)
- [ ] Configuration section exists in pyproject.toml
- [ ] Strict mode enabled
- [ ] Pydantic plugin configured
- [ ] Python version set to 3.12
- [ ] Exclusions configured for migrations

### Functionality
- [ ] Mypy executes without configuration errors
- [ ] Type errors correctly detected
- [ ] Strict mode enforced (no untyped code)
- [ ] Pydantic models type-checked
- [ ] Async patterns validated
- [ ] Migration files excluded
- [ ] Cache provides performance improvement

### Integration
- [ ] Pre-commit hook runs mypy
- [ ] Type errors block commits
- [ ] .mypy_cache in .gitignore
- [ ] Error messages clear and actionable

### Performance
- [ ] Cold cache check completes in <30s
- [ ] Warm cache check completes in <5s
- [ ] Incremental check completes in <5s
- [ ] Speedup factor >5x

---

## Troubleshooting

### Issue: Mypy not found
```bash
# Solution: Ensure dependencies are installed
cd api
uv sync --dev
```

### Issue: Plugin not loading
```bash
# Check if pydantic is installed
uv run python -c "import pydantic; print(pydantic.__version__)"

# Reinstall if needed
uv sync --dev
```

### Issue: Cache not providing speedup
```bash
# Clear and rebuild cache
rm -rf .mypy_cache/
uv run mypy .

# Verify cache directory structure
find .mypy_cache -type f
```

### Issue: Too many type errors
```bash
# Start with specific module
uv run mypy src/models/

# Fix errors incrementally by module
uv run mypy src/schemas/
uv run mypy src/api/
```

---

## Success Metrics

| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| Installation | 100% success | Phase 1 passes |
| Configuration | 100% correct | Phase 2 checklist complete |
| Execution | No fatal errors | Phase 3 passes |
| Caching | >5x speedup | Phase 4 benchmark |
| Error Detection | 100% accuracy | Phase 5-8 pass |
| Integration | Blocks bad commits | Phase 10 passes |
| Performance | Meets SLAs | Phase 11 benchmarks |

---

## Completion Sign-off

When all validation phases pass and all checklists are complete, the mypy integration is production-ready.

**Sign-off**: [ ] All validation phases completed successfully
**Date**: ___________
**Validated By**: ___________
