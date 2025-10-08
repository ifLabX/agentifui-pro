# Implementation Plan: FastAPI Backend Architecture Refactoring

**Branch**: `004-refactor-spec-md` | **Date**: 2025-10-08 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/004-refactor-spec-md/spec.md`

## Execution Flow (/plan command scope)
```
1. Load feature spec from Input path
   ✅ Loaded: Zero-functionality refactoring to FastAPI best practices
2. Fill Technical Context (scan for NEEDS CLARIFICATION)
   ✅ Detect Project Type: web (frontend + backend)
   ✅ Set Structure Decision: Backend-only refactoring
3. Fill the Constitution Check section
   ✅ Completed based on constitution.md
4. Evaluate Constitution Check section
   ✅ No constitutional violations - pure refactoring
   ✅ Update Progress Tracking: Initial Constitution Check
5. Execute Phase 0 → research.md
   ✅ No NEEDS CLARIFICATION - spec is comprehensive
6. Execute Phase 1 → contracts, data-model.md, quickstart.md, CLAUDE.md
   ✅ Generate design artifacts
7. Re-evaluate Constitution Check section
   ✅ No new violations after design
   ✅ Update Progress Tracking: Post-Design Constitution Check
8. Plan Phase 2 → Describe task generation approach
   ✅ TDD-based task ordering defined
9. STOP - Ready for /tasks command
```

**IMPORTANT**: The /plan command STOPS at step 9. Phases 2-4 are executed by other commands:
- Phase 2: /tasks command creates tasks.md
- Phase 3-4: Implementation execution (manual or via tools)

## Summary

**Primary Requirement**: Reorganize the FastAPI backend (`api/src/`) to follow official FastAPI best practices and industry standards, consolidating configuration and database infrastructure into a `core/` module, separating Pydantic schemas into `schemas/`, and organizing API endpoints under `api/endpoints/`.

**Technical Approach**: Six-phase migration strategy with new structure created first, comprehensive verification gates before cleanup, and zero tolerance for functionality changes. All 106 existing tests must pass with 97%+ coverage maintained throughout the refactoring process.

## Technical Context
**Language/Version**: Python 3.12+
**Primary Dependencies**: FastAPI, SQLAlchemy (async), Pydantic, pytest, ruff
**Storage**: PostgreSQL 18+ (with native uuidv7() support)
**Testing**: pytest with pytest-asyncio, minimum 80% coverage (currently 97%+)
**Target Platform**: Linux server (FastAPI application)
**Project Type**: web (backend refactoring only, frontend unchanged)
**Performance Goals**: Maintain existing API response times (<200ms p95)
**Constraints**: Zero functionality changes, 100% test pass rate, no API contract modifications
**Scale/Scope**: ~8 source files affected, 106 tests must continue passing, single developer migration

## Constitution Check
*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### ✅ I. Dual-Stack Excellence
- **Status**: PASS (N/A - Backend-only refactoring)
- **Validation**: No frontend changes, no API contract modifications, existing OpenAPI schemas unchanged

### ✅ II. Quality-First Development
- **Status**: PASS
- **Validation**:
  - Ruff linting must pass with no new errors (120 char line length)
  - All type hints preserved during file reorganization
  - Pre-commit hooks will validate quality on all commits
  - Existing quality standards maintained, no relaxation

### ✅ III. Test-Driven Implementation
- **Status**: PASS
- **Validation**:
  - All 106 existing tests must pass (100% success rate required)
  - Test coverage maintained at 97%+ (no decrease tolerated)
  - No test modifications except import path updates
  - Integration tests validate runtime behavior unchanged

### ✅ IV. Internationalization by Design
- **Status**: PASS (N/A - Backend-only, no user-facing text changes)
- **Validation**: No UI components affected, no translation changes

### ✅ V. Convention Consistency
- **Status**: PASS
- **Validation**:
  - Python module naming conventions maintained (snake_case)
  - Commit message: "refactor: reorganize backend to FastAPI best practices"
  - Code comments in English, minimal and purposeful
  - Import organization follows Python standards (stdlib → third-party → local)

### 🎯 Spec-Kit Workflow
- **Status**: PASS
- **Validation**:
  - Specification created: `specs/004-refactor-spec-md/spec.md` ✅
  - Implementation plan: `specs/004-refactor-spec-md/plan.md` ✅ (this file)
  - Tasks generation: Pending `/tasks` command execution
  - Implementation: Will follow TDD principles with verification gates

### 🏗️ Architecture Patterns
- **Status**: PASS
- **Validation**:
  - No new dependencies introduced
  - Maintains FastAPI dependency injection patterns
  - Maintains async/await for all I/O operations
  - No database migration changes (Alembic migrations untouched)
  - Error handling middleware unchanged

### ⚖️ Quality Gates
- **Status**: PASS
- **Pre-refactor Baseline**:
  - Type checking: All functions have type hints ✅
  - Linting: Ruff passes with existing configuration ✅
  - Testing: 106 tests passing, 97%+ coverage ✅
  - Pre-commit: Husky hooks active ✅
- **Post-refactor Requirements**:
  - Same type coverage maintained
  - Same linting standards maintained
  - Same test count and coverage maintained
  - Same pre-commit validation

## Project Structure

### Documentation (this feature)
```
specs/004-refactor-spec-md/
├── spec.md              # Feature specification (completed)
├── plan.md              # This file (/plan command output)
├── research.md          # Phase 0 output (/plan command)
├── data-model.md        # Phase 1 output (/plan command) - N/A for refactoring
├── quickstart.md        # Phase 1 output (/plan command)
├── contracts/           # Phase 1 output (/plan command) - N/A (no API changes)
└── tasks.md             # Phase 2 output (/tasks command - NOT created by /plan)
```

### Source Code (repository root)
```
# Backend refactoring only - web/ unchanged
api/
├── src/
│   ├── core/                    # NEW: Core infrastructure
│   │   ├── __init__.py          # NEW: Exports get_settings, get_db_session, etc.
│   │   ├── config.py            # NEW: From config/settings.py
│   │   └── db.py                # NEW: From database/connection.py + session.py
│   │
│   ├── models/                  # UNCHANGED LOCATION
│   │   ├── __init__.py
│   │   ├── base.py
│   │   └── errors.py
│   │
│   ├── schemas/                 # NEW: Pydantic API schemas
│   │   ├── __init__.py          # NEW: Export health schemas
│   │   └── health.py            # NEW: From health/models.py
│   │
│   ├── api/                     # NEW: API layer
│   │   ├── __init__.py          # NEW: Empty marker
│   │   ├── deps.py              # NEW: Re-export get_db_session
│   │   └── endpoints/           # NEW: Endpoint modules
│   │       ├── __init__.py      # NEW: Empty marker
│   │       └── health.py        # NEW: From health/endpoints.py
│   │
│   ├── middleware/              # UNCHANGED LOCATION
│   │   ├── __init__.py
│   │   └── error_handler.py    # MODIFIED: Updated imports only
│   │
│   ├── main.py                  # MODIFIED: Updated imports only
│   │
│   ├── config/                  # REMOVED IN PHASE 6 (after verification)
│   ├── database/                # REMOVED IN PHASE 6 (after verification)
│   └── health/                  # REMOVED IN PHASE 6 (after verification)
│
└── tests/
    ├── conftest.py              # MODIFIED: Updated imports
    ├── test_*.py                # MODIFIED: Import updates via fixtures
    └── [all test files]         # MUST PASS: 106 tests, 97%+ coverage
```

**Structure Decision**: Backend-only refactoring within existing `api/` directory. The new structure follows FastAPI's recommended layered architecture with clear separation between infrastructure (`core/`), data models (`models/`), API contracts (`schemas/`), and API routes (`api/endpoints/`). Frontend (`web/`) is completely unchanged.

## Phase 0: Outline & Research
**Status**: No research required - refactoring specification is comprehensive

### Research Analysis
1. **Unknowns Assessment**: Technical Context has no NEEDS CLARIFICATION markers
2. **Specification Completeness**: REFACTOR_SPEC.md provides:
   - Complete current and target architecture diagrams
   - Detailed 6-phase migration plan with verification steps
   - Comprehensive import mapping table
   - File-by-file transformation instructions
   - Complete verification checklist (9 verification steps)

3. **Best Practices Validation**:
   - **Decision**: FastAPI official project structure (core/, schemas/, api/endpoints/)
   - **Rationale**: Matches FastAPI documentation and Full Stack FastAPI Template patterns
   - **Alternatives considered**:
     - Domain-driven structure (premature for <10 endpoints)
     - API versioning with /v1/ (YAGNI - no v2 exists yet)
     - Service layer (unnecessary for current scale)

4. **Technology Stack Confirmation**:
   - Python 3.12+, FastAPI, SQLAlchemy async, Pydantic, pytest (all existing)
   - No new dependencies introduced (constitutional requirement)
   - PostgreSQL 18+ with native uuidv7() support (existing)

**Output**: Research complete - proceeding to Phase 1 design

## Phase 1: Design & Contracts
*Prerequisites: research.md complete*

### 1. Data Model
**Status**: N/A - No data model changes (pure refactoring)

The refactoring does NOT modify any data models. Existing SQLAlchemy models in `models/base.py` and `models/errors.py` remain completely unchanged. Only their import locations change for consumers.

### 2. API Contracts
**Status**: No contract changes - verification only

**Critical Constraint**: Zero API contract modifications allowed

**Existing Contracts** (preserved unchanged):
```
GET /health         → 200 OK {"status": "healthy"}
GET /health/db      → 200 OK {"status": "healthy"} or 503 Service Unavailable
```

**Verification Strategy**:
- Existing OpenAPI schema must remain byte-identical
- All request/response formats unchanged
- HTTP status codes preserved
- No new endpoints added
- No endpoint paths modified

### 3. Contract Tests
**Status**: Existing tests preserved, imports updated

**Test Preservation Requirements**:
- All 106 existing tests must pass unchanged
- Test coverage maintained at 97%+ (no decrease)
- Only import paths updated in test files
- Test logic and assertions completely unchanged

**Modified Test Files**:
```
tests/conftest.py           → Update: from core.config, from core.db
tests/test_health_*.py      → Indirect updates via fixtures
tests/test_database_*.py    → Indirect updates via fixtures
tests/test_config_*.py      → Indirect updates via fixtures
```

### 4. Integration Tests
**Status**: Existing integration tests serve as regression protection

**Regression Protection**:
- Health endpoint tests validate API behavior unchanged
- Database connection tests validate infrastructure unchanged
- Configuration tests validate settings management unchanged
- Application startup test validates initialization unchanged

### 5. Agent File Update
**Status**: Executing incremental CLAUDE.md update

Running agent context update script:

**Output**: quickstart.md, CLAUDE.md update (preserves manual content)

## Phase 2: Task Planning Approach
*This section describes what the /tasks command will do - DO NOT execute during /plan*

**Task Generation Strategy**:
- Load `.specify/templates/tasks-template.md` as base
- Generate tasks following 6-phase migration plan from REFACTOR_SPEC.md
- Each phase → grouped tasks with explicit dependencies
- Verification gates → blocking tasks before cleanup

**Phase-Based Task Groups**:
1. **Phase 1: Create Structure** [P] - Parallel directory creation
   - Task: Create core/, schemas/, api/endpoints/ directories
   - Task: Create all __init__.py files

2. **Phase 2: Create New Files** [Sequential] - Content migration
   - Task: Create core/config.py (copy from config/settings.py)
   - Task: Create core/db.py (merge database/connection.py + session.py)
   - Task: Create core/__init__.py (export public APIs)
   - Task: Create schemas/health.py (move from health/models.py)
   - Task: Create api/endpoints/health.py (move from health/endpoints.py)
   - Task: Create api/deps.py (minimal re-exports)

3. **Phase 3: Update main.py** [Single] - Application entry point
   - Task: Update imports in main.py (4 import statements)

4. **Phase 4: Update Imports** [P] - Parallel import updates
   - Task: Update middleware/error_handler.py imports
   - Task: Update tests/conftest.py imports
   - Task: Verify all test files import updates

5. **Phase 5: Verification Gates** [Sequential] - Must all pass
   - Task: Verify no old imports remain (grep checks)
   - Task: Verify new imports present (grep checks)
   - Task: Verify syntax errors (py_compile)
   - Task: Verify module imports (import tests)
   - Task: Verify application startup (main.py loads)
   - Task: Run full test suite (106 tests must pass)
   - Task: Verify coverage maintained (97%+)
   - Task: Run linting (ruff check)
   - Task: Checkpoint for rollback decision

6. **Phase 6: Cleanup** [Sequential] - After verification only
   - Task: Remove api/src/config/ directory
   - Task: Remove api/src/database/ directory
   - Task: Remove api/src/health/ directory
   - Task: Final test run validation

**Ordering Strategy**:
- Create-before-delete: All new files created before old files removed
- Verification gates: Blocking tasks between migration and cleanup
- Rollback safety: Checkpoint task before irreversible cleanup
- Parallel execution: Directory creation and import updates can parallelize
- Sequential dependencies: Phases must execute in order

**Estimated Output**: ~25 numbered, ordered tasks in tasks.md with explicit [P] markers for parallel execution and clear phase boundaries

**IMPORTANT**: This phase is executed by the /tasks command, NOT by /plan

## Phase 3+: Future Implementation
*These phases are beyond the scope of the /plan command*

**Phase 3**: Task execution (/tasks command creates tasks.md)
**Phase 4**: Implementation (execute tasks.md following constitutional principles)
**Phase 5**: Validation (run verification checklist, ensure 106 tests pass, maintain 97%+ coverage)

## Complexity Tracking
*Fill ONLY if Constitution Check has violations that must be justified*

**Status**: No constitutional violations detected

This refactoring strictly adheres to all constitutional principles:
- No new dependencies (II. Quality-First Development)
- No test modifications except imports (III. Test-Driven Implementation)
- Follows established Python conventions (V. Convention Consistency)
- No architecture pattern violations (Architecture Patterns)
- Maintains all quality gates (Quality Gates)

## Progress Tracking
*This checklist is updated during execution flow*

**Phase Status**:
- [x] Phase 0: Research complete (/plan command) - No research needed, spec comprehensive
- [x] Phase 1: Design complete (/plan command) - No data model changes, contracts preserved
- [x] Phase 2: Task planning complete (/plan command - describe approach only)
- [ ] Phase 3: Tasks generated (/tasks command)
- [ ] Phase 4: Implementation complete
- [ ] Phase 5: Validation passed

**Gate Status**:
- [x] Initial Constitution Check: PASS
- [x] Post-Design Constitution Check: PASS
- [x] All NEEDS CLARIFICATION resolved (none existed)
- [x] Complexity deviations documented (none exist)

---
*Based on Constitution v1.1.0 - See `.specify/memory/constitution.md`*
