# Tasks: Coze Python SDK Integration

**Input**: Design documents from `/specs/006-use-context7-and/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/test-contracts.md, quickstart.md

**Tests**: This feature IS test implementation - all tasks involve writing tests to validate SDK integration patterns.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`
- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and test directory structure creation

- [ ] T001 Create test directory structure `api/tests/coze/` following Dify SDK pattern
- [ ] T002 Add cozepy dependency to `api/pyproject.toml` dependencies section

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core test infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T003 [P] Create authentication fixtures in `api/tests/coze/conftest.py` (mock_coze_api_token, mock_coze_base_url)
- [ ] T004 [P] Create HTTP response fixtures in `api/tests/coze/conftest.py` (mock_successful_response, mock_error_response, mock_streaming_response)
- [ ] T005 [P] Create entity ID fixtures in `api/tests/coze/conftest.py` (mock_bot_id, mock_workspace_id, mock_conversation_id, mock_chat_id, mock_workflow_id)
- [ ] T006 [P] Create sample data fixtures in `api/tests/coze/conftest.py` (sample_user_message, sample_workflow_inputs, sample_bot_data)
- [ ] T007 [P] Create HTTP client mock fixtures in `api/tests/coze/conftest.py` (mock_httpx_client, mock_async_httpx_client)
- [ ] T008 Add module-level docstring to `api/tests/coze/conftest.py` explaining fixture organization and usage

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - SDK Installation and Configuration (Priority: P1) 🎯 MVP

**Goal**: Developers can install and configure the Coze Python SDK in the backend API to enable integration with Coze AI services.

**Independent Test**: Verify SDK installation in pyproject.toml, confirm package is importable, and validate authentication configuration through environment variables.

### Tests for User Story 1

**NOTE: These tests validate SDK installation and configuration - the core foundation**

- [ ] T009 [P] [US1] Test synchronous client initialization with TokenAuth in `api/tests/coze/test_coze_client.py` (class TestCozeClientInitialization, test_sync_client_init)
- [ ] T010 [P] [US1] Test asynchronous client initialization with AsyncTokenAuth in `api/tests/coze/test_coze_client.py` (class TestCozeClientInitialization, test_async_client_init)
- [ ] T011 [P] [US1] Test client initialization with custom HTTP client timeout configuration in `api/tests/coze/test_coze_client.py` (class TestCozeClientConfiguration, test_custom_http_client_timeout)
- [ ] T012 [P] [US1] Test logging configuration with setup_logging function in `api/tests/coze/test_coze_client.py` (class TestCozeClientConfiguration, test_logging_setup)
- [ ] T013 [P] [US1] Test client properties validation (base_url, api_key accessible) in `api/tests/coze/test_coze_client.py` (class TestCozeClientInitialization, test_client_properties)
- [ ] T014 [US1] Add module-level docstring to `api/tests/coze/test_coze_client.py` explaining test coverage for client initialization

**Checkpoint**: At this point, User Story 1 should be fully functional - SDK installed, importable, and clients initialize correctly

---

## Phase 4: User Story 2 - Basic Coze Client Functionality Testing (Priority: P2)

**Goal**: Developers can verify core Coze SDK client operations work correctly through comprehensive unit tests covering synchronous and asynchronous clients.

**Independent Test**: Run pytest suite that validates client initialization, authentication patterns, and basic client properties using mocks.

### Tests for User Story 2

**NOTE: These tests extend US1 foundation to verify client functionality beyond initialization**

- [ ] T015 [P] [US2] Test client with multiple base URL configurations (COZE_COM_BASE_URL vs COZE_CN_BASE_URL) in `api/tests/coze/test_coze_client.py` (class TestCozeClientConfiguration, test_base_url_variations)
- [ ] T016 [P] [US2] Test authentication header verification in HTTP requests in `api/tests/coze/test_coze_client.py` (class TestCozeClientConfiguration, test_authentication_headers)
- [ ] T017 [P] [US2] Test logid extraction from client responses for debugging in `api/tests/coze/test_coze_client.py` (class TestCozeClientConfiguration, test_logid_extraction)
- [ ] T018 [P] [US2] Test error handling for invalid API tokens in `api/tests/coze/test_coze_client.py` (class TestCozeClientConfiguration, test_invalid_token_handling)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently - client fully validated with error handling

---

## Phase 5: User Story 3 - Bot Operations Testing (Priority: P3)

**Goal**: Developers can test bot-related operations including listing bots, retrieving bot details, and managing bot workspaces through comprehensive test coverage.

**Independent Test**: Run bot-specific test suite that validates list operations, retrieval operations, and workspace queries using mocked API responses.

### Tests for User Story 3

**NOTE: These tests validate bot operations using the client from US1/US2**

- [ ] T019 [P] [US3] Test bot listing with pagination (single page) in `api/tests/coze/test_bot_client.py` (class TestBotOperations, test_list_bots_single_page)
- [ ] T020 [P] [US3] Test bot listing with multi-page iteration using iter_pages() in `api/tests/coze/test_bot_client.py` (class TestBotOperations, test_list_bots_paginated)
- [ ] T021 [P] [US3] Test bot retrieval by ID with logid verification in `api/tests/coze/test_bot_client.py` (class TestBotOperations, test_retrieve_bot)
- [ ] T022 [P] [US3] Test bot listing with workspace ID filtering in `api/tests/coze/test_bot_client.py` (class TestBotOperations, test_list_bots_by_workspace)
- [ ] T023 [P] [US3] Test bot listing with page_size parameter in `api/tests/coze/test_bot_client.py` (class TestBotOperations, test_list_bots_custom_page_size)
- [ ] T024 [P] [US3] Test async bot operations using AsyncCoze client in `api/tests/coze/test_bot_client.py` (class TestBotOperations, test_async_list_bots)
- [ ] T025 [US3] Add module-level docstring to `api/tests/coze/test_bot_client.py` explaining bot operations test coverage

**Checkpoint**: All bot operations independently testable with proper mocking and pagination support

---

## Phase 6: User Story 4 - Chat and Conversation Testing (Priority: P3)

**Goal**: Developers can test chat functionality including both synchronous and streaming chat messages, conversation management, and message operations.

**Independent Test**: Run dedicated chat test suite covering message creation, streaming responses, conversation management, and event handling with mocked responses.

### Tests for User Story 4

**NOTE: These tests validate chat/conversation operations in parallel with bot operations (both P3)**

- [ ] T026 [P] [US4] Test chat creation in blocking mode with token usage in `api/tests/coze/test_chat_client.py` (class TestChatOperations, test_create_chat_blocking)
- [ ] T027 [P] [US4] Test chat creation in streaming mode with event iteration in `api/tests/coze/test_chat_client.py` (class TestChatOperations, test_create_chat_streaming)
- [ ] T028 [P] [US4] Test chat event type handling (CONVERSATION_MESSAGE_DELTA, CONVERSATION_CHAT_COMPLETED) in `api/tests/coze/test_chat_client.py` (class TestChatOperations, test_stream_chat_events)
- [ ] T029 [P] [US4] Test chat with conversation_id for context chaining in `api/tests/coze/test_chat_client.py` (class TestChatOperations, test_chat_with_conversation)
- [ ] T030 [P] [US4] Test conversation creation in `api/tests/coze/test_chat_client.py` (class TestConversationOperations, test_create_conversation)
- [ ] T031 [P] [US4] Test conversation message listing in `api/tests/coze/test_chat_client.py` (class TestConversationOperations, test_list_conversation_messages)
- [ ] T032 [P] [US4] Test message delta accumulation in streaming chat in `api/tests/coze/test_chat_client.py` (class TestChatOperations, test_streaming_message_accumulation)
- [ ] T033 [P] [US4] Test token usage extraction from chat completion event in `api/tests/coze/test_chat_client.py` (class TestChatOperations, test_token_usage_extraction)
- [ ] T034 [P] [US4] Test async chat operations using AsyncCoze client in `api/tests/coze/test_chat_client.py` (class TestChatOperations, test_async_create_chat)
- [ ] T035 [US4] Add module-level docstring to `api/tests/coze/test_chat_client.py` explaining chat and conversation test coverage

**Checkpoint**: All chat and conversation operations independently testable with streaming and blocking modes validated

---

## Phase 7: User Story 5 - Workflow Operations Testing (Priority: P4)

**Goal**: Developers can test Coze workflow execution including running workflows, retrieving results, and accessing workflow logs with various filters.

**Independent Test**: Run workflow-specific test suite validating workflow execution modes (blocking/streaming), result retrieval, and log filtering with mocked API responses.

### Tests for User Story 5

**NOTE: These tests validate workflow operations - advanced feature building on core chat capabilities**

- [ ] T036 [P] [US5] Test workflow execution in blocking mode in `api/tests/coze/test_workflow_client.py` (class TestWorkflowOperations, test_run_workflow_blocking)
- [ ] T037 [P] [US5] Test workflow execution in streaming mode in `api/tests/coze/test_workflow_client.py` (class TestWorkflowOperations, test_run_workflow_streaming)
- [ ] T038 [P] [US5] Test workflow result retrieval by workflow_run_id in `api/tests/coze/test_workflow_client.py` (class TestWorkflowOperations, test_get_workflow_result)
- [ ] T039 [P] [US5] Test workflow log listing with default parameters in `api/tests/coze/test_workflow_client.py` (class TestWorkflowOperations, test_list_workflow_logs_default)
- [ ] T040 [P] [US5] Test workflow log filtering by status in `api/tests/coze/test_workflow_client.py` (class TestWorkflowOperations, test_list_workflow_logs_by_status)
- [ ] T041 [P] [US5] Test workflow log filtering by date range in `api/tests/coze/test_workflow_client.py` (class TestWorkflowOperations, test_list_workflow_logs_by_date)
- [ ] T042 [P] [US5] Test workflow log filtering by keyword in `api/tests/coze/test_workflow_client.py` (class TestWorkflowOperations, test_list_workflow_logs_by_keyword)
- [ ] T043 [P] [US5] Test workflow log pagination in `api/tests/coze/test_workflow_client.py` (class TestWorkflowOperations, test_list_workflow_logs_paginated)
- [ ] T044 [P] [US5] Test async workflow operations using AsyncCoze client in `api/tests/coze/test_workflow_client.py` (class TestWorkflowOperations, test_async_run_workflow)
- [ ] T045 [US5] Add module-level docstring to `api/tests/coze/test_workflow_client.py` explaining workflow operations test coverage

**Checkpoint**: All workflow operations independently testable with comprehensive filtering and pagination support

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Documentation, quality validation, and cross-story improvements

- [ ] T046 [P] Create comprehensive test documentation in `api/tests/coze/README.md` following quickstart.md structure (overview, running tests, test organization, key fixtures, coverage goals)
- [ ] T047 [P] Add type hints validation - ensure all test functions and fixtures have complete type annotations
- [ ] T048 Run mypy type checking on `api/tests/coze/` directory with strict mode and verify zero errors
- [ ] T049 Run pytest coverage analysis and verify >= 80% coverage threshold met
- [ ] T050 [P] Verify all test docstrings follow Given/When/Then format
- [ ] T051 Run full test suite and verify execution time < 5 seconds (all mocked, no real API calls)
- [ ] T052 [P] Verify test organization mirrors Dify SDK pattern (compare api/tests/dify/ structure)
- [ ] T053 Validate zero flaky tests by running test suite 5 times consecutively
- [ ] T054 [P] Review and verify all edge cases from spec.md are covered by tests (invalid tokens, network errors, timeouts, etc.)
- [ ] T055 Run ruff linting on `api/tests/coze/` and ensure zero warnings
- [ ] T056 Final verification: Run `uv run pytest api/tests/coze/ -v --cov=api/tests/coze --cov-report=term-missing` and confirm all success criteria met

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-7)**: All depend on Foundational phase completion
  - US1 (P1): Can start after Foundational - No dependencies on other stories
  - US2 (P2): Can start after Foundational - Builds on US1 but independently testable
  - US3 (P3): Can start after Foundational - Independent from US2 and US4
  - US4 (P3): Can start after Foundational - Independent from US2 and US3 (parallel)
  - US5 (P4): Can start after Foundational - Independent from all other stories
- **Polish (Phase 8)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: SDK Installation - Foundation for all tests, must complete first
- **User Story 2 (P2)**: Client Functionality - Extends US1, tests client behavior beyond init
- **User Story 3 (P3)**: Bot Operations - Independent story, can run parallel to US4
- **User Story 4 (P3)**: Chat Operations - Independent story, can run parallel to US3
- **User Story 5 (P4)**: Workflow Operations - Independent advanced feature

### Within Each User Story

- All tests within a story marked [P] can run in parallel (different test classes/methods)
- Module docstrings should be added after all tests in that module are written
- Each story is independently testable and deliverable

### Parallel Opportunities

**Setup Phase**:
- T001 and T002 are sequential (need directory before adding files)

**Foundational Phase** (all can run in parallel):
- T003, T004, T005, T006, T007 all write to same file but different fixtures [P]

**User Story Phases**:
- US1 tests (T009-T013): All [P] - different test classes/methods
- US2 tests (T015-T018): All [P] - different test classes/methods
- US3 tests (T019-T024): All [P] - different test classes/methods
- US4 tests (T026-T034): All [P] - different test classes/methods
- US5 tests (T036-T044): All [P] - different test classes/methods

**Cross-Story Parallelism**:
- After Foundational complete, US3 and US4 can be developed in parallel (both P3, independent)
- US5 can be developed in parallel with any other story

**Polish Phase**:
- T046, T047, T050, T052, T054, T055 all [P] - different files/concerns
- T048, T049, T051, T053, T056 are validation tasks (sequential, depend on prior completion)

---

## Parallel Example: Foundational Phase

```bash
# Launch all fixture creation tasks together (write to conftest.py):
Task T003: "Create authentication fixtures in api/tests/coze/conftest.py"
Task T004: "Create HTTP response fixtures in api/tests/coze/conftest.py"
Task T005: "Create entity ID fixtures in api/tests/coze/conftest.py"
Task T006: "Create sample data fixtures in api/tests/coze/conftest.py"
Task T007: "Create HTTP client mock fixtures in api/tests/coze/conftest.py"
```

## Parallel Example: User Story 3 (Bot Operations)

```bash
# Launch all bot operation tests together:
Task T019: "Test bot listing with pagination (single page)"
Task T020: "Test bot listing with multi-page iteration"
Task T021: "Test bot retrieval by ID with logid"
Task T022: "Test bot listing with workspace ID filtering"
Task T023: "Test bot listing with page_size parameter"
Task T024: "Test async bot operations"
```

## Parallel Example: User Stories 3 and 4 Together

```bash
# Two developers working in parallel on P3 priority stories:
Developer A works on User Story 3 (Bot Operations):
  - Tasks T019-T025 in api/tests/coze/test_bot_client.py

Developer B works on User Story 4 (Chat Operations):
  - Tasks T026-T035 in api/tests/coze/test_chat_client.py

Both stories are independent and can be completed in parallel
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T002)
2. Complete Phase 2: Foundational (T003-T008) - CRITICAL foundation
3. Complete Phase 3: User Story 1 (T009-T014)
4. **STOP and VALIDATE**:
   - Run `uv run pytest api/tests/coze/test_coze_client.py -v`
   - Verify SDK imports work
   - Verify client initialization tests pass
5. **MVP READY**: SDK installed, importable, clients initialize correctly

### Incremental Delivery

1. Complete Setup + Foundational (T001-T008) → Foundation ready
2. Add User Story 1 (T009-T014) → Test independently → **MVP Delivered!**
3. Add User Story 2 (T015-T018) → Test independently → Enhanced client validation
4. Add User Stories 3 & 4 in parallel (T019-T035) → Core SDK operations covered
5. Add User Story 5 (T036-T045) → Advanced workflow features complete
6. Polish (T046-T056) → Production ready with documentation and quality gates

Each story adds value without breaking previous stories.

### Parallel Team Strategy

With multiple developers:

1. **Team completes Setup + Foundational together** (T001-T008)
2. **Once Foundational is done**:
   - Developer A: User Story 1 (T009-T014) - Must complete first (P1)
   - Wait for US1 completion, then:
   - Developer A: User Story 2 (T015-T018)
   - Developer B: User Story 3 (T019-T025) - Can run parallel to US2
   - Developer C: User Story 4 (T026-T035) - Can run parallel to US2 and US3
3. **Advanced features**:
   - Any developer: User Story 5 (T036-T045) - Independent
4. **Team completes Polish together** (T046-T056)

Stories complete and integrate independently.

---

## Notes

- [P] tasks = different files/test classes, no dependencies, can run in parallel
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- This is a test-only feature - no source code implementation tasks needed
- All tests use mocks - no real Coze API calls required
- Commit after each user story phase completion (T014, T018, T025, T035, T045, T056)
- Stop at any checkpoint to validate story independently
- Reference quickstart.md for test patterns and examples
- Reference contracts/test-contracts.md for test requirements
- Follow Dify SDK pattern in api/tests/dify/ for consistency

## Task Summary

- **Total Tasks**: 56
- **Setup Phase**: 2 tasks
- **Foundational Phase**: 6 tasks (BLOCKING - must complete before user stories)
- **User Story 1 (P1)**: 6 tasks - SDK Installation and Configuration
- **User Story 2 (P2)**: 4 tasks - Basic Client Functionality
- **User Story 3 (P3)**: 7 tasks - Bot Operations
- **User Story 4 (P3)**: 10 tasks - Chat and Conversation
- **User Story 5 (P4)**: 10 tasks - Workflow Operations
- **Polish Phase**: 11 tasks - Documentation and quality validation

**Parallel Opportunities**:
- Foundational: 5 tasks can run in parallel (T003-T007)
- US1: 5 test tasks can run in parallel (T009-T013)
- US2: 4 test tasks can run in parallel (T015-T018)
- US3: 6 test tasks can run in parallel (T019-T024)
- US4: 9 test tasks can run in parallel (T026-T034)
- US5: 9 test tasks can run in parallel (T036-T044)
- US3 & US4: Can develop in parallel (both P3, independent)
- Polish: 6 tasks can run in parallel (T046, T047, T050, T052, T054, T055)

**Suggested MVP Scope**: User Story 1 only (T001-T014) = 14 tasks
**Full Implementation**: All 56 tasks for comprehensive test coverage
