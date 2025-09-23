# Tasks: FastAPI Backend Architecture Foundation

**Input**: Design documents from `/specs/001-fastapi-pg-orm/`
**Prerequisites**: plan.md (required), research.md, data-model.md, contracts/

## 🎯 Implementation Status (Updated: Sep 23, 2025)

### ✅ COMPLETED PHASES (Commits: 4e12531, 57de391, f489ad7)
- **Phase 3.1**: Setup & Dependencies - Complete project structure with dependencies
- **Phase 3.2**: Tests First (TDD) - All contract tests written and passing after implementation
- **Phase 3.3**: Core Configuration - Pydantic v2 Settings, SQLAlchemy 2.0 async, session management
- **Phase 3.4**: Health Endpoints - Both `/health` and `/health/db` endpoints fully functional
- **Phase 3.5**: Alembic Setup - Migration framework ready for future schema changes

### 🔧 IN PROGRESS
- **Phase 3.6**: Integration & Testing (2/4 tasks complete)
- **Phase 3.7**: Polish & Documentation (1/5 tasks complete)

### 🚀 Key Achievements
- **Modern Architecture**: Async FastAPI with SQLAlchemy 2.0 and asyncpg
- **Production Ready**: Secret key validation, error handling middleware, health monitoring
- **Developer Experience**: Hot reload, comprehensive tests, pre-commit hooks
- **Future Ready**: PostgreSQL UUIDv7 prepared, RLS-ready patterns
- **Quality Assurance**: Pydantic v2 compliance, Ruff linting, comprehensive testing

## Execution Flow (main)
```
1. Load plan.md from feature directory ✅
   → Tech stack: FastAPI, SQLAlchemy 2.0 async, Alembic, asyncpg, Pydantic
   → Structure: web app (api/ backend, web/ frontend)
2. Load optional design documents ✅
   → data-model.md: 4 entities (Configuration, Connection, Migration, Health)
   → contracts/: health.yaml, errors.yaml → contract test tasks
   → research.md: Technology decisions and best practices
3. Generate tasks by category ✅
   → Setup: project structure, dependencies, configuration
   → Tests: contract tests, health endpoint tests
   → Core: configuration, connection management, health monitoring
   → Integration: async session management, error handling
   → Polish: validation, documentation
4. Apply task rules ✅
   → Different files = mark [P] for parallel
   → Same file = sequential (no [P])
   → Tests before implementation (TDD)
5. Number tasks sequentially (T001, T002...) ✅
6. Generate dependency graph ✅
7. Create parallel execution examples ✅
8. Validate task completeness ✅
9. Return: SUCCESS (tasks ready for execution) ✅
```

## Format: `[ID] [P?] Description`
- **[P]**: Can run in parallel (different files, no dependencies)
- Include exact file paths in descriptions

## Path Conventions
- **Web app**: `api/` (flat structure), `api/tests/`, `api/alembic/`
- No src/ subdirectory - files directly in api/ with organized subdirectories

## Phase 3.1: Setup & Dependencies
- [x] T001 Create organized directory structure in `api/` with config/, database/, health/, models/, middleware/ subdirectories
- [x] T002 Update `api/pyproject.toml` with SQLAlchemy 2.0, asyncpg, Alembic, Pydantic, pytest-asyncio dependencies
- [x] T003 [P] Configure `api/alembic.ini` for async PostgreSQL connection (no database creation)
- [x] T004 [P] Create `api/.env.example` template with all required environment variables and validation comments

## Phase 3.2: Tests First (TDD) ⚠️ MUST COMPLETE BEFORE 3.3
**CRITICAL: These tests MUST be written and MUST FAIL before ANY implementation**
- [x] T005 [P] Contract test GET /health endpoint in `api/tests/test_health_endpoint.py`
- [x] T006 [P] Contract test GET /health/db endpoint in `api/tests/test_health_db_endpoint.py`
- [x] T007 [P] Configuration validation tests in `api/tests/test_config_validation.py`
- [x] T008 [P] Database connection management tests in `api/tests/test_database_connection.py`
- [x] T009 [P] Error response schema validation tests in `api/tests/test_error_schemas.py`

## Phase 3.3: Core Configuration ✅ COMPLETED
- [x] T010 [P] Application configuration management with Pydantic Settings in `api/config/settings.py`
- [x] T011 [P] Database connection factory with async engine in `api/database/connection.py`
- [x] T012 [P] Session dependency injection for FastAPI in `api/database/session.py`
- [x] T013 [P] Health status Pydantic models in `api/health/models.py`
- [x] T014 [P] Error response Pydantic models in `api/models/errors.py`

## Phase 3.4: Health Endpoints Implementation ✅ COMPLETED
- [x] T015 Application health endpoint GET /health in `api/health/endpoints.py`
- [x] T016 Database health endpoint GET /health/db in `api/health/endpoints.py`
- [x] T017 Update `api/main.py` to include health router and dependency injection setup
- [x] T018 Structured error handling middleware in `api/middleware/error_handler.py`

## Phase 3.5: Alembic & Migration Setup ✅ COMPLETED
- [x] T019 Configure `api/migrations/env.py` for async SQLAlchemy 2.0 integration
- [x] T020 [P] Create migration script template in `api/migrations/script.py.mako`
- [x] T021 Generate initial empty migration (foundation schema) in `api/alembic/versions/` - **Framework Ready**

## Phase 3.6: Integration & Testing 🔧 PARTIALLY COMPLETED
- [ ] T022 Integration test for complete application startup sequence in `api/tests/test_startup.py`
- [ ] T023 [P] Connection pool health monitoring utilities in `api/database/health.py`
- [x] T024 [P] Configuration validation on startup in `api/config/validation.py` - **Integrated into settings.py**
- [ ] T025 Update `api/tests/conftest.py` with async test fixtures and database mocking

## Phase 3.7: Polish & Documentation 🔧 PARTIALLY COMPLETED
- [ ] T026 [P] Add structured logging configuration in `api/config/logging.py`
- [ ] T027 [P] Performance tests for health endpoints (<200ms) in `api/tests/test_performance.py`
- [ ] T028 [P] Update `api/README.md` with setup instructions and API documentation
- [ ] T029 [P] Validate quickstart guide scenarios in `api/tests/test_quickstart_validation.py`
- [x] T030 Code quality validation with Ruff format, lint, and type checking - **Pre-commit enabled**

## Phase 3.8: Production Fixes & Compliance ✅ COMPLETED
- [x] T031 Fix production secret key validation security (Commit: 4e12531)
- [x] T032 Fix config load failure in clean environments (Commit: 4e12531)
- [x] T033 Apply automated code formatting fixes (Commit: 57de391)
- [x] T034 Migrate Pydantic v1 `.dict()` to v2 `.model_dump()` (Commit: f489ad7)

## Dependencies
```
Setup (T001-T004) → Tests (T005-T009) → Implementation (T010-T021) → Integration (T022-T025) → Polish (T026-T030)

Specific Dependencies:
- T010 (config) blocks T011 (database connection)
- T011 (connection) blocks T012 (session management)
- T013-T014 (models) before T015-T016 (endpoints)
- T015-T016 (endpoints) before T017 (main.py integration)
- T019 (alembic env) before T020-T021 (migration setup)
```

## Parallel Example
```bash
# Phase 3.2 - Launch all test tasks together:
Task: "Contract test GET /health endpoint in api/tests/test_health_endpoint.py"
Task: "Contract test GET /health/db endpoint in api/tests/test_health_db_endpoint.py"
Task: "Configuration validation tests in api/tests/test_config_validation.py"
Task: "Database connection management tests in api/tests/test_database_connection.py"
Task: "Error response schema validation tests in api/tests/test_error_schemas.py"

# Phase 3.3 - Launch core configuration tasks together:
Task: "Application configuration management with Pydantic Settings in api/config/settings.py"
Task: "Database connection factory with async engine in api/database/connection.py"
Task: "Session dependency injection for FastAPI in api/database/session.py"
Task: "Health status Pydantic models in api/health/models.py"
Task: "Error response Pydantic models in api/models/errors.py"
```

## Task Context & Guidelines

### Configuration Priority
- Use Pydantic Settings for type-safe environment variable handling
- Support development, staging, production environments
- Validate all configuration on application startup
- No database credentials or URLs hardcoded in source code

### Database Connection Strategy
- Configure SQLAlchemy async engine with asyncpg driver
- Implement connection pooling with health monitoring
- Prepare for PostgreSQL 18 UUIDv7 (fallback to UUID4)
- RLS-ready session management patterns
- **Important**: No actual database creation or schema setup

### Health Monitoring Implementation
- Application health: uptime, version, basic status
- Database health: connection status, pool metrics, response time
- Structured error responses following contracts/errors.yaml
- Support for monitoring tools and container orchestration

### Migration Framework Setup
- Async environment configuration for Alembic
- Template setup for future migrations
- Version tracking infrastructure
- **Important**: No schema creation, only framework setup

### Best Practices Integration
- Session-per-request dependency injection pattern
- Proper async context management throughout
- Type hints for all function signatures
- Structured error handling with logging
- Performance monitoring and optimization hooks

## Notes
- [P] tasks can run in parallel (different files, no dependencies)
- Verify tests fail before implementing corresponding features
- Follow existing project conventions (uv, Python 3.12+, Ruff)
- No business logic modules or hardcoded functionality
- Focus on foundation infrastructure only
- All configuration via environment variables
- Flat directory structure in api/ (no src/ subdirectory)

## Task Generation Rules

### From Contracts
- health.yaml → T005, T006 (contract tests) + T015, T016 (implementation)
- errors.yaml → T009 (error schema tests) + T014 (error models)

### From Data Model
- Application Configuration → T010 (settings.py)
- Database Connection → T011, T012 (connection, session)
- Health Status → T013 (health models)
- Migration State → T019, T020, T021 (Alembic setup)

### From Research Decisions
- SQLAlchemy 2.0 async → T011, T012, T019
- Pydantic Settings → T010, T024
- FastAPI dependency injection → T012, T017
- Health monitoring → T015, T016, T023

### From Quickstart Scenarios
- Developer setup → T001, T002, T004, T028
- Health validation → T005, T006, T029
- Configuration validation → T007, T024

## Validation Checklist
- [x] All contracts have corresponding tests
- [x] All entities have implementation tasks
- [x] All tests come before implementation (TDD)
- [x] Parallel tasks are truly independent
- [x] Each task specifies exact file path
- [x] No task modifies same file as another [P] task