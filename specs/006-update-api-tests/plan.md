# Implementation Plan: Update Dify SDK Test Suite for httpx Migration

**Branch**: `006-update-api-tests` | **Date**: 2025-10-11 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/006-update-api-tests/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Migrate the Dify SDK test suite from `requests`-based mocking to `httpx.AsyncClient`-based async testing patterns. All seven test files (conftest.py + 6 client test files) must be converted to use async/await patterns with pytest-asyncio, fixture-based async context manager mocks, and proper httpx.Response mocking. The SDK has been upgraded from version 0.1.14 (requests) to 0.1.15 (httpx), requiring comprehensive test infrastructure updates while maintaining 100% backward compatibility with existing test logic.

## Technical Context

**Language/Version**: Python 3.12+
**Primary Dependencies**: pytest, pytest-asyncio, httpx, dify-python-sdk==0.1.15, unittest.mock (AsyncMock)
**Storage**: N/A (test-only changes)
**Testing**: pytest with pytest-asyncio auto mode configured in pytest.ini
**Target Platform**: Development/CI environments (backend test suite)
**Project Type**: Backend test suite migration (monorepo api/ directory)
**Performance Goals**: Test execution time within 10% of baseline, 100% test pass rate
**Constraints**: Minimum 80% code coverage, zero async-related errors, maintain backward compatibility with test logic
**Scale/Scope**: 7 test files (~650 lines), fixture-based mocking, async conversion of all test methods

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### ✅ I. Dual-Stack Excellence
- **Status**: N/A - Test-only changes (no frontend/backend API modifications)
- **Assessment**: Constitutional principle does not apply to isolated test infrastructure migration

### ✅ II. Quality-First Development
- **Status**: PASS
- **Assessment**: Migration maintains Python type hints, follows Ruff linting standards (120 char line length), preserves test quality requirements
- **Evidence**: FR-009 requires 100% backward compatibility with test logic, SC-003 maintains ≥80% coverage

### ✅ III. Test-Driven Implementation
- **Status**: PASS
- **Assessment**: Migration enhances test infrastructure by converting to modern async patterns
- **Evidence**:
  - All tests remain in `api/tests/dify/` directory (proper organization maintained)
  - Test isolation preserved with fixture-based mocking
  - Minimum 80% coverage requirement enforced (SC-003)
- **Action**: No changes to test organization or file structure required

### ✅ IV. Internationalization by Design
- **Status**: N/A - Test infrastructure only (no user-facing text)
- **Assessment**: Constitutional principle does not apply to test suite migration

### ✅ V. Convention Consistency
- **Status**: PASS
- **Assessment**:
  - Python naming conventions maintained (snake_case for functions/variables)
  - Test file naming follows existing patterns (test_*.py)
  - Code comments in English only (minimal and purposeful)
- **Evidence**: FR-009 ensures backward compatibility preserves existing naming patterns

### ✅ VI. Professional Communication Standards
- **Status**: PASS with requirements
- **Assessment**:
  - All async/await patterns follow Python best practices
  - No console output or debugging artifacts in test code
  - Proper exception handling with specific httpx exceptions (FR-007)
- **Action**: Remove any existing `print()` or debugging statements during migration

### Overall Gate Status: ✅ PASS
No constitutional violations. Proceed to Phase 0 research.

## Project Structure

### Documentation (this feature)

```
specs/006-update-api-tests/
├── spec.md              # Feature specification
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command) - N/A for this feature
├── checklists/          # Quality validation checklists
│   └── requirements.md  # Specification quality checklist
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```
api/
├── tests/
│   └── dify/                           # Target test directory (all changes here)
│       ├── conftest.py                 # Shared async fixtures (UPDATE)
│       ├── test_chat_client.py         # Chat API tests (CONVERT TO ASYNC)
│       ├── test_completion_client.py   # Completion API tests (CONVERT TO ASYNC)
│       ├── test_dify_client.py         # Base client tests (CONVERT TO ASYNC)
│       ├── test_knowledge_base_client.py # Knowledge base tests (CONVERT TO ASYNC)
│       ├── test_workflow_client.py     # Workflow tests (CONVERT TO ASYNC)
│       └── test_workspace_client.py    # Workspace tests (CONVERT TO ASYNC)
├── pyproject.toml                      # Dependencies (ADD pytest-asyncio)
└── pytest.ini                          # Pytest configuration (CREATE/UPDATE for asyncio_mode = auto)
```

**Structure Decision**: Monorepo backend test suite structure. All changes isolated to `api/tests/dify/` directory with pytest configuration updates in `api/pytest.ini`. No production code changes required (test infrastructure only).

## Complexity Tracking

*Fill ONLY if Constitution Check has violations that must be justified*

No constitutional violations detected. This section intentionally left empty.

---

## Phase 0: Research ✅ COMPLETE

**Output**: [research.md](./research.md)

**Key Findings**:
- **Technology Decision**: Use pytest-httpx library (cleaner than manual AsyncMock patterns)
- **Configuration**: pytest-asyncio auto mode (zero-decorator pattern)
- **Response Behavior**: httpx.Response data methods are synchronous (.json(), .text)
- **Async Methods**: Only client methods and streaming iterators are async

**Unknowns Resolved**:
- ✅ Best practices for httpx.AsyncClient mocking
- ✅ pytest-asyncio configuration modes
- ✅ httpx.Response method synchronicity
- ✅ Async test conversion patterns
- ✅ Common pitfalls and solutions

---

## Phase 1: Design & Contracts ✅ COMPLETE

**Outputs**:
- [data-model.md](./data-model.md) - Test infrastructure entities
- [quickstart.md](./quickstart.md) - Migration guide
- contracts/ - N/A (no API contracts for test-only feature)
- CLAUDE.md - Updated with pytest-httpx and httpx technologies

**Design Decisions**:
1. **Mock Strategy**: pytest-httpx fixture-based approach (cleaner than manual mocks)
2. **Fixture Organization**: Keep existing sample data fixtures, remove requests-based mocks
3. **Test Conversion Pattern**: 5-step migration process per test file
4. **Assertion Strategy**: Use httpx_mock.get_requests() for verification
5. **Configuration**: pytest.ini with asyncio_mode=auto for zero-decorator tests

**Data Model**:
- AsyncClient Mock (via pytest-httpx)
- Response Mock (via pytest-httpx)
- Test Fixtures (conftest.py)
- pytest Configuration (pytest.ini)
- HTTPXMock Request Configuration

**Agent Context Updated**: ✅ CLAUDE.md updated with new technologies

---

## Phase 2: Task Generation (Next Step)

**Command**: `/speckit.tasks`

**Expected Output**: [tasks.md](./tasks.md) with dependency-ordered implementation tasks

**Estimated Tasks**:
1. Install pytest-httpx dependency
2. Configure pytest.ini for async mode
3. Update conftest.py (remove requests fixtures)
4. Migrate test_dify_client.py
5. Migrate test_chat_client.py
6. Migrate test_completion_client.py
7. Migrate test_workflow_client.py
8. Migrate test_knowledge_base_client.py
9. Migrate test_workspace_client.py
10. Final validation and coverage check

---

## Implementation Readiness

**Status**: ✅ Ready for `/speckit.tasks`

**Artifacts Created**:
- ✅ plan.md (this file)
- ✅ research.md (technology research)
- ✅ data-model.md (test entities)
- ✅ quickstart.md (migration guide)
- ✅ CLAUDE.md (agent context updated)

**Next Action**: Run `/speckit.tasks` to generate ordered task list
