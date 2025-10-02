# Quickstart: API Backend Directory Restructuring Validation

**Feature**: 002-migrate-api-backend
**Created**: 2025-10-02

## Prerequisites

- Git branch: `002-migrate-api-backend`
- Working directory: `/Users/liuyizhou/repos/agentifui-pro/api`
- Python: 3.12+
- uv: Installed and configured

## Pre-Migration Checklist

Before executing the migration:

1. **Verify current state**:
   ```bash
   cd /Users/liuyizhou/repos/agentifui-pro/api
   git status  # Should be on 002-migrate-api-backend branch
   ls -la      # Should see flat layout (config/, database/, etc.)
   ```

2. **Run baseline tests**:
   ```bash
   uv sync
   uv run pytest
   # All tests should pass before migration
   ```

3. **Backup user .env file** (if exists):
   ```bash
   if [ -f .env ]; then cp .env .env.backup; fi
   ```

## Migration Execution Steps

Execute these steps in order. Each step includes validation.

### Step 1: Create src/ Directory Structure

```bash
# Create src/ directory
mkdir -p src

# Verify creation
ls -la | grep src
# Expected: drwxr-xr-x ... src
```

**Validation**: src/ directory exists

### Step 2: Move Application Modules to src/

```bash
# Move all application code to src/
mv config src/
mv database src/
mv models src/
mv health src/
mv middleware src/
mv main.py src/

# Verify moves
ls -la src/
# Expected: config/, database/, models/, health/, middleware/, main.py

ls -la
# Expected: src/, migrations/, tests/, pyproject.toml, alembic.ini, etc.
# NOT expected: config/, database/, models/, etc. (these moved)
```

**Validation**:
- All modules present in src/
- No application code left in api/ root
- migrations/ and tests/ remain at root

### Step 3: Update pyproject.toml

```bash
# Add package discovery configuration
# Edit pyproject.toml to add:

[tool.setuptools.packages.find]
where = ["src"]

# After dependencies section, before end of file
```

**Validation**: pyproject.toml contains `[tool.setuptools.packages.find]` section

### Step 4: Update .ruff.toml

```bash
# Add src directory configuration
# Edit .ruff.toml to add in [tool.ruff] section:

src = ["src"]

# At the beginning of the file, in the main [tool.ruff] section
```

**Validation**: .ruff.toml contains `src = ["src"]` line

### Step 5: Add pytest Configuration

```bash
# Add pytest configuration to pyproject.toml
# Add at end of file:

[tool.pytest.ini_options]
pythonpath = ["src"]
testpaths = ["tests"]
asyncio_mode = "auto"
```

**Validation**: pyproject.toml contains `[tool.pytest.ini_options]` section

### Step 6: Update migrations/env.py

```bash
# Update imports in migrations/env.py
# Change these imports:

# OLD:
from models.base import Base
from config.settings import get_settings

# NEW:
from src.models.base import Base
from src.config.settings import get_settings

# Apply to all application imports in the file
```

**Validation**: migrations/env.py imports from src.* modules

### Step 7: Create .env File (if missing)

```bash
# Create .env from .env.example if it doesn't exist
if [ ! -f .env ]; then
    cp .env.example .env
    echo "Created .env from .env.example"
else
    echo ".env already exists - preserving user configuration"
fi

# Verify .env exists
ls -la .env
```

**Validation**: .env file exists and contains configuration

### Step 8: Synchronize Dependencies

```bash
# Run uv sync to update package
uv sync

# Expected output: Package sync completes without import errors
```

**Validation**:
- ✅ uv sync completes successfully
- ✅ No import errors
- ✅ Package installed in editable mode

### Step 9: Run Test Suite

```bash
# Run full test suite
uv run pytest

# Expected output: All tests pass
```

**Validation**:
- ✅ pytest discovers tests from tests/ directory
- ✅ Tests import from src.* modules successfully
- ✅ All tests pass (same results as pre-migration)
- ❌ If tests fail: Review import errors, check pytest configuration

### Step 10: Start API Server

```bash
# Start uvicorn server
uv run uvicorn src.main:app --reload --port 8000

# Expected output:
# INFO:     Uvicorn running on http://127.0.0.1:8000
# INFO:     Application startup complete
```

**Validation**:
- ✅ Uvicorn starts without import errors
- ✅ FastAPI application initializes
- ❌ If fails: Check module path (src.main:app), review import errors

### Step 11: Test Health Endpoint

```bash
# In another terminal, test health endpoint
curl http://localhost:3000/health

# Expected response:
# {"status":"ok","database":"connected"}
```

**Validation**:
- ✅ Health endpoint responds
- ✅ Database connection works
- ✅ Application fully functional

## Post-Migration Validation

### Validation Checklist

Mark each item after successful completion:

**Directory Structure**:
- [ ] src/ directory exists and contains all application code
- [ ] migrations/ remains at project root
- [ ] tests/ remains at project root
- [ ] Configuration files at project root

**Configuration**:
- [ ] pyproject.toml updated with package discovery
- [ ] .ruff.toml updated with src directory
- [ ] pytest configuration added
- [ ] migrations/env.py updated with src. imports

**Functionality**:
- [ ] `uv sync` completes without errors
- [ ] `uv run pytest` all tests pass
- [ ] `uv run uvicorn src.main:app` server starts
- [ ] Health endpoints respond correctly
- [ ] Database operations work

**Environment**:
- [ ] .env file exists (created or preserved)
- [ ] User .env modifications preserved
- [ ] Database connection string valid

### Smoke Test Script

Quick validation script to run after migration:

```bash
#!/bin/bash
set -e

echo "🔍 Validating migration..."

# Check directory structure
echo "✓ Checking directory structure..."
[ -d "src" ] || { echo "❌ src/ directory missing"; exit 1; }
[ -d "src/config" ] || { echo "❌ src/config/ missing"; exit 1; }
[ -d "migrations" ] || { echo "❌ migrations/ should be at root"; exit 1; }
[ -d "tests" ] || { echo "❌ tests/ should be at root"; exit 1; }

# Check configuration files
echo "✓ Checking configuration files..."
grep -q "where.*src" pyproject.toml || { echo "❌ pyproject.toml not updated"; exit 1; }
grep -q "src.*src" .ruff.toml || { echo "❌ .ruff.toml not updated"; exit 1; }

# Run uv sync
echo "✓ Running uv sync..."
uv sync || { echo "❌ uv sync failed"; exit 1; }

# Run tests
echo "✓ Running tests..."
uv run pytest -v || { echo "❌ Tests failed"; exit 1; }

# Test import
echo "✓ Testing imports..."
uv run python -c "from src.main import app; print('✓ Imports work')" || { echo "❌ Import failed"; exit 1; }

echo "✅ Migration validation complete!"
```

Save as `validate-migration.sh` and run: `bash validate-migration.sh`

## Rollback Procedure

If migration fails and needs rollback:

### Option 1: Git Rollback (Recommended)

```bash
# Discard all changes and return to main
git checkout main
git branch -D 002-migrate-api-backend

# Restart migration if needed
git checkout -b 002-migrate-api-backend
```

### Option 2: Manual Rollback

```bash
# Move modules back to root
mv src/config .
mv src/database .
mv src/models .
mv src/health .
mv src/middleware .
mv src/main.py .

# Remove src/ directory
rmdir src

# Restore original files from git
git checkout pyproject.toml .ruff.toml migrations/env.py

# Remove pytest configuration from pyproject.toml
# (Manual edit to remove [tool.pytest.ini_options] section)

# Restore .env if backed up
if [ -f .env.backup ]; then mv .env.backup .env; fi

# Verify rollback
uv sync
uv run pytest
```

## Troubleshooting

### Import Errors After Migration

**Symptom**: `ModuleNotFoundError: No module named 'config'`

**Cause**: Package discovery not configured correctly

**Fix**:
```bash
# Verify pyproject.toml has:
[tool.setuptools.packages.find]
where = ["src"]

# Run uv sync again
uv sync
```

### Test Discovery Fails

**Symptom**: pytest doesn't find tests

**Cause**: pytest configuration missing

**Fix**:
```bash
# Verify pyproject.toml has:
[tool.pytest.ini_options]
pythonpath = ["src"]
testpaths = ["tests"]

# Run pytest with explicit path
uv run pytest tests/
```

### Uvicorn Module Not Found

**Symptom**: `Error loading ASGI app. Module "src.main" not found`

**Cause**: Incorrect module path

**Fix**:
```bash
# Ensure using src.main:app not main:app
uv run uvicorn src.main:app --reload
```

### Alembic Cannot Find Models

**Symptom**: Alembic doesn't detect model changes

**Cause**: migrations/env.py still using old imports

**Fix**:
```bash
# Update migrations/env.py imports:
from src.models.base import Base
from src.config.settings import get_settings

# Test alembic
uv run alembic check
```

## Success Criteria

Migration is complete when ALL of the following are true:

1. ✅ src/ directory contains all application code
2. ✅ migrations/ and tests/ remain at root
3. ✅ `uv sync` completes without errors
4. ✅ `uv run pytest` all tests pass
5. ✅ `uv run uvicorn src.main:app` server starts
6. ✅ Health endpoint returns 200 OK
7. ✅ Database connection successful
8. ✅ Alembic commands work
9. ✅ Ruff linting passes
10. ✅ .env file preserved or created

## Next Steps

After successful migration:

1. **Commit changes**:
   ```bash
   git add .
   git commit -m "refactor(api): migrate to src/ layout structure"
   ```

2. **Update documentation**:
   - README.md with new import examples
   - CLAUDE.md with src/ layout notes

3. **Create pull request**:
   ```bash
   gh pr create --title "Migrate API backend to src/ layout" --body "See specs/002-migrate-api-backend/"
   ```

4. **Monitor CI/CD**:
   - Ensure all quality gates pass
   - Verify deployment works with new structure
