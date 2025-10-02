# Research: API Backend Directory Restructuring

**Feature**: 002-migrate-api-backend
**Created**: 2025-10-02

## Research Topics

### 1. Python src Layout Best Practices

**Decision**: Adopt standard src/ layout with all application code under src/, keeping tests/, migrations/, and config files at project root.

**Rationale**:
- **Editable installs isolation**: src/ layout prevents accidentally importing from the project root during development, ensuring imports work the same way in development and production
- **Test isolation**: Tests must import from installed package, not local files, catching import issues early
- **Packaging best practice**: Recommended by Python Packaging Authority (PyPA) and widely adopted in modern Python projects
- **Tool compatibility**: Well-supported by pytest, uv, setuptools, and other modern Python tools

**Alternatives considered**:
- **Flat layout**: Current structure, simpler but allows accidental imports from project root
- **Nested package layout**: Adds unnecessary depth for single-application projects

**Implementation details**:
- Move all application modules to `src/` directory
- Keep `migrations/` and `tests/` at project root (standard practice)
- Add `__init__.py` to make src/ a namespace (optional, depends on packaging approach)

### 2. Package Discovery Configuration

**Decision**: Use automatic package discovery with `packages = find:` in pyproject.toml, configured to search in src/ directory.

**Rationale**:
- **Automatic discovery**: No manual package list maintenance
- **Future-proof**: New packages automatically included
- **Standard approach**: Recommended by setuptools and modern Python packaging guides
- **Simple configuration**: Single `where = ["src"]` directive

**Alternatives considered**:
- **Manual package list**: `packages = ["config", "database", ...]` - requires updates when adding packages
- **Namespace packages**: More complex, unnecessary for single application

**Implementation details**:
```toml
[tool.setuptools.packages.find]
where = ["src"]
```

### 3. Import Path Strategy

**Decision**: Use absolute imports from package root for all internal imports.

**Rationale**:
- **Clarity**: `from config.settings import get_settings` is clearer than `from ..config.settings import get_settings`
- **Refactoring safety**: Absolute imports don't break when moving files
- **Tool compatibility**: Better IDE support and static analysis
- **Consistency**: Matches existing codebase pattern

**Alternatives considered**:
- **Relative imports**: More fragile during refactoring, harder to track dependencies
- **Mixed approach**: Inconsistent, harder to maintain

**Implementation details**:
- All imports remain as-is: `from config import ...`, `from database import ...`
- Python will resolve these from src/ directory after pyproject.toml update
- No import path changes needed in source files

### 4. pytest Configuration

**Decision**: Configure pytest to add src/ to Python path and use `importmode=importlib` for modern import resolution.

**Rationale**:
- **Proper import resolution**: pytest will find modules in src/ directory
- **Modern approach**: importlib mode is the future-proof import strategy
- **No sys.path manipulation**: Clean, declarative configuration

**Alternatives considered**:
- **PYTHONPATH environment variable**: Fragile, environment-dependent
- **conftest.py sys.path modification**: Hacky, not recommended
- **Install package in editable mode**: Best practice, but pytest.ini provides fallback

**Implementation details**:
```ini
[tool.pytest.ini_options]
pythonpath = ["src"]
testpaths = ["tests"]
asyncio_mode = "auto"
```

### 5. Alembic Migration Configuration

**Decision**: Update alembic.ini and migrations/env.py to reference src/ paths for model imports.

**Rationale**:
- **Model discovery**: Alembic needs to find SQLAlchemy models in new location
- **Migration generation**: Automatic migration detection requires correct import paths
- **Backward compatibility**: Existing migrations remain valid, only new ones use updated paths

**Alternatives considered**:
- **Keep migrations/ inside src/**: Non-standard, migrations are typically at project root
- **Symlink approach**: Fragile, platform-dependent

**Implementation details**:
- Update `script_location` in alembic.ini to remain `migrations`
- Update `sqlalchemy.url` loading in migrations/env.py to import from `src.config.settings`
- Update model imports in migrations/env.py: `from src.models.base import Base`

### 6. Ruff Source Directory Configuration

**Decision**: Update .ruff.toml to specify src/ as the primary source directory.

**Rationale**:
- **Linting scope**: Ruff should analyze code in src/ directory
- **Import resolution**: Ruff's import checker needs correct source root
- **Consistent with pytest**: Both tools configured for src/ layout

**Alternatives considered**:
- **No configuration change**: Ruff would still work but might have import resolution issues

**Implementation details**:
```toml
[tool.ruff]
src = ["src"]
```

### 7. Uvicorn Module Loading

**Decision**: Update dev script to load FastAPI app as `src.main:app` instead of `main:app`.

**Rationale**:
- **Correct module path**: Uvicorn needs fully qualified module name
- **Consistency**: Matches how Python will import after src/ layout
- **No PYTHONPATH required**: Clean command without environment manipulation

**Alternatives considered**:
- **Set PYTHONPATH**: Works but requires environment setup
- **Run from src/ directory**: Changes working directory, affects relative paths

**Implementation details**:
```bash
# Current: uv run uvicorn main:app --reload
# New: uv run uvicorn src.main:app --reload
```

### 8. Environment Variable Preservation

**Decision**: Check for existing .env file and preserve it; create from .env.example only if missing.

**Rationale**:
- **User data safety**: Never overwrite user-modified .env files
- **Development continuity**: Developers won't lose database credentials or API keys
- **Migration safety**: Reduces risk of configuration loss

**Alternatives considered**:
- **Always copy .env.example**: Risk of data loss
- **Merge approach**: Complex, error-prone
- **Require manual .env creation**: Less user-friendly

**Implementation details**:
```bash
if [ ! -f .env ]; then
    cp .env.example .env
fi
```

## Summary of Decisions

1. **src/ layout**: All application code moves to src/, tests/ and migrations/ stay at root
2. **Package discovery**: Automatic with `packages = find:` and `where = ["src"]`
3. **Import paths**: Absolute imports, no changes needed in source files
4. **pytest**: Add src/ to pythonpath, use importmode=importlib
5. **Alembic**: Update migrations/env.py to import from src.* modules
6. **Ruff**: Add `src = ["src"]` to configuration
7. **Uvicorn**: Load as `src.main:app` instead of `main:app`
8. **Environment**: Preserve existing .env, create from example if missing

## Risk Mitigation

- **Import errors**: Resolved by proper pytest and package configuration
- **Alembic migration issues**: Existing migrations unchanged, only env.py updated
- **Environment loss**: .env preservation strategy prevents data loss
- **Rollback**: Git branch allows easy rollback if issues arise
- **Validation**: Comprehensive test suite run ensures no functionality breaks
