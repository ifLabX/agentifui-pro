# Quickstart: Coze Python SDK Integration Testing

**Feature**: Coze Python SDK Integration
**Audience**: Developers implementing or maintaining Coze SDK tests
**Estimated Time**: 15 minutes

## What You'll Learn

This quickstart guide will help you:
1. Understand the Coze SDK test suite structure
2. Run the complete test suite
3. Add a new test case
4. Understand the mocking patterns used
5. Verify test coverage and type checking

## Prerequisites

- Python 3.12+ installed
- `uv` package manager configured
- Access to `api/` directory in monorepo
- Familiarity with pytest and basic Python testing

## Step 1: Install Dependencies

The Coze SDK and all testing dependencies are managed through `pyproject.toml`.

```bash
cd api

# Install all dependencies including cozepy
uv sync

# Verify installation
uv run python -c "import cozepy; print(cozepy.__version__)"
```

**Expected Output**: Coze SDK version number (e.g., "0.1.0")

## Step 2: Explore Test Structure

Navigate to the test directory:

```bash
cd tests/coze
ls -la
```

**You should see**:
```
conftest.py              # Shared test fixtures
test_coze_client.py      # Client initialization tests
test_bot_client.py       # Bot operations tests
test_chat_client.py      # Chat and conversation tests
test_workflow_client.py  # Workflow execution tests
README.md                # Detailed test documentation
```

### Quick Tour of conftest.py

Open `conftest.py` to see the shared fixtures:

```python
# Authentication fixtures
mock_coze_api_token()    # Returns "test-coze-token-12345"
mock_coze_base_url()     # Returns "https://api.coze.cn/v1"

# Response fixtures
mock_successful_response()  # 200 OK with sample data
mock_error_response()       # 400 Bad Request
mock_streaming_response()   # Streaming chat events

# Entity ID fixtures
mock_bot_id()            # Sample bot ID
mock_workspace_id()      # Sample workspace ID
mock_conversation_id()   # Sample conversation ID
```

## Step 3: Run the Test Suite

### Run All Tests

```bash
cd api
uv run pytest tests/coze/ -v
```

**Expected Output**:
```
tests/coze/test_coze_client.py::test_sync_client_init PASSED
tests/coze/test_coze_client.py::test_async_client_init PASSED
tests/coze/test_bot_client.py::test_list_bots PASSED
tests/coze/test_chat_client.py::test_create_chat_blocking PASSED
tests/coze/test_chat_client.py::test_create_chat_streaming PASSED
tests/coze/test_workflow_client.py::test_run_workflow PASSED

======= 30 passed in 4.23s =======
```

### Run Specific Test Module

```bash
# Run only client initialization tests
uv run pytest tests/coze/test_coze_client.py -v

# Run only chat tests
uv run pytest tests/coze/test_chat_client.py -v
```

### Run with Coverage

```bash
uv run pytest tests/coze/ --cov=tests/coze --cov-report=term-missing
```

**Expected Output**:
```
Name                           Stmts   Miss  Cover   Missing
------------------------------------------------------------
tests/coze/conftest.py            45      2    96%   78-79
tests/coze/test_coze_client.py    32      0   100%
tests/coze/test_bot_client.py     28      1    96%   42
tests/coze/test_chat_client.py    56      3    95%   89-91
tests/coze/test_workflow_client.py 38     2    95%   54-55
------------------------------------------------------------
TOTAL                            199     8    96%
```

## Step 4: Understand a Test Case

Let's examine a simple test from `test_coze_client.py`:

```python
def test_sync_client_init(
    mock_coze_api_token: str,
    mock_coze_base_url: str
) -> None:
    """
    Test synchronous Coze client initialization.

    GIVEN: Valid API token and base URL
    WHEN: Creating Coze client with TokenAuth
    THEN: Client initializes with correct auth and base_url
    """
    from cozepy import Coze, TokenAuth

    # Create client
    client = Coze(
        auth=TokenAuth(mock_coze_api_token),
        base_url=mock_coze_base_url
    )

    # Verify initialization
    assert client is not None
    assert client.base_url == mock_coze_base_url
```

**Key Patterns**:
1. **Type Hints**: All parameters and return types annotated
2. **Given/When/Then**: Docstring follows BDD format
3. **Fixtures**: Uses shared fixtures from conftest.py
4. **Assertions**: Clear, specific assertions about expected behavior

## Step 5: Add a New Test

Let's add a test to verify bot retrieval with logid extraction.

### 5.1: Open test_bot_client.py

```bash
vi tests/coze/test_bot_client.py
```

### 5.2: Add New Test Function

Add this test to the `TestBotOperations` class (or similar):

```python
def test_retrieve_bot_with_logid(
    coze_client: Coze,
    mock_bot_id: str,
    mock_successful_response: Mock
) -> None:
    """
    Test bot retrieval and logid extraction.

    GIVEN: Valid bot ID
    WHEN: Retrieving bot details
    THEN: Response includes bot data and logid for debugging
    """
    # Configure mock response
    mock_successful_response.json.return_value = {
        "data": {
            "bot_id": mock_bot_id,
            "name": "Test Bot",
            "workspace_id": "workspace-123"
        },
        "logid": "req-12345-abcde"
    }

    # Mock the HTTP client
    with patch("httpx.Client.request", return_value=mock_successful_response):
        # Retrieve bot
        bot = coze_client.bots.retrieve(bot_id=mock_bot_id)

        # Verify bot data
        assert bot.bot_id == mock_bot_id
        assert bot.name == "Test Bot"

        # Verify logid is accessible
        assert bot.response.logid == "req-12345-abcde"
```

### 5.3: Run Your New Test

```bash
uv run pytest tests/coze/test_bot_client.py::test_retrieve_bot_with_logid -v
```

**Expected Output**:
```
tests/coze/test_bot_client.py::test_retrieve_bot_with_logid PASSED [100%]
```

## Step 6: Understand Mocking Patterns

### Pattern 1: Mock HTTP Responses

The most common pattern - mock the HTTP layer:

```python
from unittest.mock import Mock, patch

@pytest.fixture
def mock_successful_response() -> Mock:
    """Mock successful HTTP response."""
    response = Mock(spec=httpx.Response)
    response.status_code = 200
    response.json.return_value = {
        "data": {"result": "success"},
        "logid": "req-123"
    }
    return response

def test_with_mocked_response(mock_successful_response):
    with patch("httpx.Client.request", return_value=mock_successful_response):
        # Test code that makes HTTP requests
        pass
```

### Pattern 2: Mock Streaming Responses

For testing chat streaming:

```python
@pytest.fixture
def mock_streaming_response() -> Mock:
    """Mock streaming HTTP response."""
    response = Mock(spec=httpx.Response)
    response.status_code = 200
    response.headers = {"Content-Type": "text/event-stream"}

    # Mock Server-Sent Events format
    streaming_data = [
        b'event: conversation.message.delta\ndata: {"content":"Hello"}',
        b'event: conversation.chat.completed\ndata: {"status":"completed"}',
    ]
    response.iter_lines = Mock(return_value=iter(streaming_data))
    return response
```

### Pattern 3: Async Test Fixtures

For testing AsyncCoze client:

```python
import pytest

@pytest.fixture
async def async_coze_client(
    mock_coze_api_token: str,
    mock_coze_base_url: str
):
    """Async Coze client fixture."""
    from cozepy import AsyncCoze, AsyncTokenAuth

    client = AsyncCoze(
        auth=AsyncTokenAuth(mock_coze_api_token),
        base_url=mock_coze_base_url
    )
    return client

@pytest.mark.asyncio
async def test_async_operation(async_coze_client):
    """Test async SDK operation."""
    result = await async_coze_client.bots.list(space_id="workspace-123")
    assert result is not None
```

## Step 7: Verify Type Checking

Run mypy to ensure all tests pass type checking:

```bash
cd api
uv run mypy tests/coze/
```

**Expected Output**:
```
Success: no issues found in 5 source files
```

**Common Type Issues and Fixes**:

```python
# ❌ Missing type hint
def test_example(fixture):
    pass

# ✅ With type hint
def test_example(fixture: str) -> None:
    pass

# ❌ Untyped Mock
mock_obj = Mock()

# ✅ Typed Mock with spec
mock_obj = Mock(spec=httpx.Response)

# ❌ Untyped fixture
@pytest.fixture
def example():
    return {"key": "value"}

# ✅ Typed fixture
@pytest.fixture
def example() -> dict[str, str]:
    return {"key": "value"}
```

## Step 8: Check Code Quality

Run all quality checks (linting, formatting, type checking):

```bash
cd api

# Lint with ruff
uv run ruff check tests/coze/

# Format with ruff
uv run ruff format tests/coze/

# Type check with mypy
uv run mypy tests/coze/

# Run all checks together
uv run ruff check tests/coze/ && \
uv run mypy tests/coze/ && \
uv run pytest tests/coze/ --cov=tests/coze
```

## Common Tasks

### Add a New Fixture

1. Open `conftest.py`
2. Add fixture function with type hint:

```python
@pytest.fixture
def sample_new_data() -> dict[str, Any]:
    """Provide sample data for new feature."""
    return {
        "field1": "value1",
        "field2": 123,
        "field3": ["item1", "item2"]
    }
```

3. Use in tests:

```python
def test_new_feature(sample_new_data: dict[str, Any]) -> None:
    """Test new feature with sample data."""
    assert sample_new_data["field1"] == "value1"
```

### Debug a Failing Test

1. **Run with verbose output**:
   ```bash
   uv run pytest tests/coze/test_chat_client.py::test_failing -vv
   ```

2. **Add print debugging** (temporary):
   ```python
   def test_failing(fixture):
       result = some_operation()
       print(f"DEBUG: result = {result}")  # Remove before commit
       assert result == expected
   ```

3. **Use pytest's built-in debugger**:
   ```bash
   uv run pytest tests/coze/test_chat_client.py::test_failing --pdb
   ```

### Test a Specific Scenario

Use parametrize for testing multiple scenarios:

```python
import pytest

@pytest.mark.parametrize("status,expected", [
    ("created", True),
    ("in_progress", True),
    ("completed", True),
    ("failed", False),
])
def test_chat_status_validation(status: str, expected: bool) -> None:
    """Test different chat status values."""
    is_active = status in ["created", "in_progress", "completed"]
    assert is_active == expected
```

## Quick Reference

### Essential Commands

```bash
# Run all tests
uv run pytest tests/coze/

# Run with coverage
uv run pytest tests/coze/ --cov=tests/coze --cov-report=html

# Run specific test
uv run pytest tests/coze/test_chat_client.py::test_create_chat_blocking

# Run tests matching pattern
uv run pytest tests/coze/ -k "chat"

# Run with verbose output
uv run pytest tests/coze/ -v

# Run type checking
uv run mypy tests/coze/

# Run linting
uv run ruff check tests/coze/
```

### Important Files

| File | Purpose |
|------|---------|
| `conftest.py` | Shared fixtures and test configuration |
| `test_coze_client.py` | Client initialization tests |
| `test_bot_client.py` | Bot operations tests |
| `test_chat_client.py` | Chat and conversation tests |
| `test_workflow_client.py` | Workflow execution tests |
| `README.md` | Comprehensive test documentation |

### Key Fixtures

| Fixture | Type | Purpose |
|---------|------|---------|
| `mock_coze_api_token` | str | Test API token |
| `mock_coze_base_url` | str | Test API base URL |
| `mock_bot_id` | str | Sample bot identifier |
| `mock_successful_response` | Mock | 200 OK HTTP response |
| `mock_streaming_response` | Mock | Streaming chat response |
| `sample_user_message` | dict | Sample chat message data |

## Next Steps

After completing this quickstart:

1. **Read Full Documentation**: Check `README.md` for comprehensive details
2. **Explore Data Model**: Review `data-model.md` for entity structures
3. **Study Contracts**: Read `contracts/test-contracts.md` for test requirements
4. **Review Research**: Check `research.md` for implementation decisions
5. **Examine Dify Tests**: Compare with `tests/dify/` for consistency

## Troubleshooting

### Issue: Tests fail with import errors

**Solution**: Ensure SDK is installed
```bash
cd api
uv sync
uv run python -c "import cozepy"
```

### Issue: Type checking fails on Mock objects

**Solution**: Add `spec=` parameter to Mock
```python
# Before
mock = Mock()

# After
mock = Mock(spec=httpx.Response)
```

### Issue: Coverage below 80%

**Solution**: Identify untested code
```bash
uv run pytest tests/coze/ --cov=tests/coze --cov-report=term-missing
# Look for "Missing" column to see uncovered lines
```

### Issue: Async tests not running

**Solution**: Verify pytest-asyncio configuration
```bash
# Check pyproject.toml has:
# [tool.pytest.ini_options]
# asyncio_mode = "auto"

# Ensure test uses @pytest.mark.asyncio
@pytest.mark.asyncio
async def test_async_function():
    pass
```

## Getting Help

- **Test Documentation**: `tests/coze/README.md`
- **Project Constitution**: `.specify/memory/constitution.md`
- **Coze SDK Docs**: https://github.com/coze-dev/coze-py
- **pytest Documentation**: https://docs.pytest.org/

## Summary

You've learned how to:
- ✅ Run the Coze SDK test suite
- ✅ Understand test structure and organization
- ✅ Add new test cases following project patterns
- ✅ Use mocking patterns for HTTP interactions
- ✅ Verify test coverage and type checking
- ✅ Debug and troubleshoot test issues

**Time to implement**: Start adding comprehensive tests following these patterns!
