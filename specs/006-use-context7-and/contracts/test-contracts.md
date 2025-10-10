# Test Contracts: Coze Python SDK Integration

**Feature**: Coze Python SDK Integration
**Date**: 2025-10-10
**Type**: Test Contracts (Internal Testing API)

## Overview

This document defines the contracts for testing the Coze Python SDK integration. Since this is a test-only feature with no production API endpoints, the "contracts" describe the test interfaces, mock API interactions, and expected behavior patterns that tests must validate.

## Test Contract Principles

1. **Mock Fidelity**: All mocks MUST match actual Coze API response structures from official documentation
2. **Type Safety**: All test functions and fixtures MUST include type hints
3. **Isolation**: Tests MUST NOT make real API calls - all HTTP interactions MUST be mocked
4. **Determinism**: Tests MUST produce consistent results across multiple runs (no flaky tests)
5. **Coverage**: Test suite MUST achieve minimum 80% code coverage

## Test Module Contracts

### 1. conftest.py Contract

**Purpose**: Provide shared test fixtures and configuration for all Coze SDK tests

**Required Fixtures**:

```python
# Authentication Fixtures
def mock_coze_api_token() -> str
def mock_coze_base_url() -> str

# Client Fixtures
def mock_httpx_client() -> Mock
async def mock_async_httpx_client() -> Mock

# Entity ID Fixtures
def mock_bot_id() -> str
def mock_workspace_id() -> str
def mock_conversation_id() -> str
def mock_chat_id() -> str
def mock_workflow_id() -> str
def mock_workflow_run_id() -> str

# Response Fixtures
def mock_successful_response() -> Mock
def mock_error_response() -> Mock
def mock_streaming_response() -> Mock

# Data Fixtures
def sample_user_message() -> dict[str, Any]
def sample_workflow_inputs() -> dict[str, Any]
def sample_bot_data() -> dict[str, Any]
```

**Contract Requirements**:
- All fixtures MUST be importable by test modules
- Response fixtures MUST include `logid` field (Coze API requirement)
- Mock clients MUST use `spec=` parameter for type safety
- All fixtures MUST have type hints

**Validation**:
```python
# Test that verifies conftest contract
def test_conftest_fixtures_available():
    """Verify all required fixtures are available."""
    from tests.coze.conftest import (
        mock_coze_api_token,
        mock_successful_response,
        sample_user_message,
        # ... all other fixtures
    )
    assert callable(mock_coze_api_token)
    # ... assertions for all fixtures
```

---

### 2. test_coze_client.py Contract

**Purpose**: Test Coze client initialization and configuration (sync and async)

**Required Test Cases**:

#### TC-CLIENT-001: Synchronous Client Initialization
```python
def test_sync_client_init(
    mock_coze_api_token: str,
    mock_coze_base_url: str
) -> None:
    """
    GIVEN: Valid API token and base URL
    WHEN: Creating Coze client with TokenAuth
    THEN: Client initializes with correct auth and base_url
    """
```

**Expected Behavior**:
- Client object created successfully
- `client.base_url` matches provided URL
- Authentication configured with TokenAuth

#### TC-CLIENT-002: Asynchronous Client Initialization
```python
@pytest.mark.asyncio
async def test_async_client_init(
    mock_coze_api_token: str,
    mock_coze_base_url: str
) -> None:
    """
    GIVEN: Valid API token and base URL
    WHEN: Creating AsyncCoze client with AsyncTokenAuth
    THEN: Async client initializes with correct auth and base_url
    """
```

**Expected Behavior**:
- AsyncCoze object created successfully
- Async methods available (bots.list returns awaitable)
- AsyncTokenAuth configured correctly

#### TC-CLIENT-003: Custom HTTP Client Configuration
```python
def test_custom_http_client_timeout(
    mock_coze_api_token: str
) -> None:
    """
    GIVEN: Custom HTTP client with timeout settings
    WHEN: Creating Coze client with custom http_client
    THEN: Client uses custom timeout configuration
    """
```

**Expected Behavior**:
- Client accepts custom httpx.Client
- Timeout settings preserved
- Connection timeout configurable separately

#### TC-CLIENT-004: Logging Configuration
```python
def test_logging_setup() -> None:
    """
    GIVEN: Default logging level
    WHEN: Calling setup_logging with DEBUG level
    THEN: Coze SDK logging level is set to DEBUG
    """
```

**Expected Behavior**:
- `setup_logging(level=logging.DEBUG)` configures logger
- Subsequent operations log at DEBUG level

**Contract Requirements**:
- ALL client initialization patterns from Coze docs MUST be tested
- Both sync and async clients MUST be covered
- Type hints required for all test functions
- Minimum 4 test cases covering core initialization patterns

---

### 3. test_bot_client.py Contract

**Purpose**: Test bot operations including listing, retrieval, and workspace queries

**Required Test Cases**:

#### TC-BOT-001: List Bots with Pagination
```python
@pytest.mark.asyncio
async def test_list_bots_paginated(
    async_coze_client: AsyncCoze,
    mock_workspace_id: str,
    mock_paginated_response: Mock
) -> None:
    """
    GIVEN: Workspace with multiple pages of bots
    WHEN: Calling bots.list with workspace_id and page_size
    THEN: Returns paginated bot list with correct page_num and items
    """
```

**Expected Behavior**:
- Returns BotListResponse with page_num, has_more, items
- Pagination parameters (page_size) respected
- Each bot item contains bot_id, name, workspace_id

#### TC-BOT-002: Retrieve Bot by ID
```python
def test_retrieve_bot(
    coze_client: Coze,
    mock_bot_id: str,
    mock_successful_response: Mock
) -> None:
    """
    GIVEN: Valid bot_id
    WHEN: Calling bots.retrieve with bot_id
    THEN: Returns bot details including metadata
    """
```

**Expected Behavior**:
- Returns Bot object with all attributes
- Response includes logid for debugging
- Correct API endpoint called (/bots/{bot_id})

#### TC-BOT-003: Iterate Through Bot Pages
```python
@pytest.mark.asyncio
async def test_iterate_bot_pages(
    async_coze_client: AsyncCoze,
    mock_workspace_id: str,
    mock_multi_page_response: Mock
) -> None:
    """
    GIVEN: Workspace with multiple pages of bots
    WHEN: Iterating through pages with iter_pages()
    THEN: All pages retrieved and all bots collected
    """
```

**Expected Behavior**:
- `async for page in response.iter_pages()` works correctly
- All pages processed until has_more=False
- Total bot count matches expected

**Contract Requirements**:
- Bot listing MUST test pagination (single and multi-page)
- Bot retrieval MUST verify correct ID passed to API
- logid extraction MUST be tested
- Type hints required for all test functions
- Minimum 3 test cases covering list, retrieve, pagination

---

### 4. test_chat_client.py Contract

**Purpose**: Test chat and conversation operations including streaming

**Required Test Cases**:

#### TC-CHAT-001: Create Chat (Blocking Mode)
```python
def test_create_chat_blocking(
    coze_client: Coze,
    mock_bot_id: str,
    mock_user_id: str,
    sample_user_message: dict,
    mock_successful_response: Mock
) -> None:
    """
    GIVEN: Bot ID, user ID, and message
    WHEN: Creating chat with response_mode="blocking"
    THEN: Returns complete chat response with token usage
    """
```

**Expected Behavior**:
- Chat created with blocking response
- Response includes chat_id, conversation_id, status="completed"
- Token usage statistics included (token_count, input_count, output_count)

#### TC-CHAT-002: Create Chat (Streaming Mode)
```python
def test_create_chat_streaming(
    coze_client: Coze,
    mock_bot_id: str,
    mock_user_id: str,
    sample_user_message: dict,
    mock_streaming_response: Mock
) -> None:
    """
    GIVEN: Bot ID, user ID, and message
    WHEN: Creating chat with chat.stream()
    THEN: Returns event iterator with message deltas and completion
    """
```

**Expected Behavior**:
- Returns iterable event stream
- Events include ChatEventType.CONVERSATION_MESSAGE_DELTA
- Final event is ChatEventType.CONVERSATION_CHAT_COMPLETED
- Message content accumulated from delta events

#### TC-CHAT-003: Create Conversation
```python
def test_create_conversation(
    coze_client: Coze,
    mock_successful_response: Mock
) -> None:
    """
    GIVEN: Coze client
    WHEN: Calling conversations.create()
    THEN: Returns conversation object with conversation_id
    """
```

**Expected Behavior**:
- Conversation created successfully
- conversation_id returned and non-empty
- Can be used in subsequent chat calls

#### TC-CHAT-004: List Conversation Messages
```python
def test_list_conversation_messages(
    coze_client: Coze,
    mock_conversation_id: str,
    mock_chat_id: str,
    mock_successful_response: Mock
) -> None:
    """
    GIVEN: Conversation ID and chat ID
    WHEN: Calling chat.messages.list()
    THEN: Returns list of messages in conversation
    """
```

**Expected Behavior**:
- Message list returned
- Messages include role (user/assistant) and content
- Pagination supported (if many messages)

#### TC-CHAT-005: Handle Chat Events
```python
def test_stream_chat_events(
    coze_client: Coze,
    mock_bot_id: str,
    mock_user_id: str,
    mock_streaming_response: Mock
) -> None:
    """
    GIVEN: Streaming chat response
    WHEN: Iterating through chat events
    THEN: Correctly identifies event types and extracts data
    """
```

**Expected Behavior**:
- ChatEventType.CONVERSATION_CHAT_CREATED event detected
- ChatEventType.CONVERSATION_MESSAGE_DELTA events processed
- ChatEventType.CONVERSATION_CHAT_COMPLETED event marks end
- Message content extracted from delta events
- Token usage extracted from completion event

**Contract Requirements**:
- MUST test both blocking and streaming modes
- MUST test conversation creation and message listing
- MUST test all key chat event types
- MUST verify token usage statistics
- Type hints required for all test functions
- Minimum 5 test cases covering chat operations

---

### 5. test_workflow_client.py Contract

**Purpose**: Test workflow execution and log retrieval

**Required Test Cases**:

#### TC-WORKFLOW-001: Run Workflow (Blocking)
```python
def test_run_workflow_blocking(
    coze_client: Coze,
    mock_workflow_id: str,
    sample_workflow_inputs: dict,
    mock_successful_response: Mock
) -> None:
    """
    GIVEN: Workflow ID and inputs
    WHEN: Running workflow with response_mode="blocking"
    THEN: Returns workflow execution result with outputs
    """
```

**Expected Behavior**:
- Workflow executes synchronously
- Returns workflow_run_id
- Status is "succeeded" or "failed"
- Outputs included if successful

#### TC-WORKFLOW-002: Run Workflow (Streaming)
```python
def test_run_workflow_streaming(
    coze_client: Coze,
    mock_workflow_id: str,
    sample_workflow_inputs: dict,
    mock_streaming_response: Mock
) -> None:
    """
    GIVEN: Workflow ID and inputs
    WHEN: Running workflow with workflows.chat.stream()
    THEN: Returns event stream with workflow progress
    """
```

**Expected Behavior**:
- Workflow streams events as it progresses
- Events include status updates
- Final event indicates completion with results

#### TC-WORKFLOW-003: Get Workflow Result
```python
def test_get_workflow_result(
    coze_client: Coze,
    mock_workflow_run_id: str,
    mock_successful_response: Mock
) -> None:
    """
    GIVEN: Workflow run ID
    WHEN: Calling workflows.runs.retrieve()
    THEN: Returns workflow execution details and outputs
    """
```

**Expected Behavior**:
- Retrieves workflow run by ID
- Includes status, inputs, outputs
- Includes execution timestamps

#### TC-WORKFLOW-004: List Workflow Logs
```python
def test_list_workflow_logs(
    coze_client: Coze,
    mock_successful_response: Mock
) -> None:
    """
    GIVEN: Coze client
    WHEN: Calling workflows.runs.list() with filters
    THEN: Returns paginated workflow execution logs
    """
```

**Expected Behavior**:
- Returns list of workflow runs
- Supports pagination
- Supports filtering by status, date range, etc.

**Contract Requirements**:
- MUST test both blocking and streaming workflow execution
- MUST test workflow result retrieval
- MUST test workflow log listing with filters
- Type hints required for all test functions
- Minimum 4 test cases covering workflow operations

---

## Mock API Interaction Contracts

### HTTP Request Contract

All test mocks MUST verify that SDK makes correct HTTP requests:

**Required Verifications**:
1. **Method**: Correct HTTP method (GET, POST, PUT, DELETE)
2. **Endpoint**: Correct API endpoint path
3. **Headers**: Includes authentication header
4. **Body**: Request body matches expected format (for POST/PUT)
5. **Query Parameters**: URL parameters correctly formatted

**Example Verification Pattern**:
```python
def test_endpoint_verification(mock_httpx_client, coze_client):
    """Verify SDK calls correct endpoint with correct method."""
    coze_client.bots.retrieve(bot_id="bot-123")

    # Verify HTTP request
    mock_httpx_client.request.assert_called_once()
    call_args = mock_httpx_client.request.call_args

    assert call_args[0][0] == "GET"  # HTTP method
    assert "/bots/bot-123" in call_args[0][1]  # Endpoint path
    assert call_args[1]["headers"]["Authorization"] == f"Bearer {api_token}"
```

### HTTP Response Contract

All mock responses MUST match Coze API format:

**Success Response Format**:
```json
{
  "data": { /* response payload */ },
  "logid": "req-{unique-id}"
}
```

**Error Response Format**:
```json
{
  "error": "error_code",
  "message": "Human-readable error message",
  "logid": "req-{unique-id}"
}
```

**Streaming Response Format** (Server-Sent Events):
```
event: {event_type}
data: {json_payload}

event: {event_type}
data: {json_payload}
```

### Type Hint Contract

All test functions MUST include complete type hints:

**Function Signatures**:
```python
def test_example(
    fixture1: str,
    fixture2: Mock,
    fixture3: dict[str, Any]
) -> None:
    """Test docstring."""
    # test implementation
```

**Fixture Signatures**:
```python
@pytest.fixture
def example_fixture() -> dict[str, str]:
    """Fixture docstring."""
    return {"key": "value"}

@pytest.fixture
async def async_fixture() -> Mock:
    """Async fixture docstring."""
    return Mock()
```

## Test Execution Contract

### Running Tests

**Command**: `uv run pytest tests/coze/`

**Expected Behavior**:
- All tests execute in < 5 seconds (mocked, no real API calls)
- Zero test failures
- Zero flaky tests (consistent results across runs)
- Coverage report shows >= 80% coverage

### Test Output Contract

**Successful Test Run**:
```
tests/coze/test_coze_client.py ....                [ 20%]
tests/coze/test_bot_client.py ...                  [ 40%]
tests/coze/test_chat_client.py .....               [ 65%]
tests/coze/test_workflow_client.py ....            [100%]

======= 30 passed in 4.23s =======
Coverage: 85%
```

**Test Failure Format**:
```
FAILED tests/coze/test_chat_client.py::test_create_chat_blocking
AssertionError: Expected chat_id in response, got None
```

## Coverage Contract

### Minimum Coverage Requirements

- **Overall**: 80% minimum coverage for all test code
- **Per Module**: Each test module should aim for 90%+ coverage of its focus area
- **Critical Paths**: 100% coverage for client initialization, authentication, core operations

### Excluded from Coverage

- Mock object internals (httpx.Client mocking code)
- Type checking annotations
- Docstrings

## Type Checking Contract

### mypy Compliance

**Command**: `uv run mypy tests/coze/`

**Expected Behavior**:
- Zero type errors
- All fixtures have return type hints
- All test functions have parameter and return type hints
- Mock objects use `spec=` parameter where applicable

**Allowed Exceptions**:
- `# type: ignore[arg-type]` for Mock objects where spec doesn't match perfectly
- Must be documented with comment explaining why type ignore is necessary

## Documentation Contract

### Test Module Docstrings

**Required Format**:
```python
"""
Tests for {Component Name}.

This module tests the {component} functionality including:
- {Feature 1}
- {Feature 2}
- {Feature 3}

All tests use mocks to avoid real API calls.
"""
```

### Test Function Docstrings

**Required Format**:
```python
def test_specific_behavior(fixtures) -> None:
    """
    Test {specific behavior}.

    GIVEN: {initial conditions}
    WHEN: {action performed}
    THEN: {expected outcome}
    """
```

## README.md Contract

**Required Sections**:
1. **Overview**: What the tests cover
2. **Running Tests**: How to execute test suite
3. **Test Organization**: File structure explanation
4. **Key Fixtures**: Reference of important fixtures
5. **Adding New Tests**: Guide for contributing tests
6. **Coverage Goals**: Current and target coverage

## Compliance Validation

### Contract Validation Test

Create `test_contracts.py` to validate contract compliance:

```python
"""Validate that tests comply with defined contracts."""

def test_all_fixtures_have_type_hints():
    """Verify all fixtures in conftest.py have type hints."""
    # Implementation that inspects conftest.py fixtures

def test_all_test_functions_have_docstrings():
    """Verify all test functions have Given/When/Then docstrings."""
    # Implementation that checks test function docstrings

def test_minimum_test_count_per_module():
    """Verify each test module has minimum required test cases."""
    # TC-CLIENT: >= 4 tests
    # TC-BOT: >= 3 tests
    # TC-CHAT: >= 5 tests
    # TC-WORKFLOW: >= 4 tests

def test_coverage_meets_minimum():
    """Verify test coverage meets 80% minimum."""
    # Run coverage and validate threshold
```

## Summary

These test contracts ensure:

1. **Consistency**: All tests follow same patterns and conventions
2. **Completeness**: All SDK functionality has corresponding tests
3. **Quality**: Type safety, documentation, and coverage requirements met
4. **Maintainability**: Clear structure makes tests easy to update
5. **Reliability**: Mocks ensure deterministic, fast test execution

All test implementation MUST comply with these contracts to ensure the test suite meets project quality standards and provides reliable validation of Coze SDK integration.
