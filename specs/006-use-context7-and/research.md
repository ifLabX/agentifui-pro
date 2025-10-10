# Research: Coze Python SDK Integration

**Feature**: Coze Python SDK Integration
**Date**: 2025-10-10
**Status**: Complete

## Executive Summary

Research completed for integrating the Coze Python SDK (cozepy) following the established Dify SDK test pattern. All technical decisions resolved based on Context7 documentation analysis and existing Dify integration patterns.

## Research Areas

### 1. Coze SDK Installation and Configuration

**Decision**: Install cozepy via pip, add to pyproject.toml dependencies section

**Rationale**:
- Official Coze documentation specifies `pip install cozepy` as standard installation method
- Package is publicly available on PyPI
- Compatible with project's uv package manager (uv handles pip packages natively)
- No build dependencies or compilation required

**Alternatives Considered**:
- **Git installation**: Could install from GitHub source, but unnecessary complexity for stable SDK
- **Vendor the SDK**: Would require manual updates and lose automated security patches

**Implementation Details**:
```toml
# api/pyproject.toml
dependencies = [
    # ... existing dependencies
    "cozepy>=0.1.0",  # Coze Python SDK
]
```

### 2. Test Framework and Mocking Strategy

**Decision**: Use pytest with unittest.mock for HTTP mocking, following Dify pattern exactly

**Rationale**:
- Dify tests use `unittest.mock.Mock` and `@patch("requests.request")` successfully
- Coze SDK uses httpx internally (per documentation), but exposes standard request/response interface
- Mock at the HTTP client level (httpx) rather than SDK level for flexibility
- pytest-asyncio already configured for async test support
- Consistency with existing test patterns reduces learning curve

**Alternatives Considered**:
- **pytest-httpx**: Dedicated httpx mocking library
  - Rejected: Adds dependency for marginal benefit over unittest.mock
- **responses library**: Popular HTTP mocking
  - Rejected: Designed for requests library, not httpx
- **vcrpy**: Record/replay HTTP interactions
  - Rejected: Adds complexity, fixtures make tests clearer

**Implementation Pattern**:
```python
from unittest.mock import Mock, patch

@pytest.fixture
def mock_httpx_client():
    """Mock httpx.Client for Coze SDK."""
    with patch("httpx.Client") as mock_client:
        yield mock_client
```

### 3. Test Organization Structure

**Decision**: Mirror Dify test structure: conftest.py + 4 test modules organized by SDK functionality

**Rationale**:
- Dify pattern proven effective: clear separation, easy navigation, good test organization
- Organizing by SDK client type (Coze, Bot, Chat, Workflow) matches SDK's API structure
- conftest.py pattern centralizes fixtures, reducing duplication
- Each test module can have focused test classes for specific operations

**Alternatives Considered**:
- **Single test file**: All tests in test_coze.py
  - Rejected: Would exceed 1000 lines, hard to navigate
- **Organize by operation type**: test_list.py, test_create.py, etc.
  - Rejected: Crosses SDK client boundaries, harder to understand

**File Structure**:
```
api/tests/coze/
├── conftest.py              # Shared fixtures (API keys, mocks, sample data)
├── test_coze_client.py      # Client initialization (sync/async)
├── test_bot_client.py       # Bot operations (list, retrieve, workspace)
├── test_chat_client.py      # Chat and conversation management
├── test_workflow_client.py  # Workflow execution and logs
└── README.md                # Test documentation
```

### 4. Fixture Design for Coze SDK

**Decision**: Create fixtures for API credentials, base URLs, sample IDs, and mock responses

**Rationale**:
- Dify conftest.py provides excellent template with comprehensive fixtures
- Coze SDK requires: API token (COZE_API_TOKEN), base URL (COZE_API_BASE or COZE_CN_BASE_URL)
- Mock responses need to match Coze API response format (includes logid for debugging)
- Sample IDs needed: bot_id, workspace_id, conversation_id, workflow_id, chat_id

**Key Fixtures to Implement**:
```python
@pytest.fixture
def mock_coze_api_token() -> str:
    return "test-coze-token-12345"

@pytest.fixture
def mock_coze_base_url() -> str:
    return "https://api.coze.cn/v1"

@pytest.fixture
def mock_bot_id() -> str:
    return "7379462189365198898"

@pytest.fixture
def mock_workspace_id() -> str:
    return "workspace-12345-abcde"

@pytest.fixture
def mock_successful_response() -> Mock:
    response = Mock()
    response.status_code = 200
    response.json.return_value = {"success": True, "logid": "req-123"}
    return response

@pytest.fixture
def mock_streaming_response() -> Mock:
    """Mock for streaming chat responses."""
    response = Mock()
    response.status_code = 200
    streaming_data = [
        b'event: conversation.message.delta\ndata: {"content": "Hello"}',
        b'event: conversation.chat.completed\ndata: {"status": "completed"}',
    ]
    response.iter_lines = Mock(return_value=iter(streaming_data))
    return response
```

### 5. Async Testing Strategy

**Decision**: Use pytest-asyncio with async fixtures and test functions for AsyncCoze client

**Rationale**:
- Coze SDK provides both sync (Coze) and async (AsyncCoze) clients
- pytest-asyncio already installed and configured (`asyncio_mode = "auto"` in pyproject.toml)
- Async tests critical for validating async/await patterns in SDK usage
- Separate test cases for sync vs async ensures both interfaces work correctly

**Implementation Pattern**:
```python
import pytest
from cozepy import AsyncCoze, AsyncTokenAuth

@pytest.fixture
async def async_coze_client(mock_coze_api_token: str, mock_coze_base_url: str):
    """Async Coze client fixture."""
    client = AsyncCoze(
        auth=AsyncTokenAuth(mock_coze_api_token),
        base_url=mock_coze_base_url
    )
    return client

@pytest.mark.asyncio
async def test_async_list_bots(async_coze_client, mock_workspace_id):
    """Test async bot listing."""
    bots = await async_coze_client.bots.list(space_id=mock_workspace_id)
    # assertions...
```

### 6. Event Handling for Streaming Responses

**Decision**: Test event types (CONVERSATION_MESSAGE_DELTA, CONVERSATION_CHAT_COMPLETED) using iterator pattern

**Rationale**:
- Coze SDK chat streaming returns event iterator with specific event types
- Per documentation, key events are: message.delta (partial content), chat.completed (final)
- Testing must verify both event type recognition and content extraction
- Mock streaming data should match actual Coze API event format

**Event Format (from Coze docs)**:
```
event: conversation.message.delta
data: {"message":{"content":"Hello"}}

event: conversation.chat.completed
data: {"chat":{"status":"completed","usage":{"token_count":633}}}
```

**Test Implementation**:
```python
def test_stream_chat_events(coze_client, mock_streaming_response):
    """Test streaming chat event handling."""
    events = list(coze_client.chat.stream(
        bot_id="bot-123",
        user_id="user-456",
        additional_messages=[Message.build_user_question_text("Hello")]
    ))

    # Verify delta events
    delta_events = [e for e in events if e.event == ChatEventType.CONVERSATION_MESSAGE_DELTA]
    assert len(delta_events) > 0

    # Verify completion event
    completed = [e for e in events if e.event == ChatEventType.CONVERSATION_CHAT_COMPLETED]
    assert len(completed) == 1
    assert completed[0].chat.usage.token_count > 0
```

### 7. mypy Type Checking Compliance

**Decision**: Add type hints to all test functions and mock objects, configure mypy to check test files

**Rationale**:
- Constitution requires Python type hints for all function signatures
- mypy configured with `strict = true` in pyproject.toml
- Current configuration excludes tests directory, but best practice includes type-checked tests
- Type hints in tests serve as documentation and catch type errors early

**Configuration Update**:
```toml
# api/pyproject.toml
[tool.mypy]
files = ["src", "tests/coze"]  # Add Coze tests to type checking
exclude = ["^migrations/", "^\\.venv/"]  # Keep tests/dify excluded for now
```

**Type Hint Pattern**:
```python
from typing import Any
from unittest.mock import Mock
import pytest

@pytest.fixture
def sample_inputs() -> dict[str, Any]:
    """Provide sample input data for testing."""
    return {
        "query": "What is the weather?",
        "context": "User asking about weather"
    }

def test_create_chat(
    coze_client: Coze,
    mock_bot_id: str,
    mock_user_id: str,
    sample_inputs: dict[str, Any]
) -> None:
    """Test chat creation with type-safe fixtures."""
    # test implementation
```

### 8. Test Documentation Standards

**Decision**: Include comprehensive docstrings in all test files and create README.md explaining test structure

**Rationale**:
- Dify tests have excellent docstrings explaining purpose and coverage
- README.md provides quick reference for running tests and understanding organization
- Documentation critical for onboarding and future maintenance
- Success criterion: new developers understand coverage in 10 minutes

**Documentation Structure**:

**Module-level docstring example**:
```python
"""
Tests for Coze Bot Client.

This module tests the bot client functionality including:
- Bot listing with pagination
- Bot retrieval by ID
- Workspace queries
- logid extraction for debugging

All tests use mocks to avoid real API calls.
"""
```

**README.md contents**:
- Quick start: Running tests (`uv run pytest tests/coze/`)
- Test organization: What each file covers
- Fixture reference: Key fixtures and their purpose
- Coverage goals: 80% minimum, current status
- Common patterns: How to add new tests

### 9. Pagination and Iterator Testing

**Decision**: Test pagination using mock page objects with iter_pages() pattern

**Rationale**:
- Coze SDK list operations return paginated results (BotListResponse with iter_pages())
- Must verify both single page retrieval and multi-page iteration
- Mock must simulate realistic pagination behavior (page_num, has_more flags)

**Pagination Test Pattern**:
```python
@pytest.mark.asyncio
async def test_bot_pagination(async_coze_client, mock_workspace_id):
    """Test bot listing pagination."""
    # Mock multi-page response
    mock_page1 = Mock()
    mock_page1.page_num = 1
    mock_page1.has_more = True
    mock_page1.items = [Mock(bot_id="bot-1"), Mock(bot_id="bot-2")]

    mock_page2 = Mock()
    mock_page2.page_num = 2
    mock_page2.has_more = False
    mock_page2.items = [Mock(bot_id="bot-3")]

    mock_response = Mock()
    mock_response.iter_pages = Mock(return_value=async_iter([mock_page1, mock_page2]))

    all_bots = []
    async for page in mock_response.iter_pages():
        all_bots.extend(page.items)

    assert len(all_bots) == 3
```

### 10. HTTP Client Configuration Testing

**Decision**: Test custom HTTP client timeout and logging configuration

**Rationale**:
- Coze SDK supports custom httpx.Client with timeout configuration
- Documentation shows logging setup via setup_logging() function
- Tests should verify these configurations work correctly
- Validates SDK initialization patterns developers will use

**Configuration Test Pattern**:
```python
import httpx
from cozepy import Coze, TokenAuth, SyncHTTPClient, setup_logging

def test_custom_http_client_timeout(mock_coze_api_token):
    """Test Coze client with custom HTTP timeout."""
    http_client = SyncHTTPClient(timeout=httpx.Timeout(
        timeout=600.0,
        connect=5.0
    ))

    client = Coze(
        auth=TokenAuth(token=mock_coze_api_token),
        http_client=http_client
    )

    assert client.http_client.timeout.timeout == 600.0
    assert client.http_client.timeout.connect == 5.0

def test_logging_configuration():
    """Test debug logging setup."""
    import logging
    setup_logging(level=logging.DEBUG)
    # Verify logging level set correctly
    logger = logging.getLogger("cozepy")
    assert logger.level == logging.DEBUG
```

## Best Practices Summary

### From Dify Integration Pattern

1. **Fixture Organization**: Group related fixtures (auth, responses, sample data)
2. **Test Class Organization**: One class per major operation category
3. **Descriptive Test Names**: test_operation_context pattern (e.g., test_create_chat_blocking)
4. **Mock Verification**: Always verify correct endpoints and parameters in API calls
5. **Comprehensive Coverage**: Test default params, edge cases, error scenarios

### From Coze SDK Documentation

1. **Client Initialization**: Test both TokenAuth and AsyncTokenAuth
2. **Base URL Configuration**: Test COZE_COM_BASE_URL and COZE_CN_BASE_URL
3. **Response Structure**: Verify logid presence for debugging support
4. **Event-Driven Architecture**: Test event type enums and iteration patterns
5. **Streaming Best Practices**: Test both blocking and streaming response modes

## Implementation Checklist

- [x] Research Coze SDK installation method
- [x] Determine mocking strategy (httpx mocking)
- [x] Design test structure (mirror Dify pattern)
- [x] Define fixture requirements
- [x] Plan async testing approach
- [x] Design event handling tests
- [x] Plan mypy compliance strategy
- [x] Define documentation standards
- [x] Research pagination patterns
- [x] Plan HTTP client configuration tests

## Dependencies and Tools

**Required Dependencies** (already in project):
- pytest >= 7.0.0
- pytest-asyncio >= 0.21.0
- httpx >= 0.24.0
- mypy >= 1.18.2

**New Dependency**:
- cozepy (Coze Python SDK)

**Development Tools**:
- uv (package management)
- ruff (linting and formatting)
- mypy (type checking)

## Risk Mitigation

### Identified Risks

1. **Coze SDK API Changes**: SDK could update, breaking tests
   - **Mitigation**: Pin cozepy version in pyproject.toml, use `>=version` for flexibility

2. **Mock Divergence**: Mocks may not match real API behavior
   - **Mitigation**: Base mocks on official documentation examples, update with SDK releases

3. **Async Test Flakiness**: Async tests can be unstable
   - **Mitigation**: Use pytest-asyncio auto mode, avoid timing dependencies, use deterministic mocks

4. **Type Hint Complexity**: Mock objects hard to type correctly
   - **Mitigation**: Use `Mock(spec=ClassName)` for better type inference, add `# type: ignore` only when justified

## References

- Coze Python SDK Documentation: https://github.com/coze-dev/coze-py
- Context7 Documentation Snippets: Installation, client initialization, streaming patterns
- Existing Dify Tests: api/tests/dify/ (conftest.py, test_chat_client.py, test_workflow_client.py)
- Project Constitution: .specify/memory/constitution.md
- Project Standards: api/pyproject.toml (pytest config, mypy config)
