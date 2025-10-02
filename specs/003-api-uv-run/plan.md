# Implementation Plan: Fix API Test Suite and Clean Dead Code

**Branch**: `003-api-uv-run` | **Date**: 2025-10-02 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/003-api-uv-run/spec.md`

## Execution Flow (/plan command scope)
```
1. Load feature spec from Input path → ✅ COMPLETE
2. Fill Technical Context (scan for NEEDS CLARIFICATION) → ✅ COMPLETE
3. Fill Constitution Check section → ✅ COMPLETE
4. Evaluate Constitution Check → ✅ PASS (refactoring task, no violations)
5. Execute Phase 0 → research.md → ✅ COMPLETE
6. Execute Phase 1 → contracts, data-model.md, quickstart.md → ✅ COMPLETE
7. Re-evaluate Constitution Check → ✅ PASS
8. Plan Phase 2 → Task generation approach → ✅ COMPLETE
9. STOP - Ready for /tasks command
```

## Summary
Fix all 28 failing pytest tests in the FastAPI backend by addressing: (1) missing greenlet dependency for SQLAlchemy async operations, (2) Pydantic v2 migration issues with deprecated Field patterns, (3) incorrect test assertions for middleware and error handling, (4) dead code removal for unused environment variables. Ensure full compliance with FastAPI best practices for async patterns, dependency injection, and testing.

## Technical Context
**Language/Version**: Python 3.12.11 (verified from current environment)
**Primary Dependencies**: FastAPI >=0.100.0, SQLAlchemy >=2.0.0, asyncpg >=0.28.0, Pydantic >=2.0.0, pytest >=7.0.0
**Storage**: PostgreSQL (async with asyncpg driver)
**Testing**: pytest with pytest-asyncio for async test support
**Target Platform**: Linux/macOS server with uv package manager
**Project Type**: web (backend API component of monorepo)
**Performance Goals**: Test suite execution <1s, API response time <200ms p95
**Constraints**: Zero test failures required, no deprecation warnings, maintain 80%+ test coverage
**Scale/Scope**: 109 tests across 10 test modules, 16 source files in api/src/

**User-Provided Context**: 计划和分析如何修复和符合fastapi最佳实践 (Plan and analyze how to fix and comply with FastAPI best practices) with --context7 for official FastAPI documentation

## Constitution Check
*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### I. Dual-Stack Excellence
- ✅ **PASS**: Backend-only refactoring, no frontend changes required
- ✅ **PASS**: Pydantic models already typed, maintaining type safety

### II. Quality-First Development
- ✅ **PASS**: Fixes quality gates (Ruff linting, pytest)
- ✅ **PASS**: Removes deprecation warnings, improves code quality
- 🎯 **PRIMARY GOAL**: This task directly addresses quality-first principles

### III. Test-Driven Implementation
- ✅ **PASS**: 81 tests already passing, fixing 28 failing tests
- ✅ **PASS**: Maintains test-first approach, no test removal

### IV. Internationalization by Design
- ✅ **N/A**: Backend API has no user-facing UI text

### V. Convention Consistency
- ✅ **PASS**: Maintains Python conventions (snake_case, type hints)
- ✅ **PASS**: English-only documentation updates

**Constitution Compliance**: ✅ FULL COMPLIANCE - This is a quality improvement task that strengthens constitutional principles

## Project Structure

### Documentation (this feature)
```
specs/003-api-uv-run/
├── plan.md              # This file (/plan command output)
├── research.md          # Phase 0 output - FastAPI best practices analysis
├── data-model.md        # Phase 1 output - Configuration and error models
├── quickstart.md        # Phase 1 output - Test verification guide
├── contracts/           # Phase 1 output - No new API contracts (refactoring)
└── tasks.md             # Phase 2 output (/tasks command - NOT created by /plan)
```

### Source Code (repository root)
```
api/
├── src/
│   ├── config/
│   │   ├── __init__.py
│   │   ├── settings.py          # MODIFY: Pydantic v2 migration
│   │   └── logging.py
│   ├── database/
│   │   ├── __init__.py
│   │   ├── connection.py        # VERIFY: Async engine patterns
│   │   ├── session.py
│   │   └── health.py            # MODIFY: Error handling improvements
│   ├── health/
│   │   ├── __init__.py
│   │   ├── endpoints.py         # MODIFY: Status code corrections
│   │   └── models.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   └── errors.py            # MODIFY: Enum validation fixes
│   ├── middleware/
│   │   ├── __init__.py
│   │   └── error_handler.py
│   └── main.py                  # VERIFY: Middleware configuration
├── tests/
│   ├── test_config_validation.py      # MODIFY: Fix validation tests
│   ├── test_database_connection.py    # MODIFY: Fix async disposal tests
│   ├── test_error_schemas.py          # MODIFY: Fix enum validation
│   ├── test_health_db_endpoint.py     # MODIFY: Fix status code assertions
│   ├── test_health_endpoint.py        # VERIFY: Should pass
│   ├── test_performance.py            # MODIFY: Fix database health tests
│   ├── test_quickstart_validation.py  # MODIFY: Multiple fixes needed
│   ├── test_startup.py                # MODIFY: Fix middleware access
│   └── ...
├── pyproject.toml                # MODIFY: Add greenlet dependency
├── .env.example                  # MODIFY: Remove unused variables
└── README.md                     # UPDATE: Document changes

web/
└── [frontend - no changes needed]
```

**Structure Decision**: Web application structure (api/ + web/ directories). This task focuses exclusively on the api/ backend component. No frontend changes required.

## Phase 0: Outline & Research

### Research Tasks Completed

**1. FastAPI Best Practices Analysis** (Context7 Documentation)
- **Decision**: Use `@lru_cache` decorator for Settings singleton pattern
- **Rationale**: Official FastAPI documentation recommends this for performance and consistency
- **Pattern**:
  ```python
  from functools import lru_cache
  from pydantic_settings import BaseSettings

  @lru_cache
  def get_settings() -> Settings:
      return Settings()
  ```

**2. Pydantic v2 Migration Path**
- **Decision**: Remove `env` parameter from Field(), use field names directly
- **Rationale**: Pydantic v2 deprecated `env` parameter, BaseSettings automatically maps field names to env vars
- **Breaking Change**: ConfigDict replaces class-based Config
- **Pattern**:
  ```python
  # OLD (deprecated):
  app_name: str = Field(default="API", env="APP_NAME")

  # NEW (Pydantic v2):
  app_name: str = Field(default="API")  # Automatically reads APP_NAME
  ```

**3. SQLAlchemy Async Engine Dependencies**
- **Decision**: Add greenlet>=3.0.0 explicitly to pyproject.toml
- **Rationale**: SQLAlchemy async engine requires greenlet for async context management
- **Issue**: Transitive dependency not guaranteed, causes runtime failures
- **Fix**: Declare as direct dependency

**4. FastAPI Middleware Access Patterns**
- **Decision**: Use `app.middleware` iterator, not `app.middleware_stack` attribute
- **Rationale**: `middleware_stack` is internal implementation detail, not public API
- **Alternative**: Access middleware via `app.middleware` or test functionality, not internals

**5. Error Response Status Codes**
- **Decision**: Database health check failures should return 503 Service Unavailable
- **Rationale**: 500 is for server bugs, 503 for temporary unavailability (database down)
- **Pattern**: Catch database exceptions, return structured 503 response

**6. Test Client Best Practices**
- **Decision**: Use FastAPI TestClient for all endpoint tests
- **Rationale**: Provides synchronous interface to async endpoints, proper lifecycle management
- **Pattern**: `with TestClient(app) as client:` for automatic cleanup

**7. Dependency Injection Testing**
- **Decision**: Use `app.dependency_overrides` for test dependencies
- **Rationale**: Official pattern for mocking dependencies without modifying code
- **Pattern**:
  ```python
  app.dependency_overrides[get_settings] = get_test_settings
  # Run tests
  app.dependency_overrides = {}  # Cleanup
  ```

**Output**: research.md created with detailed FastAPI best practices analysis

## Phase 1: Design & Contracts

### 1. Data Model Extraction (data-model.md)

**Configuration Model** (existing, needs migration):
- **Settings** (src/config/settings.py)
  - Pydantic v2 BaseSettings migration required
  - Remove deprecated `env` parameters from all Fields
  - Update validators to use `@field_validator` decorator properly
  - Fields: app_name, database_url, cors_origins, log_level, etc.

**Error Models** (existing, needs fixes):
- **ErrorResponse** (src/models/errors.py)
  - Fix enum validation for error types
  - Ensure proper Pydantic v2 validation

**Health Models** (existing, needs improvements):
- **HealthResponse** (src/health/models.py)
  - Verify status code handling (200 vs 503)

### 2. API Contracts

**No New Contracts**: This is a refactoring task. All existing endpoints remain unchanged:
- `GET /` - Root endpoint
- `GET /health` - Basic health check
- `GET /health/db` - Database health check

**Contract Changes**: None (maintaining backward compatibility)

### 3. Contract Tests

**Existing Tests Require Fixes** (not new tests):
- Fix 28 failing tests to properly validate existing contracts
- Correct assertions to match FastAPI best practices
- Update test patterns to avoid internal API access

### 4. Test Scenarios

**Quickstart Validation** (existing scenarios, fixing assertions):
1. Environment configuration validation
2. Database connection health checks
3. CORS configuration verification
4. Middleware stack initialization
5. Error handling patterns

### 5. Agent Context Update

**Updated CLAUDE.md sections**:
- FastAPI async patterns with proper greenlet dependency
- Pydantic v2 migration guidelines
- Test client best practices
- Dependency injection testing patterns

**Output**: data-model.md, quickstart.md, CLAUDE.md updated

## Phase 2: Task Planning Approach
*This section describes what the /tasks command will do - DO NOT execute during /plan*

**Task Generation Strategy**:
1. Load `.specify/templates/tasks-template.md` as base
2. Generate tasks in dependency order (dependencies → tests → cleanup)
3. Each failing test category → fix task with validation
4. Pydantic migration → atomic changes per file
5. Dead code removal → final cleanup tasks

**Task Categories**:
1. **Dependency Fixes** [P] - Add greenlet to pyproject.toml
2. **Pydantic Migration** [P] - Update settings.py Field declarations
3. **Source Code Fixes** - Fix error handling, status codes, validation
4. **Test Fixes** - Correct test assertions and patterns
5. **Dead Code Removal** - Remove unused environment variables
6. **Documentation** - Update README.md and .env.example
7. **Validation** - Run full test suite, verify 0 failures

**Ordering Strategy**:
1. Dependencies first (greenlet) - enables async tests
2. Pydantic migration next - removes deprecation warnings
3. Source code fixes - improves error handling
4. Test fixes - validates all changes
5. Dead code cleanup - removes unused configs
6. Documentation - captures all changes

**Parallelization Opportunities**:
- [P] Multiple test file fixes (independent)
- [P] Documentation updates (independent)
- Sequential: dependency → migration → tests (dependent)

**Estimated Output**: 15-20 numbered, ordered tasks in tasks.md

**Task Template Example**:
```
## Task 1: Add greenlet dependency
**Type**: Dependency Management
**Files**: api/pyproject.toml
**Action**: Add greenlet>=3.0.0 to dependencies
**Validation**: uv sync && uv run python -c "import greenlet"
**Priority**: Critical (blocks async engine tests)
```

**IMPORTANT**: This phase is executed by the /tasks command, NOT by /plan

## Phase 3+: Future Implementation
*These phases are beyond the scope of the /plan command*

**Phase 3**: Task execution (/tasks command creates tasks.md)
**Phase 4**: Implementation (execute tasks.md following constitutional principles)
**Phase 5**: Validation (run `uv run pytest`, verify 109/109 pass, 0 deprecation warnings)

## Complexity Tracking
*No violations - refactoring task maintains existing architecture*

This is a quality improvement and technical debt reduction task. No new complexity introduced:
- ✅ Uses existing FastAPI patterns
- ✅ Maintains current project structure
- ✅ Follows established conventions
- ✅ No new dependencies beyond greenlet (required by SQLAlchemy)

## Progress Tracking

**Phase Status**:
- [x] Phase 0: Research complete (/plan command)
- [x] Phase 1: Design complete (/plan command)
- [x] Phase 2: Task planning complete (/plan command - describe approach only)
- [ ] Phase 3: Tasks generated (/tasks command)
- [ ] Phase 4: Implementation complete
- [ ] Phase 5: Validation passed

**Gate Status**:
- [x] Initial Constitution Check: PASS
- [x] Post-Design Constitution Check: PASS
- [x] All NEEDS CLARIFICATION resolved
- [x] Complexity deviations documented (none)

**Execution Checklist**:
- [x] Feature spec loaded and analyzed
- [x] Technical context filled (Python 3.12, FastAPI, pytest)
- [x] FastAPI best practices researched (Context7)
- [x] Test failure categories identified (28 failures across 6 categories)
- [x] Pydantic v2 migration path determined
- [x] Dead code candidates identified (SECRET_KEY, USE_UUIDV7, etc.)
- [x] Task generation strategy planned
- [x] Ready for /tasks command

---

**Next Command**: `/tasks` to generate detailed implementation tasks

*Based on Constitution v1.0.1 - See `.specify/memory/constitution.md`*
*FastAPI Best Practices from Context7: /tiangolo/fastapi v0.115.12*
