# Migration Components: API Backend Directory Restructuring

**Feature**: 002-migrate-api-backend
**Created**: 2025-10-02

## Migration Scope

This document outlines all components involved in the src/ layout migration, categorized by operation type.

## Components to Move

### Application Source Code

All application modules move from `api/` to `api/src/`:

1. **config/**

   - Current: `api/config/`
   - Target: `api/src/config/`
   - Contents: `__init__.py`, `settings.py`, `logging.py`
   - Dependencies: None (imported by other modules)

1. **database/**

   - Current: `api/database/`
   - Target: `api/src/database/`
   - Contents: `__init__.py`, `connection.py`, `session.py`, `base.py`
   - Dependencies: config (for settings)

1. **models/**

   - Current: `api/models/`
   - Target: `api/src/models/`
   - Contents: `__init__.py`, `base.py`, SQLAlchemy model files
   - Dependencies: database (for base classes)

1. **health/**

   - Current: `api/health/`
   - Target: `api/src/health/`
   - Contents: `__init__.py`, `endpoints.py`, `schemas.py`
   - Dependencies: database (for health checks)

1. **middleware/**

   - Current: `api/middleware/`
   - Target: `api/src/middleware/`
   - Contents: `__init__.py`, `error_handler.py`
   - Dependencies: config (for logging)

1. **main.py**

   - Current: `api/main.py`
   - Target: `api/src/main.py`
   - Dependencies: All above modules (FastAPI app entry point)

### Package Structure

After migration, src/ directory structure:

```
api/src/
├── __init__.py           # Created (optional, for namespace)
├── config/
│   ├── __init__.py       # Existing
│   ├── settings.py       # Existing
│   └── logging.py        # Existing
├── database/
│   ├── __init__.py       # Existing
│   ├── connection.py     # Existing
│   ├── session.py        # Existing
│   └── base.py           # Existing
├── models/
│   ├── __init__.py       # Existing
│   ├── base.py           # Existing
│   └── (model files)     # Existing
├── health/
│   ├── __init__.py       # Existing
│   ├── endpoints.py      # Existing
│   └── schemas.py        # Existing
├── middleware/
│   ├── __init__.py       # Existing
│   └── error_handler.py  # Existing
└── main.py               # Moved
```

## Components to Update

### Configuration Files

1. **pyproject.toml**

   - Update `[tool.setuptools.packages.find]` section
   - Add `where = ["src"]` directive
   - Update any hardcoded package references
   - Change: Package discovery configuration

1. **alembic.ini**

   - Update `script_location` (remains `migrations`)
   - No changes needed (migrations stay at root)
   - Keep existing configuration

1. **.ruff.toml**

   - Add `src = ["src"]` to `[tool.ruff]` section
   - Update source directory configuration
   - Change: Linting scope definition

1. **pytest configuration (pyproject.toml)**

   - Add `[tool.pytest.ini_options]` section
   - Set `pythonpath = ["src"]`
   - Set `testpaths = ["tests"]`
   - Add `asyncio_mode = "auto"`
   - Change: Test discovery and import resolution

### Migration Scripts

5. **migrations/env.py**
   - Update model imports to use src. prefix
   - Change: `from models.base import Base` → `from src.models.base import Base`
   - Change: `from config.settings import get_settings` → `from src.config.settings import get_settings`
   - Update any other application imports

### Development Scripts

6. **README.md dev commands**
   - Update uvicorn command: `main:app` → `src.main:app`
   - Update any other development commands
   - Change: Command examples and quick start guide

## Components to Preserve

### Files Staying at Project Root

1. **migrations/**

   - Location: `api/migrations/` (unchanged)
   - Reason: Standard practice, Alembic convention
   - Contents: All existing migration files

1. **tests/**

   - Location: `api/tests/` (unchanged)
   - Reason: Standard practice, pytest convention
   - Update: Test files will import from src.\* modules
   - Contents: All existing test files

1. **.env.example**

   - Location: `api/.env.example` (unchanged)
   - Reason: Template file, no code changes needed
   - Usage: Source for creating .env if missing

1. **pyproject.toml**

   - Location: `api/pyproject.toml` (updated, not moved)
   - Reason: Project configuration file stays at root

1. **alembic.ini**

   - Location: `api/alembic.ini` (updated, not moved)
   - Reason: Alembic configuration file stays at root

1. **.ruff.toml**

   - Location: `api/.ruff.toml` (updated, not moved)
   - Reason: Ruff configuration file stays at root

1. **.env** (if exists)

   - Location: `api/.env` (unchanged)
   - Reason: User configuration, must preserve
   - Action: Copy from .env.example if missing

## Import Path Updates

### Module Resolution

After migration, Python will resolve imports as follows:

**Before** (flat layout):

```python
from config.settings import get_settings
from database.connection import get_engine
from models.base import Base
```

**After** (src/ layout):

```python
# Same imports in source files - no changes needed
from config.settings import get_settings
from database.connection import get_engine
from models.base import Base
# Python resolves these from src/ directory via pyproject.toml
```

### Test Imports

Tests will need explicit src. prefix since they're outside src/ directory:

**Before**:

```python
from main import app
from config.settings import get_settings
```

**After**:

```python
from src.main import app
from src.config.settings import get_settings
```

### Alembic Imports (migrations/env.py)

**Before**:

```python
from models.base import Base
from config.settings import get_settings
```

**After**:

```python
from src.models.base import Base
from src.config.settings import get_settings
```

## Migration Validation Points

### Phase 1: Directory Structure

- [ ] src/ directory created
- [ ] All modules moved successfully
- [ ] All __init__.py files present
- [ ] No orphaned files in api/ root

### Phase 2: Configuration Updates

- [ ] pyproject.toml updated
- [ ] .ruff.toml updated
- [ ] pytest configuration added
- [ ] migrations/env.py updated

### Phase 3: Import Resolution

- [ ] `uv sync` completes without errors
- [ ] Test imports resolve correctly
- [ ] Alembic can discover models

### Phase 4: Functionality Validation

- [ ] All tests pass
- [ ] API server starts successfully
- [ ] Health endpoints respond correctly
- [ ] Database migrations work

## Rollback Strategy

If migration fails, rollback procedure:

1. **Git rollback**: `git checkout main` (branch-based safety)
1. **Or manual rollback**:
   - Move src/\* back to api/ root
   - Restore original pyproject.toml
   - Restore original .ruff.toml
   - Restore original migrations/env.py
   - Remove pytest configuration

## Migration Dependencies

```
src/ directory creation
    ↓
Move modules to src/
    ↓
Update pyproject.toml (package discovery)
    ↓
Update .ruff.toml (linting scope)
    ↓
Add pytest configuration
    ↓
Update migrations/env.py (imports)
    ↓
Create .env if missing
    ↓
Validate: uv sync
    ↓
Validate: pytest
    ↓
Validate: uvicorn startup
```

## Size and Complexity Metrics

- **Modules to move**: 6 (config, database, models, health, middleware, main.py)
- **Files to update**: 4 (pyproject.toml, .ruff.toml, pytest config, migrations/env.py)
- **Test files to update**: Automatic (via pytest configuration)
- **Estimated LoC changes**: ~50-100 lines (mostly configuration)
- **Risk level**: Low (refactoring with comprehensive validation)
