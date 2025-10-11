# Tasks: Update Dify SDK Test Suite for httpx Migration

**Input**: Design documents from `/specs/006-update-api-tests/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, quickstart.md

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`
- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2)
- Include exact file paths in descriptions

## Path Conventions
- **Backend tests**: `api/tests/dify/` at repository root
- **Configuration**: `api/pyproject.toml`, `api/pytest.ini`
- All paths are absolute from repository root

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Install dependencies and configure pytest for async testing

- [x] T001 [Setup] Install pytest-httpx dependency in `api/pyproject.toml` using `uv add --dev "pytest-httpx>=0.30.0"`
- [x] T002 [Setup] Create/update `api/pytest.ini` with pytest-asyncio configuration (asyncio_mode=auto, asyncio_default_fixture_loop_scope=function)
- [x] T003 [Setup] Verify pytest discovers async tests by running `uv run pytest api/tests/dify/ --collect-only` (expect discovery errors, tests will fail until migration)

**Checkpoint**: pytest-httpx installed, pytest.ini configured for async mode

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Update conftest.py with pytest-httpx fixtures - MUST be complete before ANY test file migration

**⚠️ CRITICAL**: No test file migration can begin until this phase is complete

- [x] T004 [Foundation] Remove requests imports from `api/tests/dify/conftest.py` (lines 13, 80-83: `import requests`, `@pytest.fixture def mock_requests_request()`)
- [x] T005 [Foundation] Remove requests-based mock response fixtures from `api/tests/dify/conftest.py` (lines 35-46: `mock_successful_response`, lines 50-60: `mock_error_response`, lines 64-76: `mock_streaming_response`)
- [x] T006 [Foundation] Keep all existing sample data fixtures in `api/tests/dify/conftest.py` (mock_api_key, mock_base_url, mock_user, sample_inputs, sample_files, all ID fixtures - NO CHANGES to these)
- [x] T007 [Foundation] Add docstring to `api/tests/dify/conftest.py` explaining httpx_mock fixture is auto-provided by pytest-httpx (no manual fixture definition needed)

**Checkpoint**: conftest.py updated with pytest-httpx patterns, all sample data fixtures preserved

---

## Phase 3: User Story 1 - Developer runs existing tests after SDK update (Priority: P1) 🎯 MVP

**Goal**: All 6 test files pass with 100% success rate using httpx.AsyncClient async patterns

**Independent Test**: Run `cd api && uv run pytest tests/dify/ -v` and verify all tests pass with httpx.AsyncClient mocking

### Implementation for User Story 1

#### T008-T013: Migrate test_dify_client.py (Base Client - Start Here)

- [x] T008 [P] [US1] Update imports in `api/tests/dify/test_dify_client.py`: Remove `from unittest.mock import Mock`, add `from pytest_httpx import HTTPXMock`
- [x] T009 [P] [US1] Convert all test methods to async in `api/tests/dify/test_dify_client.py`: Change `def test_*` to `async def test_*` (approximately 5-8 test methods)
- [x] T010 [US1] Replace request mocking in `api/tests/dify/test_dify_client.py`: Replace `mock_requests_request` fixture parameter with `httpx_mock: HTTPXMock`
- [x] T011 [US1] Update response configuration in `api/tests/dify/test_dify_client.py`: Replace `mock_requests_request.return_value = mock_response` with `httpx_mock.add_response(json={...}, status_code=200)`
- [x] T012 [US1] Add await keywords in `api/tests/dify/test_dify_client.py`: Add `await` before all client method calls that make HTTP requests
- [x] T013 [US1] Update assertions in `api/tests/dify/test_dify_client.py`: Replace `mock_requests_request.assert_called_once()` with `requests = httpx_mock.get_requests(); assert len(requests) == 1`
- [x] T014 [US1] Run tests for test_dify_client.py only: Execute `cd api && uv run pytest tests/dify/test_dify_client.py -v` and verify 100% pass rate

#### T015-T020: Migrate test_chat_client.py (Chat Operations)

- [ ] T015 [P] [US1] Update imports in `api/tests/dify/test_chat_client.py`: Remove Mock imports, add HTTPXMock import
- [ ] T016 [P] [US1] Convert all test methods to async in `api/tests/dify/test_chat_client.py`: Change `def test_*` to `async def test_*` (approximately 15-20 test methods including annotation tests)
- [ ] T017 [US1] Replace request mocking in `api/tests/dify/test_chat_client.py`: Update all test fixtures to use httpx_mock
- [ ] T018 [US1] Configure pytest-httpx responses in `api/tests/dify/test_chat_client.py`: Add httpx_mock.add_response() calls with appropriate URLs, methods, and response bodies for chat operations
- [ ] T019 [US1] Add await keywords and update assertions in `api/tests/dify/test_chat_client.py`: Update all HTTP client calls and verification logic
- [ ] T020 [US1] Run tests for test_chat_client.py only: Execute `cd api && uv run pytest tests/dify/test_chat_client.py -v` and verify 100% pass rate

#### T021-T026: Migrate test_completion_client.py (Completion Operations)

- [ ] T021 [P] [US1] Update imports in `api/tests/dify/test_completion_client.py`: Remove Mock imports, add HTTPXMock import
- [ ] T022 [P] [US1] Convert all test methods to async in `api/tests/dify/test_completion_client.py`: Change `def test_*` to `async def test_*`
- [ ] T023 [US1] Replace request mocking in `api/tests/dify/test_completion_client.py`: Update all test fixtures to use httpx_mock
- [ ] T024 [US1] Configure pytest-httpx responses in `api/tests/dify/test_completion_client.py`: Add httpx_mock.add_response() for completion endpoints
- [ ] T025 [US1] Add await keywords and update assertions in `api/tests/dify/test_completion_client.py`: Update all client calls and assertions
- [ ] T026 [US1] Run tests for test_completion_client.py only: Execute `cd api && uv run pytest tests/dify/test_completion_client.py -v` and verify 100% pass rate

#### T027-T032: Migrate test_workflow_client.py (Workflow Operations)

- [ ] T027 [P] [US1] Update imports in `api/tests/dify/test_workflow_client.py`: Remove Mock imports, add HTTPXMock import
- [ ] T028 [P] [US1] Convert all test methods to async in `api/tests/dify/test_workflow_client.py`: Change `def test_*` to `async def test_*` (approximately 10-12 test methods)
- [ ] T029 [US1] Replace request mocking in `api/tests/dify/test_workflow_client.py`: Update all test fixtures to use httpx_mock
- [ ] T030 [US1] Configure pytest-httpx responses in `api/tests/dify/test_workflow_client.py`: Add httpx_mock.add_response() for workflow endpoints including logs with pagination
- [ ] T031 [US1] Add await keywords and update assertions in `api/tests/dify/test_workflow_client.py`: Update all client calls and verification logic
- [ ] T032 [US1] Run tests for test_workflow_client.py only: Execute `cd api && uv run pytest tests/dify/test_workflow_client.py -v` and verify 100% pass rate

#### T033-T038: Migrate test_knowledge_base_client.py (Knowledge Base Operations)

- [ ] T033 [P] [US1] Update imports in `api/tests/dify/test_knowledge_base_client.py`: Remove Mock imports, add HTTPXMock import
- [ ] T034 [P] [US1] Convert all test methods to async in `api/tests/dify/test_knowledge_base_client.py`: Change `def test_*` to `async def test_*`
- [ ] T035 [US1] Replace request mocking in `api/tests/dify/test_knowledge_base_client.py`: Update all test fixtures to use httpx_mock
- [ ] T036 [US1] Configure pytest-httpx responses in `api/tests/dify/test_knowledge_base_client.py`: Add httpx_mock.add_response() for knowledge base endpoints including document and segment operations
- [ ] T037 [US1] Add await keywords and update assertions in `api/tests/dify/test_knowledge_base_client.py`: Update all client calls and assertions
- [ ] T038 [US1] Run tests for test_knowledge_base_client.py only: Execute `cd api && uv run pytest tests/dify/test_knowledge_base_client.py -v` and verify 100% pass rate

#### T039-T044: Migrate test_workspace_client.py (Workspace Operations)

- [ ] T039 [P] [US1] Update imports in `api/tests/dify/test_workspace_client.py`: Remove Mock imports, add HTTPXMock import
- [ ] T040 [P] [US1] Convert all test methods to async in `api/tests/dify/test_workspace_client.py`: Change `def test_*` to `async def test_*`
- [ ] T041 [US1] Replace request mocking in `api/tests/dify/test_workspace_client.py`: Update all test fixtures to use httpx_mock
- [ ] T042 [US1] Configure pytest-httpx responses in `api/tests/dify/test_workspace_client.py`: Add httpx_mock.add_response() for workspace endpoints
- [ ] T043 [US1] Add await keywords and update assertions in `api/tests/dify/test_workspace_client.py`: Update all client calls and verification logic
- [ ] T044 [US1] Run tests for test_workspace_client.py only: Execute `cd api && uv run pytest tests/dify/test_workspace_client.py -v` and verify 100% pass rate

#### T045-T047: Final Validation for User Story 1

- [ ] T045 [US1] Run complete test suite: Execute `cd api && uv run pytest tests/dify/ -v` and verify ALL tests pass (100% success rate)
- [ ] T046 [US1] Verify coverage maintained: Execute `cd api && uv run pytest tests/dify/ --cov=tests/dify --cov-report=term-missing` and confirm ≥80% coverage
- [ ] T047 [US1] Check for async-related errors: Review pytest output and confirm zero event loop errors, no missing await keywords, no synchronous Mock usage

**Checkpoint**: User Story 1 complete - All 6 test files pass with httpx.AsyncClient, ≥80% coverage, no async errors

---

## Phase 4: User Story 2 - Developer adds new Dify SDK integration tests (Priority: P2)

**Goal**: Provide clear async test patterns and fixtures for future test development

**Independent Test**: Create a new test file following migrated patterns and verify it works correctly with httpx.AsyncClient mocking

### Implementation for User Story 2

- [ ] T048 [P] [US2] Add inline documentation to `api/tests/dify/conftest.py`: Document httpx_mock fixture usage, pytest-asyncio auto mode behavior, and example test patterns
- [ ] T049 [P] [US2] Add inline code examples to one migrated test file (recommend `api/tests/dify/test_dify_client.py`): Add comments showing common patterns (simple GET, POST with body, error handling, streaming)
- [ ] T050 [US2] Create reference example test in `api/tests/dify/test_dify_client.py`: Add a comprehensive example test method demonstrating all pytest-httpx features (multiple requests, assertions, error responses)
- [ ] T051 [US2] Verify documentation completeness: Review all 7 test files and conftest.py, ensure async/await patterns are consistent and easily observable for future reference

**Checkpoint**: User Story 2 complete - Test patterns documented, examples provided for future test development

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Final quality checks and cleanup across all migrated tests

- [ ] T052 [P] [Polish] Run linting: Execute `cd api && uv run ruff check tests/dify/ --fix` and ensure all code passes Ruff standards
- [ ] T053 [P] [Polish] Verify type hints: Ensure all fixture signatures have proper type annotations (already present in conftest.py, verify in migrated tests)
- [ ] T054 [Polish] Performance check: Run `cd api && uv run pytest tests/dify/ --durations=10` and verify execution time is within 10% of baseline (document baseline first)
- [ ] T055 [Polish] Final test run with verbose output: Execute `cd api && uv run pytest tests/dify/ -v --tb=short` and confirm zero failures, zero warnings
- [ ] T056 [Polish] Update CLAUDE.md if needed: Verify agent context file reflects pytest-httpx usage patterns (already updated by /speckit.plan)

**Checkpoint**: All quality gates passed, test suite ready for production use

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup (Phase 1) completion - BLOCKS all test file migrations
- **User Story 1 (Phase 3)**: Depends on Foundational (Phase 2) completion
  - Test files can be migrated in parallel (T008-T044 across 6 files)
  - Or sequentially: test_dify_client.py → test_chat_client.py → test_completion_client.py → test_workflow_client.py → test_knowledge_base_client.py → test_workspace_client.py
- **User Story 2 (Phase 4)**: Depends on User Story 1 completion (needs migrated tests to document)
- **Polish (Phase 5)**: Depends on User Story 2 completion

### Within User Story 1 (Test File Migration Pattern)

Each test file follows this pattern:
1. Update imports (can run in parallel across files)
2. Convert to async (can run in parallel across files)
3. Replace mocking (sequential within same file)
4. Configure responses (sequential within same file)
5. Add await & update assertions (sequential within same file)
6. Run tests for that file only (validation step)

### Parallel Opportunities

#### Phase 1 (Setup):
- T001, T002, T003 are sequential (dependency chain)

#### Phase 2 (Foundational):
- T004, T005 can run in parallel (different parts of conftest.py)
- T006, T007 follow after T004/T005

#### Phase 3 (User Story 1) - Maximum Parallelism:

**Option A: Parallel by test file (6 parallel tracks)**
```bash
# Launch all 6 test file migrations simultaneously:
Track 1: T008-T014 (test_dify_client.py)
Track 2: T015-T020 (test_chat_client.py)
Track 3: T021-T026 (test_completion_client.py)
Track 4: T027-T032 (test_workflow_client.py)
Track 5: T033-T038 (test_knowledge_base_client.py)
Track 6: T039-T044 (test_workspace_client.py)
```

**Option B: Parallel by migration step (within each file)**
```bash
# For each file, these can run in parallel:
- T008, T009 (imports + convert to async) [P]
- Then T010-T013 sequentially (same file edits)

# Repeat pattern for each test file
```

#### Phase 4 (User Story 2):
- T048, T049, T050 can run in parallel (different documentation locations)
- T051 follows after documentation complete

#### Phase 5 (Polish):
- T052, T053 can run in parallel (independent quality checks)
- T054, T055, T056 are sequential (depend on prior checks)

---

## Parallel Example: User Story 1 (Maximum Efficiency)

```bash
# After Phase 2 (Foundational) completes, launch all 6 test file migrations:

# Developer A (or Agent 1):
Task T008-T014: Migrate test_dify_client.py completely

# Developer B (or Agent 2):
Task T015-T020: Migrate test_chat_client.py completely

# Developer C (or Agent 3):
Task T021-T026: Migrate test_completion_client.py completely

# Developer D (or Agent 4):
Task T027-T032: Migrate test_workflow_client.py completely

# Developer E (or Agent 5):
Task T033-T038: Migrate test_knowledge_base_client.py completely

# Developer F (or Agent 6):
Task T039-T044: Migrate test_workspace_client.py completely

# Then converge for validation:
Task T045-T047: Final validation (single developer or automated CI)
```

---

## Implementation Strategy

### MVP First (User Story 1 Only - Restore Test Functionality)

1. **Complete Phase 1: Setup** (T001-T003) - ~15 minutes
   - Install pytest-httpx
   - Configure pytest.ini
   - Verify test discovery

2. **Complete Phase 2: Foundational** (T004-T007) - ~30 minutes
   - Update conftest.py with pytest-httpx patterns
   - Remove requests-based fixtures
   - Preserve sample data fixtures

3. **Complete Phase 3: User Story 1** (T008-T047) - ~10-12 hours
   - Migrate all 6 test files to async patterns
   - Run tests incrementally after each file
   - Final validation with coverage check
   - **STOP and VALIDATE**: All tests pass, ≥80% coverage

4. **Result**: Test suite fully functional with httpx.AsyncClient, ready for production use

### Incremental Delivery (Add Documentation)

1. Complete MVP (Phases 1-3) → Tests working ✅
2. **Add Phase 4: User Story 2** (T048-T051) - ~2 hours
   - Document patterns for future developers
   - Add inline examples
   - Create reference tests
3. **Result**: Tests working + documented patterns for future development ✅

### Full Delivery (Production-Ready)

1. Complete MVP + Documentation (Phases 1-4)
2. **Add Phase 5: Polish** (T052-T056) - ~2 hours
   - Linting, type checking
   - Performance validation
   - Final quality gates
3. **Result**: Production-ready async test suite with documentation ✅

### Parallel Team Strategy

With 6 developers available:

1. **Phase 1 & 2**: Team works together (1 hour total)
2. **Phase 3 (User Story 1)**: Split by test file
   - Each developer takes 1 test file (T008-T014, T015-T020, etc.)
   - All work in parallel (~2 hours each = 2 hours total wall time)
   - Converge for final validation (T045-T047)
3. **Phase 4 & 5**: Team works together or splits by tasks (2-3 hours)

**Total wall time with 6 developers**: ~5-6 hours (vs 15-18 hours sequential)

---

## Task Estimation Summary

| Phase | Task Count | Estimated Time | Can Parallelize? |
|-------|------------|----------------|------------------|
| Phase 1: Setup | 3 | 15 min | No (sequential) |
| Phase 2: Foundational | 4 | 30 min | Partial (2 parallel tracks) |
| Phase 3: User Story 1 | 40 | 10-12 hours | Yes (6 parallel tracks) |
| Phase 4: User Story 2 | 4 | 2 hours | Partial (3 parallel tracks) |
| Phase 5: Polish | 5 | 2 hours | Partial (2 parallel tracks) |
| **TOTAL** | **56 tasks** | **15-17 hours** | **6-way parallelism max** |

### MVP Scope (Recommended First Delivery)
- **Phases**: 1, 2, 3 only
- **Tasks**: T001-T047 (47 tasks)
- **Time**: 12-14 hours sequential, 3-4 hours with 6 developers
- **Outcome**: All tests pass with httpx.AsyncClient ✅

---

## Notes

- **[P] markers**: Tasks marked [P] operate on different files and can run in parallel
- **[Story] labels**: US1 = User Story 1 (test functionality), US2 = User Story 2 (documentation)
- **Independent testing**: Each test file can be validated independently during migration
- **Rollback strategy**: Git commit after each test file migration (T014, T020, T026, etc.)
- **Quality gates**: Run tests after each file, run coverage after full suite
- **No tests requested**: This feature IS the test migration, so no additional test generation needed
- **Pattern consistency**: Follow quickstart.md for migration patterns across all 6 test files
