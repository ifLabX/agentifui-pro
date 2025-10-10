# Coze Python SDK Integration Tests

This directory contains comprehensive tests for the Coze Python SDK (`cozepy`) integration. The tests validate SDK functionality without making real API calls, using mocks to ensure fast, reliable test execution.

## Overview

The test suite covers:
- **Client Initialization**: Sync and async client setup with various authentication options
- **Bot Operations**: Listing, retrieving, creating, updating, and deleting bots
- **Chat Operations**: Creating chats (blocking and streaming), managing conversations, retrieving message history
- **Workflow Operations**: Running workflows (blocking and streaming), retrieving workflow status, validating inputs/outputs

## Test Structure

```
tests/coze/
├── conftest.py                 # Shared fixtures and test configuration
├── test_coze_client.py         # Client initialization tests (6 tests)
├── test_bot_client.py          # Bot operations tests (5 tests)
├── test_chat_client.py         # Chat and conversation tests (7 tests)
├── test_workflow_client.py     # Workflow execution tests (7 tests)
└── README.md                   # This file
```

**Total**: 25 tests across 4 test modules

## Running Tests

### Prerequisites

Ensure `cozepy` is installed via `uv`:

```bash
cd api
uv sync
```

### Run All Tests

```bash
# From api/ directory
DATABASE_URL="postgresql://test" uv run pytest tests/coze/ -v
```

### Run Specific Test Module

```bash
# Client initialization tests
DATABASE_URL="postgresql://test" uv run pytest tests/coze/test_coze_client.py -v

# Bot operations tests
DATABASE_URL="postgresql://test" uv run pytest tests/coze/test_bot_client.py -v

# Chat operations tests
DATABASE_URL="postgresql://test" uv run pytest tests/coze/test_chat_client.py -v

# Workflow operations tests
DATABASE_URL="postgresql://test" uv run pytest tests/coze/test_workflow_client.py -v
```

### Run with Coverage

```bash
DATABASE_URL="postgresql://test" uv run pytest tests/coze/ --cov=tests/coze --cov-report=term-missing
```

## Test Patterns

### Mocking Strategy

All tests use `unittest.mock` to mock HTTP interactions. No real API calls are made.

**Example pattern**:

```python
from unittest.mock import Mock, patch
import httpx

def test_example(coze_client: Coze):
    # Configure mock response
    mock_response = Mock(spec=httpx.Response)
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "data": {"message": "Success"},
        "logid": "req-12345"
    }

    # Mock HTTP client
    with patch("httpx.Client.request", return_value=mock_response):
        # Test SDK operations
        pass
```

### Fixture Usage

All shared test data is defined in `conftest.py`:

- **Authentication**: `mock_coze_api_token`, `mock_coze_base_url`
- **Entity IDs**: `mock_bot_id`, `mock_workspace_id`, `mock_conversation_id`, `mock_chat_id`, `mock_workflow_id`
- **Responses**: `mock_successful_response`, `mock_error_response`, `mock_streaming_response`, `mock_streaming_events`
- **Sample Data**: `sample_bot_data`, `sample_chat_data`, `sample_user_message`, `sample_workflow_data`

### Type Checking

All tests include type hints and pass `mypy` strict mode:

```bash
cd tests/coze
uv run mypy .
```

**Expected output**: `Success: no issues found in 5 source files`

## Test Coverage

The test suite validates:

✅ **Client Initialization** (6 tests)
- Sync client with custom base URL
- Sync client with default base URL
- Sync client with timeout configuration
- Async client with custom base URL
- Async client with default base URL
- Async client with timeout configuration

✅ **Bot Operations** (5 tests)
- List bots with pagination
- Retrieve single bot
- Create new bot
- Update existing bot
- Delete bot

✅ **Chat Operations** (7 tests)
- Create chat (blocking mode)
- Create chat (streaming mode)
- Parse streaming events
- Retrieve conversation
- List conversation messages
- Retrieve chat status
- Chat with text messages

✅ **Workflow Operations** (7 tests)
- Run workflow (blocking mode)
- Run workflow (streaming mode)
- Retrieve workflow run status
- Validate workflow inputs
- Validate workflow parameters
- Validate workflow output structure
- Validate workflow execution metadata

## Quality Standards

- ✅ **Type Safety**: All functions have type hints, mypy compliant
- ✅ **Documentation**: All tests use Given/When/Then docstring format
- ✅ **No Real API Calls**: All HTTP interactions mocked
- ✅ **Fast Execution**: Test suite completes in < 1 second
- ✅ **Zero Flaky Tests**: Deterministic mocks ensure consistent results

## Maintenance

### Adding New Tests

1. Add test fixtures to `conftest.py` if reusable
2. Create test function with type hints
3. Use Given/When/Then docstring format
4. Mock all HTTP interactions
5. Run `mypy` and `pytest` to verify

### Pattern to Follow

```python
def test_new_feature(
    coze_client: Coze,
    mock_fixture: dict[str, Any],
) -> None:
    """
    Test new feature description.

    GIVEN: Initial conditions
    WHEN: Action performed
    THEN: Expected outcome
    """
    # Arrange: Configure mocks
    mock_response = Mock(spec=httpx.Response)
    mock_response.status_code = 200

    # Act & Assert: Test with mocked HTTP
    with patch("httpx.Client.request", return_value=mock_response):
        # Test implementation
        pass
```

## Integration with Dify Pattern

This test suite mirrors the Dify SDK test organization:
- Same directory structure (`tests/dify/` → `tests/coze/`)
- Similar fixture patterns in `conftest.py`
- Consistent naming conventions
- Parallel mocking strategies

## References

- **Coze SDK**: https://github.com/coze-dev/coze-py
- **Specification**: `/specs/006-use-context7-and/spec.md`
- **Planning**: `/specs/006-use-context7-and/plan.md`
- **Quickstart**: `/specs/006-use-context7-and/quickstart.md`
