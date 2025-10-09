# Tasks: Static Type Checking Integration

**Input**: Design documents from `/specs/005-integrate-mypy-for/`
**Prerequisites**: plan.md, research.md, data-model.md, contracts/type-checking-service.yaml

## Execution Summary

This task list implements mypy static type checking integration for the Python backend following TDD principles. All contract tests must be written and failing before implementation begins.

**File Inventory** (from glob):
- 15 Python source files across api/src/
- Modules: api/, core/, middleware/, models/, schemas/
- Test structure: api/tests/ (to be created)

## Format: `[ID] [P?] Description`
- **[P]**: Can run in parallel (different files, no dependencies)
- Exact file paths included in all task descriptions

---

## Phase 3.1: Setup & Dependencies

- [ ] **T001** Add mypy to dev dependencies in `api/pyproject.toml`
  - Add `"mypy>=1.8.0"` to `[dependency-groups].dev` array
  - Run `cd api && uv sync --dev` to install
  - Verify: `uv run mypy --version` shows 1.8.0+

- [ ] **T002** Create mypy configuration section in `api/pyproject.toml`
  - Add complete `[tool.mypy]` section per data-model.md specification
  - Include: strict mode, python_version, plugins, mypy_path, packages, exclude
  - Add module overrides for migrations and asyncpg
  - Verify: Configuration matches data-model.md exactly

- [ ] **T003** Add `.mypy_cache/` to `.gitignore`
  - Add line: `api/.mypy_cache/` (or `.mypy_cache/` if global)
  - Verify: Pattern excludes cache directory from git tracking

---

## Phase 3.2: Contract Tests (TDD) ⚠️ MUST COMPLETE BEFORE 3.3

**CRITICAL: These tests MUST be written and MUST FAIL before ANY implementation**

- [ ] **T004 [P]** Contract test: mypy installation in `api/tests/test_type_checking.py`
  - Create test file with `test_mypy_installed()` function
  - Assert: `subprocess.run(["uv", "run", "mypy", "--version"])` succeeds
  - Assert: Output contains "mypy" and version >= 1.8.0
  - Expected: FAIL (mypy not configured yet)

- [ ] **T005 [P]** Contract test: configuration exists in `api/tests/test_type_checking.py`
  - Add `test_mypy_config_exists()` function
  - Read `pyproject.toml`, parse TOML
  - Assert: `[tool.mypy]` section exists
  - Assert: Required fields present (strict, plugins, python_version, etc.)
  - Expected: PASS (T002 completed)

- [ ] **T006 [P]** Contract test: strict mode enabled in `api/tests/test_type_checking.py`
  - Add `test_strict_mode_enabled()` function
  - Parse pyproject.toml `[tool.mypy]` section
  - Assert: `strict = true` is set
  - Expected: PASS (T002 completed)

- [ ] **T007 [P]** Contract test: Pydantic plugin configured in `api/tests/test_type_checking.py`
  - Add `test_pydantic_plugin_configured()` function
  - Parse pyproject.toml `[tool.mypy]` section
  - Assert: `plugins` list contains "pydantic.mypy"
  - Expected: PASS (T002 completed)

- [ ] **T008 [P]** Contract test: migrations excluded in `api/tests/test_type_checking.py`
  - Add `test_migrations_excluded()` function
  - Parse pyproject.toml `[[tool.mypy.overrides]]` sections
  - Assert: Override exists for `module = "migrations.*"` with `ignore_errors = true`
  - Expected: PASS (T002 completed)

- [ ] **T009 [P]** Contract test: mypy execution in `api/tests/test_type_checking.py`
  - Add `test_mypy_runs_successfully()` function
  - Run: `subprocess.run(["uv", "run", "mypy", "."], cwd="api")`
  - Assert: Exit code is 0 or 1 (not 2 - configuration error)
  - Expected: FAIL initially (type errors exist), PASS after fixes

- [ ] **T010 [P]** Contract test: cache creation in `api/tests/test_type_checking.py`
  - Add `test_mypy_cache_created()` function
  - Delete `.mypy_cache/` if exists
  - Run mypy: `subprocess.run(["uv", "run", "mypy", "."], cwd="api")`
  - Assert: `api/.mypy_cache/` directory exists
  - Assert: Contains `3.12/` subdirectory
  - Expected: FAIL (mypy not run yet), PASS after T009

- [ ] **T011 [P]** Contract test: type error detection in `api/tests/test_type_checking.py`
  - Add `test_type_error_detection()` function
  - Create temp file with intentional type error: `def f() -> int: return "str"`
  - Run mypy on temp file
  - Assert: Exit code 1, error message contains "return-value" error code
  - Clean up temp file
  - Expected: PASS after mypy configured

---

## Phase 3.3: Initial Type Check & Error Documentation

- [ ] **T012** Run mypy on codebase and document errors
  - Execute: `cd api && uv run mypy .`
  - Capture all type errors to `specs/005-integrate-mypy-for/initial-errors.md`
  - Categorize errors by file/module
  - Count errors per file for tracking progress
  - Expected: Multiple type errors (no fixes yet)

---

## Phase 3.4: Fix Type Errors - Core Module

**Dependencies**: T012 complete (error inventory)

- [ ] **T013 [P]** Fix type errors in `api/src/core/config.py`
  - Add missing type annotations for all functions/methods
  - Ensure Settings class fields have proper types
  - Add return type annotations
  - Verify: `uv run mypy src/core/config.py` passes

- [ ] **T014 [P]** Fix type errors in `api/src/core/db.py`
  - Add type annotations for async functions
  - Type AsyncEngine, AsyncSession correctly
  - Add return types for get_session(), get_db()
  - Handle Optional types for nullable returns
  - Verify: `uv run mypy src/core/db.py` passes

- [ ] **T015 [P]** Fix type errors in `api/src/core/__init__.py`
  - Add type annotations for any exported functions
  - Ensure proper re-export typing if needed
  - Verify: `uv run mypy src/core/__init__.py` passes

---

## Phase 3.5: Fix Type Errors - Models Module

**Dependencies**: T012 complete

- [ ] **T016 [P]** Fix type errors in `api/src/models/base.py`
  - Add type annotations for Base class
  - Ensure SQLAlchemy declarative base properly typed
  - Add annotations for metadata, __tablename__ if present
  - Verify: `uv run mypy src/models/base.py` passes

- [ ] **T017 [P]** Fix type errors in `api/src/models/errors.py`
  - Add type annotations for all exception classes
  - Type __init__ methods with proper parameter types
  - Add return type annotations (should be None for __init__)
  - Verify: `uv run mypy src/models/errors.py` passes

- [ ] **T018 [P]** Fix type errors in `api/src/models/__init__.py`
  - Add type annotations for exports
  - Ensure re-exports properly typed
  - Verify: `uv run mypy src/models/__init__.py` passes

---

## Phase 3.6: Fix Type Errors - Schemas Module

**Dependencies**: T012 complete

- [ ] **T019 [P]** Fix type errors in `api/src/schemas/health.py`
  - Ensure Pydantic model fields have proper type annotations
  - Add return types for any methods
  - Verify Pydantic plugin correctly infers types
  - Verify: `uv run mypy src/schemas/health.py` passes

- [ ] **T020 [P]** Fix type errors in `api/src/schemas/__init__.py`
  - Add type annotations for schema exports
  - Verify: `uv run mypy src/schemas/__init__.py` passes

---

## Phase 3.7: Fix Type Errors - API Module

**Dependencies**: T012 complete, T013-T020 recommended (dependencies typed)

- [ ] **T021 [P]** Fix type errors in `api/src/api/deps.py`
  - Add type annotations for FastAPI dependencies
  - Type async generator functions correctly (AsyncIterator)
  - Add return types for all dependency functions
  - Verify: `uv run mypy src/api/deps.py` passes

- [ ] **T022 [P]** Fix type errors in `api/src/api/endpoints/health.py`
  - Add type annotations for endpoint functions
  - Ensure FastAPI route decorators properly typed
  - Add return type annotations (should match response_model)
  - Type async functions correctly
  - Verify: `uv run mypy src/api/endpoints/health.py` passes

- [ ] **T023 [P]** Fix type errors in `api/src/api/endpoints/__init__.py`
  - Add type annotations for router exports
  - Verify: `uv run mypy src/api/endpoints/__init__.py` passes

- [ ] **T024 [P]** Fix type errors in `api/src/api/__init__.py`
  - Add type annotations for API exports
  - Verify: `uv run mypy src/api/__init__.py` passes

---

## Phase 3.8: Fix Type Errors - Middleware Module

**Dependencies**: T012 complete

- [ ] **T025 [P]** Fix type errors in `api/src/middleware/error_handler.py`
  - Add type annotations for middleware functions
  - Type FastAPI Request, Response correctly
  - Add return type annotations for all functions
  - Handle Callable types for next handlers
  - Verify: `uv run mypy src/middleware/error_handler.py` passes

- [ ] **T026 [P]** Fix type errors in `api/src/middleware/__init__.py`
  - Add type annotations for middleware exports
  - Verify: `uv run mypy src/middleware/__init__.py` passes

---

## Phase 3.9: Fix Type Errors - Main Application

**Dependencies**: T013-T026 complete (all modules typed)

- [ ] **T027** Fix type errors in `api/src/main.py`
  - Add type annotations for app initialization
  - Type FastAPI app instance correctly
  - Add return types for lifespan events if present
  - Type middleware registration functions
  - Verify: `uv run mypy src/main.py` passes

---

## Phase 3.10: Verify All Contract Tests Pass

**Dependencies**: T004-T011 (tests written), T013-T027 (implementation complete)

- [ ] **T028** Run all contract tests and verify they pass
  - Execute: `cd api && uv run pytest tests/test_type_checking.py -v`
  - Expected: All 8 contract tests PASS
  - If failures: Debug and fix until all pass
  - Document: Record test output in task completion notes

---

## Phase 3.11: Full Codebase Type Check

**Dependencies**: T013-T027 (all type errors fixed)

- [ ] **T029** Run mypy on entire codebase and verify no errors
  - Execute: `cd api && uv run mypy .`
  - Expected: "Success: no issues found in N source files"
  - If errors remain: Fix remaining issues
  - Document: Record number of files checked

---

## Phase 3.12: Pre-commit Hook Integration

**Dependencies**: T029 (mypy passes on codebase)

- [ ] **T030** Update pre-commit hook in `.husky/pre-commit`
  - Add mypy check after Ruff check for api/ workspace
  - Implementation:
    ```bash
    if [ -n "$API_CHANGES" ]; then
      echo "🔎 Running type checker..."
      cd api && uv run mypy . || exit 1
      cd ..
    fi
    ```
  - Maintain workspace detection pattern
  - Ensure mypy runs only when api/ has changes

- [ ] **T031** Test pre-commit hook with intentional type error
  - Create temp file: `api/src/test_hook.py` with type error
  - Stage file: `git add api/src/test_hook.py`
  - Attempt commit: Should fail with mypy error
  - Fix error and retry: Should succeed
  - Clean up: `rm api/src/test_hook.py`
  - Verify: Hook correctly blocks commits with type errors

---

## Phase 3.13: Performance Validation

**Dependencies**: T029 (mypy configured and passing)

- [ ] **T032** Benchmark mypy performance
  - Measure cold cache: `rm -rf api/.mypy_cache && time (cd api && uv run mypy .)`
  - Record time - should be <30s for ~15 files
  - Measure warm cache: `time (cd api && uv run mypy .)`
  - Record time - should be <5s
  - Calculate speedup factor - should be >5x
  - Document: Record benchmarks in completion notes
  - Verify: Performance meets SLAs from plan.md

---

## Phase 3.14: Quickstart Validation

**Dependencies**: T001-T032 complete (full integration)

- [ ] **T033** Execute quickstart.md validation guide
  - Follow all 11 validation phases in `specs/005-integrate-mypy-for/quickstart.md`
  - Complete all phase checklists
  - Document any deviations or issues
  - Expected: All phases pass, all checklists complete
  - Sign-off: Mark quickstart as validated

---

## Phase 3.15: Polish & Documentation

**Dependencies**: T033 (validation complete)

- [ ] **T034 [P]** Update CLAUDE.md with mypy context
  - Run: `.specify/scripts/bash/update-agent-context.sh claude`
  - Verify: CLAUDE.md includes mypy configuration details
  - Review: Ensure context is accurate and helpful

- [ ] **T035 [P]** Document mypy integration in project documentation
  - Add section to `api/README.md` (if exists) or create documentation
  - Include: Installation, configuration, running mypy, troubleshooting
  - Document: Pre-commit hook behavior
  - Document: Performance characteristics

- [ ] **T036 [P]** Create initial-errors.md comparison document
  - Compare initial errors (T012) with final state (T029)
  - Document: Number of errors fixed per module
  - Document: Total files checked, total errors fixed
  - Include: Before/after metrics

---

## Dependencies Graph

```
Setup Phase (T001-T003)
  ↓
Contract Tests (T004-T011) [All Parallel]
  ↓
Error Documentation (T012)
  ↓
Type Fixes (T013-T027) [Parallel within modules, sequential for dependencies]
  ├─ Core (T013-T015) [P]
  ├─ Models (T016-T018) [P]
  ├─ Schemas (T019-T020) [P]
  ├─ API (T021-T024) [P after Core/Models/Schemas]
  ├─ Middleware (T025-T026) [P]
  └─ Main (T027) [After all modules]
  ↓
Verification (T028-T029)
  ↓
Integration (T030-T031)
  ↓
Performance (T032)
  ↓
Validation (T033)
  ↓
Polish (T034-T036) [All Parallel]
```

---

## Parallel Execution Examples

### Example 1: Contract Tests (T004-T011)
All contract test functions can be written in parallel since they're different functions in the same file:

```bash
# Write all test functions concurrently
# Each developer/agent takes different test functions
# Then combine into single test_type_checking.py file
```

### Example 2: Core Module Fixes (T013-T015)
Different files, can run in parallel:

```bash
# Terminal 1:
cd api && uv run mypy src/core/config.py

# Terminal 2:
cd api && uv run mypy src/core/db.py

# Terminal 3:
cd api && uv run mypy src/core/__init__.py
```

### Example 3: Module-level Parallelization
Fix type errors across different modules in parallel:

```bash
# Agent 1: Core module (T013-T015)
# Agent 2: Models module (T016-T018)
# Agent 3: Schemas module (T019-T020)
# Agent 4: Middleware module (T025-T026)
```

---

## Task Completion Tracking

**Setup**: 3 tasks
**Contract Tests**: 8 tasks
**Error Documentation**: 1 task
**Type Fixes**: 15 tasks
**Verification**: 2 tasks
**Integration**: 2 tasks
**Performance**: 1 task
**Validation**: 1 task
**Polish**: 3 tasks

**Total**: 36 tasks

**Estimated Time**:
- Setup: 30 minutes
- Contract Tests: 2 hours
- Type Fixes: 4-6 hours (depends on error count)
- Integration: 1 hour
- Validation: 1 hour
- Polish: 1 hour

**Total Estimated**: 9-11 hours

---

## Validation Checklist

*GATE: All items must be checked before feature is complete*

- [ ] All 36 tasks completed
- [ ] All contract tests pass (T028)
- [ ] Mypy runs without errors on full codebase (T029)
- [ ] Pre-commit hook blocks type errors (T031)
- [ ] Performance meets SLAs: <5s incremental, <30s full (T032)
- [ ] Quickstart validation complete (T033)
- [ ] Documentation updated (T034-T035)
- [ ] `.mypy_cache/` in .gitignore (T003)
- [ ] All configuration matches data-model.md (T002)
- [ ] All Python files have type annotations
- [ ] Strict mode enforced (no untyped code)
- [ ] Pydantic plugin functioning correctly
- [ ] Async patterns correctly type-checked
- [ ] Migration files excluded from checking

---

## Notes

- **TDD Compliance**: Contract tests (T004-T011) MUST be written before implementation begins
- **Parallel Execution**: Tasks marked [P] can run concurrently
- **File Independence**: Tasks on different files are inherently parallelizable
- **Dependencies**: Follow dependency graph strictly - don't skip ahead
- **Commit Strategy**: Commit after each completed task or logical group
- **Error Handling**: If T029 shows errors, fix them before proceeding
- **Performance**: If T032 fails benchmarks, investigate caching issues

---

## Success Criteria

✅ **Phase 3 Complete** when:
1. All 36 tasks checked off
2. Mypy type checking integrated and passing
3. Pre-commit hook functioning
4. Performance goals met
5. All documentation updated
6. Quickstart validation passed

This marks the completion of Phase 3 (Implementation) in the implementation plan.
