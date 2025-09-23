# Implementation Plan: FastAPI Backend Architecture Foundation

**Branch**: `001-fastapi-pg-orm` | **Date**: 2025-09-23 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/001-fastapi-pg-orm/spec.md`

## Execution Flow (/plan command scope)
```
1. Load feature spec from Input path ✅
   → Feature spec loaded successfully
2. Fill Technical Context (scan for NEEDS CLARIFICATION) ✅
   → Detected Project Type: web (backend FastAPI + frontend Next.js exists)
   → Set Structure Decision based on project type
3. Fill the Constitution Check section ✅
4. Evaluate Constitution Check section ✅
   → No violations found - complies with existing patterns
   → Update Progress Tracking: Initial Constitution Check ✅
5. Execute Phase 0 → research.md 🔄
   → Context7 research completed for SQLAlchemy 2.0 + Alembic
6. Execute Phase 1 → contracts, data-model.md, quickstart.md, CLAUDE.md 🔄
7. Re-evaluate Constitution Check section 🔄
   → Update Progress Tracking: Post-Design Constitution Check
8. Plan Phase 2 → Describe task generation approach (DO NOT create tasks.md) 🔄
9. STOP - Ready for /tasks command
```

**IMPORTANT**: The /plan command STOPS at step 7. Phases 2-4 are executed by other commands:
- Phase 2: /tasks command creates tasks.md
- Phase 3-4: Implementation execution (manual or via tools)

## Summary
Setup minimal FastAPI backend architecture foundation with PostgreSQL, SQLAlchemy ORM, and Alembic migrations. Focus on establishing solid infrastructure base without business logic modules, supporting future RLS implementation and PostgreSQL 18 UUIDv7 primary keys.

## Technical Context
**Language/Version**: Python 3.12+ (matches existing project requirements)
**Primary Dependencies**: FastAPI 0.100.0+, SQLAlchemy 2.0+ with asyncio support, Alembic (latest), asyncpg for PostgreSQL async driver
**Storage**: PostgreSQL (preparing for v18 with UUIDv7 support for primary keys)
**Testing**: pytest with FastAPI test client, async test support
**Target Platform**: Linux server with async FastAPI deployment (uvicorn)
**Project Type**: web - FastAPI backend serving Next.js frontend
**Performance Goals**: Database connection pooling, async/await patterns, sub-200ms API response times
**Constraints**: No business logic modules, RLS-ready architecture, follow existing project conventions (uv package management, Ruff linting)
**Scale/Scope**: Foundation for medium-scale application (~10K users), proper migration framework for schema evolution

## Constitution Check
*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### I. Dual-Stack Excellence ✅
- FastAPI backend with Pydantic models ensures typed API contracts
- Existing Next.js frontend will consume typed OpenAPI specifications
- Cross-stack communication via auto-generated TypeScript interfaces

### II. Quality-First Development ✅
- Inherits existing Ruff configuration (120 char limit, comprehensive ruleset)
- Aligns with pre-commit hooks and quality gates
- Python 3.12+ requirement maintains modern standards

### III. Test-Driven Implementation ✅
- FastAPI test client for endpoint validation
- Database migration testing with Alembic
- Health check endpoint validation

### IV. Internationalization by Design ✅
- Backend foundation only - no user-facing text
- API responses use structured data, not hardcoded strings
- Future business modules will inherit i18n patterns

### V. Convention Consistency ✅
- Follows existing project structure (api/ directory)
- Uses established tooling (uv, Python 3.12+)
- Maintains English-only documentation and comments

**Status**: PASS - No constitutional violations detected

## Project Structure

### Documentation (this feature)
```
specs/001-fastapi-pg-orm/
├── plan.md              # This file (/plan command output)
├── research.md          # Phase 0 output (/plan command)
├── data-model.md        # Phase 1 output (/plan command)
├── quickstart.md        # Phase 1 output (/plan command)
├── contracts/           # Phase 1 output (/plan command)
└── tasks.md             # Phase 2 output (/tasks command - NOT created by /plan)
```

### Source Code (repository root)
```
# Option 2: Web application (when "frontend" + "backend" detected)
api/                     # Existing FastAPI backend
├── models/              # SQLAlchemy models
├── database/            # DB connection, session management
├── config/              # Environment configuration
├── health/              # Health check endpoints
├── middleware/          # Error handling middleware
├── alembic/             # New: Alembic migrations
│   ├── env.py           # Migration environment
│   ├── script.py.mako   # Migration template
│   └── versions/        # Migration files
├── tests/               # New: organized tests
│   ├── conftest.py      # Test configuration
│   ├── test_health.py   # Health endpoint tests
│   └── test_database.py # Database connection tests
├── alembic.ini          # Alembic configuration
├── main.py              # Existing: FastAPI app entry point
└── pyproject.toml       # Existing: updated with new dependencies

web/                     # Existing Next.js frontend
├── src/
│   ├── components/
│   ├── pages/
│   └── services/
└── tests/
```

**Structure Decision**: Option 2 (Web application) - FastAPI backend with Next.js frontend

## Phase 0: Outline & Research

1. **Extract unknowns from Technical Context** above:
   - PostgreSQL 18 UUIDv7 integration patterns (future-proofing)
   - SQLAlchemy 2.0 async best practices with FastAPI
   - Alembic configuration for async environments
   - RLS-ready database architecture patterns

2. **Generate and dispatch research agents**:
   ```
   For PostgreSQL 18 UUIDv7: Research UUID v7 implementation readiness and fallback strategies
   For SQLAlchemy 2.0 async: Find best practices for FastAPI + SQLAlchemy 2.0 + asyncpg integration
   For Alembic async: Research async migration patterns and configuration
   For RLS architecture: Find PostgreSQL RLS patterns that don't require immediate implementation
   ```

3. **Consolidate findings** in `research.md` using format:
   - Decision: [what was chosen]
   - Rationale: [why chosen]
   - Alternatives considered: [what else evaluated]

**Output**: research.md with all technical decisions documented

## Phase 1: Design & Contracts
*Prerequisites: research.md complete*

1. **Extract entities from feature spec** → `data-model.md`:
   - Database Connection (session management, connection pooling)
   - Migration State (Alembic version tracking)
   - Application Configuration (environment settings)
   - Health Status (monitoring endpoints)

2. **Generate API contracts** from functional requirements:
   - GET /health → application health status
   - GET /health/db → database connectivity status
   - Standard error response schemas
   - Output OpenAPI schema to `/contracts/`

3. **Generate contract tests** from contracts:
   - test_health.py → health endpoint validation
   - test_database.py → database connection testing
   - Tests must fail initially (no implementation yet)

4. **Extract test scenarios** from user stories:
   - Developer setup scenario → quickstart validation
   - Database migration scenario → Alembic testing
   - Connection failure scenario → error handling validation

5. **Update agent file incrementally** (O(1) operation):
   - Run `.specify/scripts/bash/update-agent-context.sh claude`
   - Add SQLAlchemy 2.0, Alembic, asyncpg to tech context
   - Preserve existing FastAPI patterns
   - Update with new database architecture patterns
   - Keep under 150 lines for token efficiency

**Output**: data-model.md, /contracts/*, failing tests, quickstart.md, CLAUDE.md

## Phase 2: Task Planning Approach
*This section describes what the /tasks command will do - DO NOT execute during /plan*

**Task Generation Strategy**:
- Load `.specify/templates/tasks-template.md` as base
- Generate tasks from Phase 1 design docs (contracts, data model, quickstart)
- Each contract → contract test task [P]
- Each entity → model/service creation task [P]
- Database setup → connection and session management tasks
- Alembic setup → migration framework configuration tasks
- Health checks → monitoring endpoint implementation tasks

**Ordering Strategy**:
- TDD order: Tests before implementation
- Dependency order: Config → Database → Models → Services → Endpoints
- Infrastructure first: Database connection before ORM models
- Mark [P] for parallel execution (independent components)

**Estimated Output**: 20-25 numbered, ordered tasks in tasks.md focusing on:
1. Environment configuration and dependencies
2. Database connection and session management
3. Alembic migration framework setup
4. Health check endpoints
5. Test infrastructure
6. Documentation updates

**IMPORTANT**: This phase is executed by the /tasks command, NOT by /plan

## Phase 3+: Future Implementation
*These phases are beyond the scope of the /plan command*

**Phase 3**: Task execution (/tasks command creates tasks.md)
**Phase 4**: Implementation (execute tasks.md following constitutional principles)
**Phase 5**: Validation (run tests, execute quickstart.md, performance validation)

## Complexity Tracking
*Fill ONLY if Constitution Check has violations that must be justified*

No constitutional violations detected - all patterns align with existing project standards.

## Progress Tracking
*This checklist is updated during execution flow*

**Phase Status**:
- [x] Phase 0: Research complete (/plan command) ✅ 2025-09-23
- [x] Phase 1: Design complete (/plan command) ✅ 2025-09-23
- [x] Phase 2: Task planning complete (/plan command - describe approach only) ✅ 2025-09-23
- [ ] Phase 3: Tasks generated (/tasks command) - Ready for execution
- [ ] Phase 4: Implementation complete
- [ ] Phase 5: Validation passed

**Gate Status**:
- [x] Initial Constitution Check: PASS ✅
- [x] Post-Design Constitution Check: PASS ✅ All principles maintained
- [x] All NEEDS CLARIFICATION resolved ✅ Research complete
- [x] Complexity deviations documented ✅ None required

**Artifacts Generated**:
- [x] research.md: Technology decisions and PostgreSQL 18 UUIDv7 strategy
- [x] data-model.md: Core entities and architecture patterns
- [x] contracts/health.yaml: Health monitoring API specification
- [x] contracts/errors.yaml: Standardized error response schemas
- [x] quickstart.md: Developer setup and validation guide
- [x] CLAUDE.md: Updated with database architecture context

---
*Based on Constitution v1.0.0 - See `/memory/constitution.md`*