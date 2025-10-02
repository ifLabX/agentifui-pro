
# Implementation Plan: API Backend Directory Restructuring

**Branch**: `002-migrate-api-backend` | **Date**: 2025-10-02 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/Users/liuyizhou/repos/agentifui-pro/specs/002-migrate-api-backend/spec.md`

## Execution Flow (/plan command scope)
```
1. Load feature spec from Input path
   → ✅ Loaded successfully
2. Fill Technical Context (scan for NEEDS CLARIFICATION)
   → ✅ No NEEDS CLARIFICATION markers
   → Detected Project Type: web (frontend + backend structure)
   → Set Structure Decision: Backend-only refactoring
3. Fill the Constitution Check section based on constitution
   → ✅ Evaluated against constitution v1.0.1
4. Evaluate Constitution Check section
   → ✅ No violations - refactoring maintains all principles
   → Updated Progress Tracking: Initial Constitution Check PASS
5. Execute Phase 0 → research.md
   → ✅ Research on src layout best practices
6. Execute Phase 1 → data-model.md, quickstart.md, CLAUDE.md update
   → ✅ Phase 1 artifacts generated
7. Re-evaluate Constitution Check section
   → ✅ No new violations
   → Updated Progress Tracking: Post-Design Constitution Check PASS
8. Plan Phase 2 → Task generation approach documented
9. STOP - Ready for /tasks command
```

**IMPORTANT**: The /plan command STOPS at step 9. Phases 2-4 are executed by other commands:
- Phase 2: /tasks command creates tasks.md
- Phase 3-4: Implementation execution (manual or via tools)

## Summary

Migrate the Agentifui Pro API backend from flat directory layout to standard Python src/ layout. This refactoring reorganizes all project modules (config, database, health, middleware, models, main.py) into a src/ directory structure while maintaining full backward compatibility with existing functionality, tests, and tooling. The migration follows Python packaging best practices and ensures zero downtime or functionality loss.

## Technical Context

**Language/Version**: Python 3.12+
**Primary Dependencies**: FastAPI 0.100+, SQLAlchemy 2.0+, Pydantic 2.0+, Uvicorn 0.23+, Alembic 1.12+
**Storage**: PostgreSQL (via SQLAlchemy + asyncpg)
**Testing**: pytest 7.0+ with pytest-asyncio, httpx for API testing
**Target Platform**: Linux/macOS server (FastAPI async runtime)
**Project Type**: web (backend portion of monorepo with frontend in /web)
**Performance Goals**: Maintain existing API response times (<200ms p95 for health endpoints)
**Constraints**: Zero downtime migration, all existing tests must pass, maintain uv compatibility
**Scale/Scope**: Single backend application with ~8 modules, migrations/, tests/ directories

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### I. Dual-Stack Excellence
**Status**: ✅ PASS
- Backend-only refactoring, no API contract changes
- Pydantic models remain unchanged, frontend TypeScript interfaces unaffected
- OpenAPI schema generation continues to work

### II. Quality-First Development
**Status**: ✅ PASS
- Ruff configuration (.ruff.toml) will be updated for src/ layout
- All quality gates (linting, formatting, type checking) remain enforced
- Pre-commit hooks continue to function

### III. Test-Driven Implementation
**Status**: ✅ PASS (Refactoring Context)
- Existing tests must pass after migration (regression prevention)
- pytest configuration updated for src/ layout
- Test discovery mechanisms validated

### IV. Internationalization by Design
**Status**: ✅ N/A (Backend infrastructure only)

### V. Convention Consistency
**Status**: ✅ PASS
- Python package naming follows snake_case convention
- All comments remain in English
- Conventional commit for the migration

## Project Structure

### Documentation (this feature)
```
specs/002-migrate-api-backend/
├── plan.md              # This file (/plan command output)
├── research.md          # Phase 0 output (/plan command)
├── data-model.md        # Phase 1 output (/plan command)
├── quickstart.md        # Phase 1 output (/plan command)
└── tasks.md             # Phase 2 output (/tasks command - NOT created by /plan)
```

### Source Code (repository root)

**Current Structure (api/ directory)**:
```
api/
├── config/              # Settings and configuration
├── database/            # DB connection and session management
├── health/              # Health check endpoints
├── middleware/          # Error handling and middleware
├── models/              # SQLAlchemy models
├── migrations/          # Alembic migration scripts (stays at root)
├── tests/               # Test suite (stays at root)
├── main.py              # FastAPI application entry point
├── pyproject.toml       # Project configuration
├── alembic.ini          # Alembic configuration
├── .env.example         # Environment variables template
└── .ruff.toml           # Ruff linting configuration
```

**Target Structure (api/ directory after migration)**:
```
api/
├── src/                 # All project source code moves here
│   ├── config/          # Settings and configuration
│   ├── database/        # DB connection and session management
│   ├── health/          # Health check endpoints
│   ├── middleware/      # Error handling and middleware
│   ├── models/          # SQLAlchemy models
│   └── main.py          # FastAPI application entry point
├── migrations/          # Alembic migration scripts (stays at root)
├── tests/               # Test suite (stays at root, imports from src/)
├── pyproject.toml       # Updated for src/ layout
├── alembic.ini          # Updated for src/ layout
├── .env.example         # Environment variables template
├── .env                 # Created from .env.example if missing
└── .ruff.toml           # Updated for src/ layout
```

**Structure Decision**: Backend-only refactoring within the monorepo's api/ directory. This is part of the web project type (frontend in /web, backend in /api) but only affects the backend portion. The migration moves all project source code into src/ while keeping migrations/, tests/, and configuration files at the api/ root level following Python community standards.

## Phase 0: Outline & Research

No unknowns exist in Technical Context - all information is specified. Research focuses on best practices:

1. **Python src layout best practices**:
   - Research standard src/ layout conventions
   - Package discovery configuration approaches
   - Import path strategies for existing code

2. **Tool configuration patterns**:
   - pytest with src/ layout (pythonpath, import modes)
   - Alembic migration script paths
   - Ruff source code directory specification
   - uvicorn module loading from src/

3. **Migration safety patterns**:
   - Strategies for preserving user .env modifications
   - Import path update approaches (absolute vs relative)
   - Validation techniques for zero-regression migrations

**Output**: research.md documenting decisions and rationale

## Phase 1: Design & Contracts

*Prerequisites: research.md complete*

This is a refactoring feature with no new API contracts or data models. Phase 1 focuses on migration design and validation strategy:

1. **Extract migration components** → `data-model.md`:
   - Source files to move (config/, database/, health/, middleware/, models/, main.py)
   - Files to update (pyproject.toml, alembic.ini, .ruff.toml, pytest configs)
   - Files to preserve (migrations/, tests/, .env.example)

2. **No new API contracts needed**:
   - This is infrastructure refactoring only
   - All existing endpoints remain unchanged
   - Skip contracts/ directory generation

3. **No new tests needed** (validation-focused instead):
   - Existing test suite must pass after migration
   - Import validation strategy
   - Environment configuration validation

4. **Extract validation scenarios** → `quickstart.md`:
   - Step-by-step migration execution
   - Validation commands (uv sync, pytest, health check)
   - Rollback procedure if issues arise

5. **Update agent file incrementally**:
   - Run `.specify/scripts/bash/update-agent-context.sh claude`
   - Add src/ layout information to CLAUDE.md
   - Update Active Technologies with migration details

**Output**: data-model.md (migration components), quickstart.md (validation steps), CLAUDE.md update

## Phase 2: Task Planning Approach

*This section describes what the /tasks command will do - DO NOT execute during /plan*

**Task Generation Strategy**:
- Load `.specify/templates/tasks-template.md` as base
- Generate tasks from migration components in data-model.md
- Each directory to move → relocation task [P where safe]
- Each configuration file → update task
- Validation steps from quickstart.md → verification tasks

**Ordering Strategy**:
1. Setup: Create src/ directory structure with __init__.py files
2. Move: Relocate all source modules to src/ [some parallel]
3. Update: Modify all configuration files for src/ layout
4. Validate: Run uv sync, pytest, import checks
5. Polish: Environment setup, documentation updates

**Estimated Output**: 15-20 numbered, ordered tasks in tasks.md

**IMPORTANT**: This phase is executed by the /tasks command, NOT by /plan

## Phase 3+: Future Implementation

*These phases are beyond the scope of the /plan command*

**Phase 3**: Task execution (/tasks command creates tasks.md)
**Phase 4**: Implementation (execute tasks.md following constitutional principles)
**Phase 5**: Validation (run tests, execute quickstart.md, verify functionality)

## Complexity Tracking

*No constitutional violations - this section left empty*

## Progress Tracking

*This checklist is updated during execution flow*

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
- [x] All NEEDS CLARIFICATION resolved (none existed)
- [x] Complexity deviations documented (none exist)

---
*Based on Constitution v1.0.1 - See `.specify/memory/constitution.md`*
