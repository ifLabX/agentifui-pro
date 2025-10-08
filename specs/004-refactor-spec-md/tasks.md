# Tasks: FastAPI Backend Architecture Refactoring

**Input**: Design documents from `/specs/004-refactor-spec-md/`
**Prerequisites**: plan.md (required), research.md, quickstart.md
**Branch**: `004-refactor-spec-md`

## Execution Flow (main)
```
1. Load plan.md from feature directory
   ✅ Loaded: 6-phase migration strategy with verification gates
   ✅ Extract: Python 3.12+, FastAPI, SQLAlchemy async, pytest, ruff
2. Load optional design documents:
   ✅ research.md: Architectural decisions and migration strategy
   ✅ quickstart.md: Complete verification checklist
   ⚠️  data-model.md: N/A (pure refactoring, no data model changes)
   ⚠️  contracts/: N/A (no API contract changes)
3. Generate tasks by category:
   ✅ Setup: Directory structure creation
   ✅ Migration: File content migration with import updates
   ✅ Verification: 9 validation gates before cleanup
   ✅ Cleanup: Remove old directories after verification
4. Apply task rules:
   ✅ Different directories = mark [P] for parallel creation
   ✅ File migrations = sequential (content dependencies)
   ✅ Import updates = [P] when different files
   ✅ Verification = sequential (blocking gates)
5. Number tasks sequentially (T001, T002...)
   ✅ 26 tasks across 6 phases
6. Generate dependency graph
   ✅ Phase dependencies documented
7. Create parallel execution examples
   ✅ Included for directory creation and import updates
8. Validate task completeness:
   ✅ All new directories created
   ✅ All file migrations covered
   ✅ All import updates specified
   ✅ All verification gates included
9. Return: SUCCESS (tasks ready for execution)
```

## Format: `[ID] [P?] Description`
- **[P]**: Can run in parallel (different files, no dependencies)
- Include exact file paths in descriptions
- Working directory: `api/` (all paths relative to api/ directory)

## Path Conventions
- **Backend refactoring**: `api/src/` for source code
- **Tests**: `api/tests/` for test files
- All paths shown assume working directory is `api/`

---

## Phase 1: Create Directory Structure

### T001 [P] Create core/ directory structure
**Description**: Create new `src/core/` directory with `__init__.py`
**Working Dir**: `api/`
**Commands**:
```bash
mkdir -p src/core
touch src/core/__init__.py
```
**Success Criteria**: Directory exists with empty `__init__.py`

### T002 [P] Create schemas/ directory structure
**Description**: Create new `src/schemas/` directory with `__init__.py`
**Working Dir**: `api/`
**Commands**:
```bash
mkdir -p src/schemas
touch src/schemas/__init__.py
```
**Success Criteria**: Directory exists with empty `__init__.py`

### T003 [P] Create api/endpoints/ directory structure
**Description**: Create new `src/api/endpoints/` nested directory structure with `__init__.py` files
**Working Dir**: `api/`
**Commands**:
```bash
mkdir -p src/api/endpoints
touch src/api/__init__.py
touch src/api/endpoints/__init__.py
```
**Success Criteria**: Both directories exist with empty `__init__.py` files

---

## Phase 2: Create New Files with Migrated Content

### T004 Create core/config.py from config/settings.py
**Description**: Copy `src/config/settings.py` to `src/core/config.py` with no modifications
**Working Dir**: `api/`
**Source**: `src/config/settings.py`
**Destination**: `src/core/config.py`
**Modifications**: None (pure copy)
**Success Criteria**:
- File created at `src/core/config.py`
- Content identical to `src/config/settings.py`
- All exports preserved: `get_settings()`, `reset_settings()`, `Settings` class

### T005 Create core/db.py by merging database files
**Description**: Merge `src/database/connection.py` + `src/database/session.py` into `src/core/db.py` with updated internal imports
**Working Dir**: `api/`
**Sources**:
- `src/database/connection.py`
- `src/database/session.py`
**Destination**: `src/core/db.py`
**Modifications**:
- Update internal imports: `from config.settings` → `from core.config`
- Combine all database-related functionality
- Preserve all exports: `get_engine()`, `get_db_session()`, `dispose_engine()`, `check_connection()`
**Success Criteria**:
- File created at `src/core/db.py`
- Contains merged content from both source files
- Internal imports updated to `from core.config`
- All original functions and exports present

### T006 Create core/__init__.py with public API exports
**Description**: Create `src/core/__init__.py` to export all public APIs from config.py and db.py
**Working Dir**: `api/`
**Destination**: `src/core/__init__.py`
**Content**:
```python
"""Core infrastructure module."""
from core.config import get_settings, reset_settings, Settings
from core.db import get_engine, get_db_session, dispose_engine, check_connection

__all__ = [
    "get_settings",
    "reset_settings",
    "Settings",
    "get_engine",
    "get_db_session",
    "dispose_engine",
    "check_connection",
]
```
**Success Criteria**: File created with all exports from config.py and db.py

### T007 Create schemas/health.py from health/models.py
**Description**: Move `src/health/models.py` content to `src/schemas/health.py` with no modifications
**Working Dir**: `api/`
**Source**: `src/health/models.py`
**Destination**: `src/schemas/health.py`
**Modifications**: None (pure move)
**Success Criteria**:
- File created at `src/schemas/health.py`
- Content identical to `src/health/models.py`
- All Pydantic models preserved: `HealthResponse`, `DatabaseHealthResponse`

### T008 Create schemas/__init__.py with health exports
**Description**: Create `src/schemas/__init__.py` to export health schemas
**Working Dir**: `api/`
**Destination**: `src/schemas/__init__.py`
**Content**:
```python
"""API schemas module."""
from schemas.health import HealthResponse, DatabaseHealthResponse

__all__ = [
    "HealthResponse",
    "DatabaseHealthResponse",
]
```
**Success Criteria**: File created with health schema exports

### T009 Create api/endpoints/health.py from health/endpoints.py
**Description**: Move `src/health/endpoints.py` to `src/api/endpoints/health.py` with updated imports
**Working Dir**: `api/`
**Source**: `src/health/endpoints.py`
**Destination**: `src/api/endpoints/health.py`
**Import Updates** (4 changes):
- `from config.settings import get_settings` → `from core.config import get_settings`
- `from database.connection import check_connection` → `from core.db import check_connection`
- `from database.session import get_db_session` → `from core.db import get_db_session`
- `from health.models import HealthResponse, DatabaseHealthResponse` → `from schemas.health import HealthResponse, DatabaseHealthResponse`
**Success Criteria**:
- File created at `src/api/endpoints/health.py`
- All imports updated to new paths
- Router logic unchanged
- Exports `router` (APIRouter instance)

### T010 Create api/deps.py with minimal dependency re-exports
**Description**: Create `src/api/deps.py` to re-export shared dependencies (no new logic)
**Working Dir**: `api/`
**Destination**: `src/api/deps.py`
**Content**:
```python
"""
Shared API dependencies.

This file only re-exports existing dependencies for convenience.
No new functionality is added.
"""
from core.db import get_db_session

__all__ = ["get_db_session"]
```
**Success Criteria**: File created with minimal re-export, no new logic

---

## Phase 3: Update Application Entry Point

### T011 Update imports in src/main.py
**Description**: Update 4 import statements in `src/main.py` to use new module paths
**Working Dir**: `api/`
**File**: `src/main.py`
**Import Updates** (4 changes):
- `from config.settings import get_settings` → `from core.config import get_settings`
- `from database.connection import dispose_engine` → `from core.db import dispose_engine`
- `from health.endpoints import router as health_router` → `from api.endpoints.health import router as health_router`
- Middleware import unchanged: `from middleware.error_handler import setup_error_handling`
**Critical Constraints**:
- ❌ DO NOT add API versioning prefixes (`/api/v1`)
- ❌ DO NOT add new routers or endpoints
- ❌ DO NOT add new middleware
- ❌ DO NOT modify configuration
- ✅ ONLY update import statements, preserve all logic
**Success Criteria**:
- All 4 imports updated to new paths
- Router registration unchanged: `app.include_router(health_router)`
- No logic changes, only import updates

---

## Phase 4: Update Import Statements

### T012 [P] Update imports in src/middleware/error_handler.py
**Description**: Update 1 import statement in middleware error handler
**Working Dir**: `api/`
**File**: `src/middleware/error_handler.py`
**Import Updates** (1 change):
- `from config.settings import get_settings` → `from core.config import get_settings`
**Success Criteria**:
- Import updated to `from core.config`
- Models import unchanged: `from models.errors import ...`
- All error handling logic unchanged

### T013 [P] Update imports in tests/conftest.py
**Description**: Update 2 import statements in test configuration fixtures
**Working Dir**: `api/`
**File**: `tests/conftest.py`
**Import Updates** (2 changes):
- `from config.settings import get_settings, reset_settings` → `from core.config import get_settings, reset_settings`
- `from database.session import get_db_session` → `from core.db import get_db_session`
**Success Criteria**:
- Both imports updated to use `core.*` paths
- All fixtures unchanged
- Test configuration logic unchanged

---

## Phase 5: Verification Gates (Sequential - All Must Pass)

### T014 Verify no old import paths remain
**Description**: Run grep checks to ensure all old import paths have been replaced
**Working Dir**: `api/`
**Commands**:
```bash
# Should return nothing (all old imports replaced)
grep -r "from config\.settings" src/ tests/
grep -r "from database\.connection" src/ tests/
grep -r "from database\.session" src/ tests/
grep -r "from health\.models" src/ tests/
grep -r "from health\.endpoints" src/ tests/
```
**Success Criteria**: All grep commands return no output (exit code 1)
**Failure Action**: If any old imports found, review and update before proceeding

### T015 Verify new import paths are present
**Description**: Run grep checks to ensure new import paths are being used
**Working Dir**: `api/`
**Commands**:
```bash
# Should find files using new imports
grep -r "from core\.config" src/ tests/
grep -r "from core\.db" src/ tests/
grep -r "from schemas\.health" src/ tests/
grep -r "from api\.endpoints\.health" src/ tests/
```
**Success Criteria**: All grep commands find expected files
**Failure Action**: If new imports missing, review migration steps

### T016 Verify Python syntax correctness
**Description**: Compile all Python files to check for syntax errors
**Working Dir**: `api/`
**Commands**:
```bash
uv run python -m py_compile src/**/*.py
uv run python -m py_compile tests/**/*.py
```
**Success Criteria**: No syntax errors (exit code 0)
**Failure Action**: Fix syntax errors before proceeding

### T017 Verify all modules can be imported
**Description**: Test that all new modules can be imported without errors
**Working Dir**: `api/`
**Commands**:
```bash
uv run python -c "from core.config import get_settings; print('✓ core.config')"
uv run python -c "from core.db import get_db_session; print('✓ core.db')"
uv run python -c "from schemas.health import HealthResponse; print('✓ schemas.health')"
uv run python -c "from api.endpoints.health import router; print('✓ api.endpoints.health')"
uv run python -c "from middleware.error_handler import setup_error_handling; print('✓ middleware')"
uv run python -c "from models.base import Base; print('✓ models.base')"
```
**Success Criteria**: All 6 modules import successfully with ✓ output
**Failure Action**: Debug import errors, check for missing dependencies or circular imports

### T018 Verify application can start successfully
**Description**: Test that the FastAPI application can initialize without errors
**Working Dir**: `api/`
**Commands**:
```bash
uv run python -c "from src.main import app; print('✓ Application initialized successfully')"
```
**Success Criteria**: Application initializes without import errors
**Failure Action**: Debug application startup errors

### T019 Run complete test suite (106 tests must pass)
**Description**: Execute all tests to ensure zero functionality changes
**Working Dir**: `api/`
**Commands**:
```bash
uv run pytest -v
```
**Success Criteria**:
- All 106 tests PASSED (100% pass rate required)
- No import errors
- No module not found errors
**Failure Action**: Debug test failures, review import updates
**Critical**: This gate BLOCKS cleanup - tests must pass 100%

### T020 Verify test coverage maintained at 97%+
**Description**: Run test coverage analysis to ensure no coverage decrease
**Working Dir**: `api/`
**Commands**:
```bash
uv run pytest --cov=src --cov-report=term-missing
```
**Success Criteria**: Overall coverage >= 97% (current baseline)
**Failure Action**: If coverage decreased, identify missing test coverage
**Critical**: Coverage decrease BLOCKS cleanup

### T021 Verify linting standards pass
**Description**: Run ruff linting to ensure no new linting errors introduced
**Working Dir**: `api/`
**Commands**:
```bash
uv run ruff check src/ tests/
```
**Success Criteria**: No new linting errors related to imports or structure
**Failure Action**: Fix linting errors before proceeding

### T022 Checkpoint for rollback decision
**Description**: Manual checkpoint to review all verification results before irreversible cleanup
**Working Dir**: `api/`
**Review Checklist**:
- [x] No old imports remaining (T014)
- [x] New imports present (T015)
- [x] No syntax errors (T016)
- [x] All modules importable (T017)
- [x] Application starts (T018)
- [x] All 106 tests pass (T019)
- [x] Coverage >= 97% (T020)
- [x] Linting passes (T021)
**Decision**:
- ✅ All checks pass → Proceed to Phase 6 cleanup
- ❌ Any check fails → STOP and rollback: `git checkout main && git branch -D 004-refactor-spec-md`
**Success Criteria**: Manual confirmation that all verification gates passed

---

## Phase 6: Cleanup (Only After All Verification Passes)

### T023 Remove src/config/ directory
**Description**: Remove old configuration directory after verification
**Working Dir**: `api/`
**Commands**:
```bash
rm -rf src/config/
```
**Prerequisites**: All verification gates (T014-T021) must pass
**Success Criteria**: Directory removed, `ls src/config/` returns "No such file"

### T024 Remove src/database/ directory
**Description**: Remove old database directory after verification
**Working Dir**: `api/`
**Commands**:
```bash
rm -rf src/database/
```
**Prerequisites**: All verification gates (T014-T021) must pass
**Success Criteria**: Directory removed, `ls src/database/` returns "No such file"

### T025 Remove src/health/ directory
**Description**: Remove old health endpoint directory after verification
**Working Dir**: `api/`
**Commands**:
```bash
rm -rf src/health/
```
**Prerequisites**: All verification gates (T014-T021) must pass
**Success Criteria**: Directory removed, `ls src/health/` returns "No such file"

### T026 Final validation - Run tests after cleanup
**Description**: Final test run to ensure cleanup didn't break anything
**Working Dir**: `api/`
**Commands**:
```bash
uv run pytest -v
uv run pytest --cov=src --cov-report=term-missing
```
**Success Criteria**:
- All 106 tests still pass
- Coverage still >= 97%
- No import errors
**Failure Action**: This should not fail if verification gates passed; if it does, investigate immediately

---

## Dependencies

### Phase Dependencies (Sequential)
```
Phase 1 (T001-T003) → Phase 2 (T004-T010) → Phase 3 (T011) → Phase 4 (T012-T013) → Phase 5 (T014-T022) → Phase 6 (T023-T026)
```

### Intra-Phase Dependencies
**Phase 1**: T001, T002, T003 can run in parallel [P]
**Phase 2**: Sequential (T004 → T005 → T006 → T007 → T008 → T009 → T010)
- T006 depends on T004, T005 (needs to know what to export)
- T008 depends on T007 (needs to know what to export)
**Phase 3**: Single task (T011)
**Phase 4**: T012, T013 can run in parallel [P]
**Phase 5**: All sequential (T014 → T015 → T016 → T017 → T018 → T019 → T020 → T021 → T022)
- Each verification gate must pass before the next
- T022 (checkpoint) blocks Phase 6 execution
**Phase 6**: Sequential (T023 → T024 → T025 → T026)

### Critical Blocking Dependencies
- **T022 blocks all of Phase 6**: No cleanup until manual checkpoint confirmation
- **T019 (test suite) blocks T020-T026**: Tests must pass 100% before any cleanup
- **T020 (coverage) blocks T023-T026**: Coverage must be maintained before cleanup

---

## Parallel Execution Examples

### Example 1: Phase 1 - Directory Creation (All Parallel)
```bash
# Launch T001-T003 together:
Task: "Create src/core/ directory with __init__.py"
Task: "Create src/schemas/ directory with __init__.py"
Task: "Create src/api/endpoints/ nested directories with __init__.py files"

# These can run in parallel because they create different directories
```

### Example 2: Phase 4 - Import Updates (Parallel)
```bash
# Launch T012-T013 together:
Task: "Update imports in src/middleware/error_handler.py from config.settings to core.config"
Task: "Update imports in tests/conftest.py from config.* and database.* to core.*"

# These can run in parallel because they modify different files
```

### Example 3: Verification Gates (Sequential Only)
```bash
# NEVER run verification gates in parallel - they must be sequential:
Task: "T014 - Verify no old imports" THEN
Task: "T015 - Verify new imports present" THEN
Task: "T016 - Verify syntax" THEN
...
Task: "T022 - Checkpoint for rollback decision"
```

---

## Notes

### Execution Guidelines
- **[P] tasks**: Can run in parallel (different files, no dependencies)
- **Sequential tasks**: Must run in order (dependencies, same files, or verification gates)
- **Commit strategy**: Commit after each phase completes successfully
- **Rollback safety**: Keep old directories until Phase 5 verification passes completely

### Critical Constraints
- ❌ **Zero functionality changes**: No new features, logic changes, or API modifications
- ❌ **Zero tolerance for test failures**: All 106 tests must pass before cleanup
- ❌ **Zero coverage decrease**: Must maintain 97%+ coverage
- ✅ **Pure refactoring**: Only file moves and import updates allowed

### Risk Mitigation
- **Create before delete**: All new files created in Phase 2 before old files removed in Phase 6
- **Verification gates**: 9 validation steps in Phase 5 before irreversible cleanup
- **Checkpoint gate**: Manual decision point (T022) before cleanup
- **Rollback capability**: Git branch isolation allows complete rollback at any point

### Common Pitfalls to Avoid
1. **Skipping verification gates**: All gates in Phase 5 must pass before Phase 6
2. **Parallel cleanup**: Phase 6 tasks must be sequential (directory removal order matters for error messages)
3. **Incomplete import updates**: Use grep verification (T014, T015) to catch missed imports
4. **Test failures ignored**: Any test failure blocks cleanup (T019 is critical gate)

---

## Task Generation Validation

### Validation Checklist
- [x] All new directories have creation tasks (T001-T003)
- [x] All file migrations specified with exact sources and destinations (T004-T010)
- [x] All import updates documented with old → new mappings (T011-T013)
- [x] All verification steps from quickstart.md included (T014-T021)
- [x] Checkpoint gate included before cleanup (T022)
- [x] All old directories have removal tasks (T023-T025)
- [x] Final validation included (T026)
- [x] Parallel tasks truly independent (different files/directories)
- [x] Each task specifies exact file paths or commands
- [x] No task modifies same file as another [P] task
- [x] All phase dependencies documented
- [x] Critical blocking gates identified

### Completeness Check
- ✅ Setup tasks: 3 directory creation tasks
- ✅ Migration tasks: 7 file creation/migration tasks
- ✅ Import update tasks: 3 files with import updates
- ✅ Verification tasks: 9 validation gates
- ✅ Cleanup tasks: 4 directory removal + final validation
- ✅ Total: 26 tasks covering complete refactoring workflow

**Validation Result**: ✅ PASS - All tasks generated, dependencies mapped, ready for execution

---

**Estimated Total Time**: 40 minutes (per research.md estimate)
**Risk Level**: Low (pure refactoring with comprehensive verification)
**Rollback Available**: Yes (git branch isolation, pre-cleanup verification gates)
