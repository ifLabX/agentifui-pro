# Tasks: Backend Foundation Architecture

**Input**: Design documents from `/specs/001-fastapi-api-alembic/`
**Prerequisites**: plan.md (✓), research.md (✓), data-model.md (✓), contracts/ (✓)

## Execution Flow (main)
```
1. Load plan.md from feature directory ✓
   → Extracted: FastAPI, SQLAlchemy 2.0, Alembic, Uvicorn, Pydantic
   → Structure: Web app (api/ directory)
2. Load optional design documents: ✓
   → data-model.md: Application Configuration, Database Connection, Migration Management
   → contracts/: health.yaml (2 endpoints), info.yaml (1 endpoint)
   → research.md: Technology decisions and best practices
3. Generate tasks by category: ✓
   → Setup: project structure, dependencies, configuration
   → Tests: contract tests for health and info endpoints
   → Core: configuration models, database setup, API endpoints
   → Integration: database connection, Alembic setup
   → Polish: development scripts, documentation
4. Apply task rules: ✓
   → Different files = marked [P] for parallel
   → Same file = sequential (no [P])
   → Tests before implementation (TDD)
5. Number tasks sequentially (T001, T002...) ✓
6. Generate dependency graph ✓
7. Create parallel execution examples ✓
8. Validate task completeness: ✓
   → All contracts have tests ✓
   → All configuration entities have models ✓
   → All endpoints implemented ✓
9. Return: SUCCESS (tasks ready for execution)
```

## Format: `[ID] [P?] Description`
- **[P]**: Can run in parallel (different files, no dependencies)
- Include exact file paths in descriptions

## Path Conventions
- **Web app structure**: `api/` directory with `app/` subdirectory
- Based on plan.md: Backend in api/, frontend in web/

## Phase 3.1: Setup
- [ ] T001 Create api/ project structure with app/, tests/, alembic/ directories
- [ ] T002 Initialize Python project with pyproject.toml and uv configuration in api/
- [ ] T003 [P] Configure Ruff linting and formatting in api/.ruff.toml
- [ ] T004 [P] Create environment configuration template in api/.env.example

## Phase 3.2: Tests First (TDD) ⚠️ MUST COMPLETE BEFORE 3.3
**CRITICAL: These tests MUST be written and MUST FAIL before ANY implementation**
- [ ] T005 [P] Contract test GET /health in api/tests/contract/test_health.py
- [ ] T006 [P] Contract test GET /health/ready in api/tests/contract/test_health_ready.py
- [ ] T007 [P] Contract test GET /info in api/tests/contract/test_info.py
- [ ] T008 [P] Integration test database connection in api/tests/integration/test_database.py
- [ ] T009 [P] Integration test application startup in api/tests/integration/test_startup.py

## Phase 3.3: Core Implementation (ONLY after tests are failing)
- [ ] T010 [P] Base model pattern in api/app/db/models/base.py
- [ ] T011 [P] Application configuration in api/app/core/config/settings.py
- [ ] T012 [P] Database configuration in api/app/core/config/database.py
- [ ] T013 [P] Health response schemas in api/app/schemas/health.py
- [ ] T014 [P] Info response schemas in api/app/schemas/info.py
- [ ] T015 Main FastAPI application in api/app/main.py
- [ ] T016 Health endpoints in api/app/api/v1/endpoints/health.py
- [ ] T017 Info endpoint in api/app/api/v1/endpoints/info.py
- [ ] T018 API router setup in api/app/api/v1/router.py
- [ ] T019 Exception handlers in api/app/core/exceptions/handlers.py

## Phase 3.4: Integration
- [ ] T020 Database session management in api/app/db/session.py
- [ ] T021 Alembic configuration setup in api/alembic.ini and api/alembic/env.py
- [ ] T022 Development server script in api/app/scripts/dev.py
- [ ] T023 CORS middleware configuration in api/app/core/middleware.py
- [ ] T024 Initial database migration setup

## Phase 3.5: Polish
- [ ] T025 [P] Unit tests for configuration validation in api/tests/unit/test_config.py
- [ ] T026 [P] Unit tests for schema validation in api/tests/unit/test_schemas.py
- [ ] T027 [P] Development scripts in api/scripts/ directory
- [ ] T028 [P] Basic logging configuration in api/app/core/logging.py
- [ ] T029 Verify quickstart.md procedures work correctly
- [ ] T030 Final code quality check and cleanup

## Dependencies
- **Setup Phase (T001-T004)** before all other phases
- **Tests (T005-T009)** before implementation (T010-T019)
- **T010 (Base model)** blocks T011-T014 (configuration models)
- **T011-T014 (Configuration/Schemas)** before T015-T019 (API implementation)
- **T015 (Main app)** blocks T016-T018 (endpoints and routing)
- **T020-T021 (Database/Alembic)** before T024 (migration setup)
- **Implementation** before **Polish (T025-T030)**

## Parallel Example
```bash
# Launch T005-T009 together (contract and integration tests):
Task: "Contract test GET /health in api/tests/contract/test_health.py"
Task: "Contract test GET /health/ready in api/tests/contract/test_health_ready.py"
Task: "Contract test GET /info in api/tests/contract/test_info.py"
Task: "Integration test database connection in api/tests/integration/test_database.py"
Task: "Integration test application startup in api/tests/integration/test_startup.py"

# Launch T010-T014 together (models and configuration):
Task: "Base model pattern in api/app/db/models/base.py"
Task: "Application configuration in api/app/core/config/settings.py"
Task: "Database configuration in api/app/core/config/database.py"
Task: "Health response schemas in api/app/schemas/health.py"
Task: "Info response schemas in api/app/schemas/info.py"

# Launch T025-T028 together (polish phase):
Task: "Unit tests for configuration validation in api/tests/unit/test_config.py"
Task: "Unit tests for schema validation in api/tests/unit/test_schemas.py"
Task: "Development scripts in api/scripts/ directory"
Task: "Basic logging configuration in api/app/core/logging.py"
```

## Notes
- **[P] tasks** = different files, no dependencies
- **Foundation focus**: Minimal viable backend structure, avoid extensive business logic
- **Integration with monorepo**: CORS configured for localhost:3000 frontend
- **Quality standards**: Ruff linting, type hints, Pydantic validation
- **Testing approach**: Contract tests for API compliance, integration tests for system behavior
- **User context**: Framework and essential components only, not extensive feature implementation

## Task Generation Rules
*Applied during main() execution*

1. **From Contracts**:
   - health.yaml → T005 (GET /health), T006 (GET /health/ready)
   - info.yaml → T007 (GET /info)

2. **From Data Model**:
   - Application Configuration → T011 (settings.py)
   - Database Connection → T012 (database.py)
   - Base Model Pattern → T010 (base.py)

3. **From Quickstart**:
   - Setup steps → T001-T004 (project structure)
   - Verification tests → T005-T009 (contract/integration tests)
   - Quality checks → T025-T030 (polish phase)

4. **Ordering**:
   - Setup → Tests → Models → Services → Endpoints → Polish
   - Dependencies prevent parallel execution where needed

## Validation Checklist
*GATE: Checked by main() before returning*

- [x] All contracts have corresponding tests (health.yaml → T005,T006; info.yaml → T007)
- [x] All entities have model tasks (Configuration → T011,T012; Base → T010)
- [x] All tests come before implementation (T005-T009 before T010-T019)
- [x] Parallel tasks truly independent (different files, no shared dependencies)
- [x] Each task specifies exact file path (all paths included in descriptions)
- [x] No task modifies same file as another [P] task (verified independence)