# Research: FastAPI Backend Architecture Refactoring

**Feature**: FastAPI Backend Architecture Refactoring
**Phase**: Phase 0 - Outline & Research
**Date**: 2025-10-08

## Research Scope

This refactoring has **no unknowns requiring research**. The REFACTOR_SPEC.md document provides a comprehensive, prescriptive migration plan with explicit architectural decisions already made.

## Architectural Decisions

### Decision 1: Core Module Structure

**Decision**: Consolidate configuration and database infrastructure into `core/` module
**Rationale**:

- Follows FastAPI official documentation pattern for "bigger applications"
- Configuration and database are infrastructure concerns that change infrequently
- Clear separation from business logic improves maintainability
- Matches Full Stack FastAPI Template structure

**Alternatives Considered**:

- Keep existing `config/` and `database/` directories
  - **Rejected**: Doesn't follow FastAPI best practices, no clear separation of layers
- Merge everything into single `infrastructure/` module
  - **Rejected**: Less descriptive naming, doesn't match FastAPI community conventions

**References**:

- [FastAPI - Bigger Applications](https://fastapi.tiangolo.com/tutorial/bigger-applications/)
- [Full Stack FastAPI Template](https://github.com/fastapi/full-stack-fastapi-template)

### Decision 2: Models vs Schemas Separation

**Decision**: Separate SQLAlchemy models (`models/`) from Pydantic schemas (`schemas/`)
**Rationale**:

- Database structure ≠ API interface
- Security: Control what data is exposed via API (e.g., hashed_password in model, not in schema)
- Flexibility: Change database without breaking API contracts
- Standard FastAPI pattern from official documentation

**Alternatives Considered**:

- Single `models/` directory for both SQLAlchemy and Pydantic
  - **Rejected**: Conflates database layer with API layer, harder to maintain API contracts
- `dto/` directory for Pydantic schemas
  - **Rejected**: Less common in FastAPI community, `schemas/` is standard terminology

**Example Pattern**:

```python
# models/user.py - Database layer
class User(Base):
    __tablename__ = "users"
    id: Mapped[str]
    email: Mapped[str]
    hashed_password: Mapped[str]  # Stored in DB

# schemas/user.py - API layer
class UserCreate(BaseModel):
    email: EmailStr
    password: str  # Received from API

class UserResponse(BaseModel):
    id: str
    email: EmailStr
    # No password field - not exposed
```

### Decision 3: No API Versioning (No /v1/ prefix)

**Decision**: Do not add API versioning paths (e.g., `/v1/health`)
**Rationale**:

- YAGNI principle: Only one API version exists currently
- Zero functionality changes requirement: Existing `/health` paths must be preserved
- Path stability: Avoids breaking changes for existing clients
- Future-proof: Easy to add versioning later when v2 is actually needed

**Alternatives Considered**:

- Add `/v1/` prefix proactively
  - **Rejected**: Violates zero functionality changes requirement, changes API paths
- Create versioned directory structure without changing paths
  - **Rejected**: Adds unnecessary complexity without current benefit

### Decision 4: No Service Layer

**Decision**: Keep business logic in endpoint handlers (no service layer yet)
**Rationale**:

- Current scale: Only 2 endpoints exist (`/health`, `/health/db`)
- Complexity threshold: Service layer recommended at >10 endpoints
- YAGNI principle: Don't add abstraction layers until needed
- Zero functionality changes requirement: Pure refactoring only

**Alternatives Considered**:

- Add service layer proactively
  - **Rejected**: Over-engineering for current scale, violates YAGNI
- Add CRUD repositories
  - **Rejected**: SQLAlchemy ORM already provides data access abstraction

**Future Consideration**:
Add service layer when business logic becomes complex (typically >10 endpoints or when multiple endpoints share significant business logic).

### Decision 5: Minimal api/deps.py

**Decision**: Create `api/deps.py` with only re-exports, no new logic
**Rationale**:

- Zero functionality changes requirement: No new features allowed
- FastAPI pattern: Shared dependencies in `deps.py` for dependency injection
- Minimal approach: Only re-export existing `get_db_session` for convenience

**Alternatives Considered**:

- Skip `api/deps.py` entirely
  - **Rejected**: Missing standard FastAPI pattern for dependency organization
- Add new dependency helpers (caching, authentication helpers)
  - **Rejected**: Violates zero functionality changes requirement

**Implementation**:

```python
# api/deps.py
from core.db import get_db_session

__all__ = ["get_db_session"]
```

## Migration Strategy Validation

### Strategy: Create-Before-Delete with Verification Gates

**Decision**: 6-phase migration with new structure created before old structure deleted
**Rationale**:

- Safety: Rollback capability maintained throughout migration
- Verification: Multiple validation gates before irreversible cleanup
- Test preservation: All 106 tests must pass before cleanup
- Risk mitigation: Checkpoint before cleanup allows rollback decision

**Phase Breakdown**:

1. Phase 1: Create new directory structure
1. Phase 2: Create new files with migrated content
1. Phase 3: Update main.py imports
1. Phase 4: Update all other import statements
1. Phase 5: **Verification gates** (9 validation steps)
1. Phase 6: Cleanup old directories (only after verification)

**Verification Gates** (Phase 5):

1. No old imports remain (grep checks)
1. New imports present (grep checks)
1. No syntax errors (py_compile)
1. All modules importable (import tests)
1. Application startup succeeds
1. Full test suite passes (106 tests)
1. Coverage maintained (97%+)
1. Linting passes (ruff check)
1. Checkpoint for rollback decision

**Rollback Strategy**:

- Branch isolation: All changes on feature branch `004-refactor-spec-md`
- Immediate rollback: `git checkout main && git branch -D 004-refactor-spec-md`
- No impact to main: Zero risk to production codebase

## Import Mapping Reference

Complete mapping of old imports to new imports for all affected files:

| Old Import | New Import | Affected Files |
|------------|------------|----------------|
| `from config.settings import get_settings` | `from core.config import get_settings` | main.py, middleware/error_handler.py, tests/conftest.py |
| `from config.settings import reset_settings` | `from core.config import reset_settings` | tests/conftest.py |
| `from database.connection import *` | `from core.db import *` | main.py, tests/conftest.py |
| `from database.session import get_db_session` | `from core.db import get_db_session` | health/endpoints.py → api/endpoints/health.py, tests/conftest.py |
| `from health.models import *` | `from schemas.health import *` | health/endpoints.py → api/endpoints/health.py |
| `from health.endpoints import router` | `from api.endpoints.health import router` | main.py |

## File Transformation Details

### New Files to Create

**core/config.py**:

- Source: Copy from `config/settings.py`
- Modifications: None (pure move)
- Exports: `get_settings()`, `reset_settings()`, `Settings` class

**core/db.py**:

- Source: Merge `database/connection.py` + `database/session.py`
- Modifications: Update internal imports (`from config.settings` → `from core.config`)
- Exports: `get_engine()`, `get_db_session()`, `dispose_engine()`, `check_connection()`

**core/__init__.py**:

- Source: New file
- Purpose: Clean interface for core module
- Exports: All public APIs from `config.py` and `db.py`

**schemas/health.py**:

- Source: Move from `health/models.py`
- Modifications: None (pure move)
- Exports: `HealthResponse`, `DatabaseHealthResponse`

**api/endpoints/health.py**:

- Source: Move from `health/endpoints.py`
- Modifications: Update 4 import statements only
- Exports: `router` (APIRouter instance)

**api/deps.py**:

- Source: New minimal file
- Purpose: Re-export shared dependencies
- Content: `from core.db import get_db_session; __all__ = ["get_db_session"]`

### Files to Modify

**main.py**:

- Changes: Update 4 import statements
- Preserved: All router registration, startup/shutdown events, CORS config

**middleware/error_handler.py**:

- Changes: Update 1 import statement (`from config.settings` → `from core.config`)
- Preserved: All error handling logic

**tests/conftest.py**:

- Changes: Update 2 import statements
- Preserved: All fixtures and test configuration

### Files to Remove (Phase 6 Only)

After ALL verification gates pass:

- `api/src/config/` directory (entire)
- `api/src/database/` directory (entire)
- `api/src/health/` directory (entire)

## Technology Stack Confirmation

**Existing Stack** (no changes):

- Python 3.12+
- FastAPI (latest stable)
- SQLAlchemy with async support
- Pydantic for validation
- pytest with pytest-asyncio
- PostgreSQL 18+ with native uuidv7() support
- ruff for linting and formatting

**No New Dependencies**: Constitutional requirement strictly enforced

## Performance Impact Assessment

**Expected Impact**: Zero performance change
**Rationale**:

- Pure code reorganization (file moves and import updates)
- No logic changes to database connection pooling
- No changes to async/await patterns
- No changes to middleware stack
- No changes to API endpoint handlers

**Validation**:

- Existing performance characteristics maintained
- Same connection pool configuration
- Same request handling patterns
- Same error handling middleware

## Risk Assessment

**Low Risk Areas**:

- Directory creation (Phase 1)
- File content migration (Phase 2)
- Import updates in isolated files (Phase 3-4)

**Medium Risk Areas**:

- Merging database/connection.py + database/session.py into core/db.py
  - Mitigation: Careful merge, preserve all exports, test imports
- Updating imports in main.py
  - Mitigation: Only 4 imports to update, comprehensive testing

**High Risk Areas**:

- Cleanup of old directories (Phase 6)
  - Mitigation: Only execute after ALL verification gates pass
  - Rollback: Git branch isolation allows complete rollback

**Zero Tolerance**:

- Test failures: Any test failure blocks cleanup
- Coverage decrease: Any coverage drop blocks cleanup
- Linting errors: Any new linting error blocks cleanup
- Import errors: Any import failure blocks cleanup

## Research Conclusion

**Status**: ✅ Complete - No unknowns remain

This refactoring is **fully specified** with:

- Complete architectural decisions made and justified
- Comprehensive 6-phase migration plan with verification gates
- Detailed import mapping table for all affected files
- File-by-file transformation instructions
- Risk mitigation strategy with rollback capability
- Zero tolerance for test failures or coverage decrease

**No further research required** - ready to proceed to Phase 1 design.
