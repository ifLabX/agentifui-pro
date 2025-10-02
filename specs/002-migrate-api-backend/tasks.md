# Tasks: API Backend Directory Restructuring

**Input**: Design documents from `/Users/liuyizhou/repos/agentifui-pro/specs/002-migrate-api-backend/`
**Prerequisites**: plan.md, research.md, data-model.md, quickstart.md

## Execution Flow (main)
```
1. Load plan.md from feature directory
   → ✅ Loaded successfully
   → Extract: Python 3.12+, FastAPI, SQLAlchemy, pytest, uv
2. Load optional design documents:
   → data-model.md: Extracted migration components (6 modules to move, 4 files to update)
   → quickstart.md: Extracted validation steps (11 steps)
   → research.md: Extracted decisions (src/ layout, package discovery)
3. Generate tasks by category:
   → Setup: Create src/ directory
   → Move: Relocate modules to src/ (6 modules)
   → Update: Configuration files (4 files)
   → Validate: Run tests and checks
   → Polish: Documentation and cleanup
4. Apply task rules:
   → Different files = mark [P] for parallel
   → Same file = sequential (no [P])
   → Migration is refactoring, not TDD (existing tests validate)
5. Number tasks sequentially (T001, T002...)
6. Generate dependency graph
7. Create parallel execution examples
8. Validate task completeness:
   → All modules moved? ✅
   → All config files updated? ✅
   → All validation steps included? ✅
9. Return: SUCCESS (tasks ready for execution)
```

## Format: `[ID] [P?] Description`
- **[P]**: Can run in parallel (different files, no dependencies)
- Include exact file paths in descriptions

## Path Conventions
- **Working directory**: `/Users/liuyizhou/repos/agentifui-pro/api`
- **Source modules**: Currently at `api/` root, moving to `api/src/`
- **Config files**: Remain at `api/` root
- **Tests**: Remain at `api/tests/`

## Phase 3.1: Pre-Migration Setup

- [ ] T001 Verify current state and run baseline tests in api/ directory
- [ ] T002 Backup existing .env file if present to .env.backup in api/

## Phase 3.2: Directory Structure Creation

- [ ] T003 Create src/ directory in api/

## Phase 3.3: Module Relocation ⚠️ MUST COMPLETE BEFORE 3.4

**CRITICAL: These moves MUST complete before any configuration updates**

- [ ] T004 [P] Move api/config/ directory to api/src/config/
- [ ] T005 [P] Move api/database/ directory to api/src/database/
- [ ] T006 [P] Move api/models/ directory to api/src/models/
- [ ] T007 [P] Move api/health/ directory to api/src/health/
- [ ] T008 [P] Move api/middleware/ directory to api/src/middleware/
- [ ] T009 Move api/main.py file to api/src/main.py

## Phase 3.4: Configuration Updates (ONLY after modules moved)

- [ ] T010 Update api/pyproject.toml: Add [tool.setuptools.packages.find] section with where = ["src"]
- [ ] T011 Update api/pyproject.toml: Add [tool.pytest.ini_options] section with pythonpath, testpaths, asyncio_mode
- [ ] T012 Update api/.ruff.toml: Add src = ["src"] to [tool.ruff] section
- [ ] T013 Update api/migrations/env.py: Change all application imports to use src. prefix (models.base → src.models.base, config.settings → src.config.settings)

## Phase 3.5: Environment Setup

- [ ] T014 Create api/.env from api/.env.example if .env does not exist (preserve existing .env if present)

## Phase 3.6: Validation (MUST run in order)

- [ ] T015 Run uv sync in api/ directory to verify package discovery and import resolution
- [ ] T016 Run uv run pytest in api/ directory to verify all tests pass with new structure
- [ ] T017 Test import resolution: Run uv run python -c "from src.main import app; print('✓ Imports work')" in api/
- [ ] T018 Start API server: Run uv run uvicorn src.main:app --reload --port 8000 in api/ and verify startup
- [ ] T019 Test health endpoint: curl http://localhost:8000/health and verify response

## Phase 3.7: Polish

- [ ] T020 [P] Update api/README.md: Change uvicorn command examples from main:app to src.main:app
- [ ] T021 Run uv run ruff check src in api/ directory to verify linting passes
- [ ] T022 Remove api/.env.backup if migration successful and .env exists

## Dependencies

**Critical Path**:
- T001-T002 (pre-migration) before T003 (create directory)
- T003 blocks T004-T009 (cannot move to non-existent directory)
- T004-T009 block T010-T013 (config updates require modules in place)
- T010-T013 block T014 (environment setup after config)
- T014 blocks T015 (uv sync requires config)
- T015 blocks T016-T019 (tests and server require successful sync)
- T016-T019 block T020-T022 (polish after validation)

**Parallel Opportunities**:
- T004-T008 can run in parallel (different directories)
- T020-T021 can run in parallel (different operations)

## Parallel Example

```bash
# Launch T004-T008 together (parallel module moves):
# Note: These are simple mv commands, can be batched in single shell script

cd /Users/liuyizhou/repos/agentifui-pro/api
mv config src/ && mv database src/ && mv models src/ && mv health src/ && mv middleware src/

# Or execute individually in parallel:
# Terminal 1: cd api && mv config src/
# Terminal 2: cd api && mv database src/
# Terminal 3: cd api && mv models src/
# Terminal 4: cd api && mv health src/
# Terminal 5: cd api && mv middleware src/
```

## Notes

- **Not TDD**: This is a refactoring migration, not new feature development
- **Existing tests validate**: Tests must pass after migration to ensure no regression
- **[P] tasks**: T004-T008 (parallel moves), T020-T021 (parallel polish)
- **Sequential config updates**: T010-T013 must be done carefully, one at a time
- **Validation order matters**: T015-T019 must run in sequence
- **Preserve .env**: T014 must not overwrite existing user configuration
- **Commit after validation**: After T019 passes, commit changes

## Validation Checklist

*GATE: Checked during execution*

- [ ] All modules successfully moved to src/ (T004-T009)
- [ ] All configuration files updated correctly (T010-T013)
- [ ] uv sync completes without errors (T015)
- [ ] All tests pass (T016)
- [ ] Import resolution works (T017)
- [ ] Server starts successfully (T018)
- [ ] Health endpoint responds (T019)
- [ ] Documentation updated (T020)
- [ ] Linting passes (T021)

## Migration Safety

**Rollback Strategy**: If any validation task (T015-T019) fails:
1. Stop execution immediately
2. Run: `git checkout main && git branch -D 002-migrate-api-backend`
3. Or manually rollback: Move src/* back to api/ root, restore original config files

**Success Criteria**: All validation tasks (T015-T019) pass ✅

## Estimated Effort

- **Setup (T001-T003)**: 5 minutes
- **Module moves (T004-T009)**: 10 minutes
- **Config updates (T010-T013)**: 15 minutes
- **Environment (T014)**: 2 minutes
- **Validation (T015-T019)**: 10 minutes
- **Polish (T020-T022)**: 5 minutes
- **Total**: ~45 minutes

## Task Complexity

- **Low complexity**: T001-T009, T014, T020, T022 (file operations)
- **Medium complexity**: T010-T013 (configuration edits)
- **Critical tasks**: T015-T019 (validation must pass)
