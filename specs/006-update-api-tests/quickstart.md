# Quickstart: httpx Async Test Migration

**Feature**: Update Dify SDK Test Suite for httpx Migration
**Date**: 2025-10-11

## Overview

This quickstart guide provides step-by-step instructions for migrating the Dify SDK test suite from `requests`-based mocking to `httpx.AsyncClient` async patterns using pytest-httpx.

## Prerequisites

- Python 3.12+
- Existing test suite in `api/tests/dify/`
- dify-python-sdk 0.1.15 installed
- Basic understanding of async/await and pytest

## Quick Setup (5 minutes)

### 1. Install Dependencies

Add pytest-httpx to development dependencies:

```bash
cd api
uv add --dev "pytest-httpx>=0.30.0"
```

### 2. Configure pytest for Async

Create or update `api/pytest.ini`:

```ini
[pytest]
asyncio_mode = auto
asyncio_default_fixture_loop_scope = function
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
```

### 3. Verify Setup

```bash
cd api
uv run pytest tests/dify/test_dify_client.py::TestDifyClientInitialization --collect-only
```

You should see test discovery without errors (tests will fail until migration).

## Migration Process

### Step 1: Update conftest.py (30 minutes)

**File**: `api/tests/dify/conftest.py`

#### Remove Old Imports

```python
# REMOVE these
import requests
from unittest.mock import Mock, patch

@pytest.fixture
def mock_requests_request() -> Generator[Mock, None, None]:
    with patch("requests.request") as mock_request:
        yield mock_request

@pytest.fixture
def mock_successful_response() -> Mock:
    response = Mock(spec=requests.Response)
    # ...
```

#### Add New Imports

```python
# ADD these
from pytest_httpx import HTTPXMock
```

#### Keep Existing Fixtures

All sample data fixtures remain unchanged:
- `mock_api_key()`
- `mock_base_url()`
- `mock_user()`
- `sample_inputs()`
- `sample_files()`
- `sample_conversation_id()`
- etc.

**Note**: The `httpx_mock` fixture is automatically provided by pytest-httpx. No need to define it.

### Step 2: Migrate One Test File (2 hours per file)

Let's start with `test_dify_client.py` as an example.

#### Before (Synchronous with requests)

```python
from unittest.mock import Mock
from dify_client import DifyClient

class TestDifyClientInitialization:
    def test_client_initialization(
        self,
        mock_api_key: str,
    ) -> None:
        """Test that DifyClient initializes correctly."""
        client = DifyClient(api_key=mock_api_key)

        assert client.api_key == mock_api_key
        assert hasattr(client, "base_url")
```

#### After (Asynchronous with httpx)

```python
from dify_client import DifyClient
from pytest_httpx import HTTPXMock

class TestDifyClientInitialization:
    async def test_client_initialization(
        self,
        mock_api_key: str,
    ) -> None:
        """Test that DifyClient initializes correctly."""
        client = DifyClient(api_key=mock_api_key)

        assert client.api_key == mock_api_key
        assert hasattr(client, "base_url")
```

**Changes**:
1. Changed `def test_*` to `async def test_*`
2. Removed `Mock` import (no longer needed)
3. Test logic unchanged (initialization doesn't make HTTP calls)

#### Example: HTTP Method Test

**Before**:
```python
def test_create_message(
    self,
    mock_api_key: str,
    mock_requests_request: Mock,
    mock_successful_response: Mock,
    sample_inputs: dict,
    mock_user: str,
) -> None:
    mock_requests_request.return_value = mock_successful_response

    client = ChatClient(api_key=mock_api_key)
    response = client.create_chat_message(
        inputs=sample_inputs,
        query="Test query",
        user=mock_user,
    )

    mock_requests_request.assert_called_once()
    assert response == mock_successful_response
```

**After**:
```python
async def test_create_message(
    self,
    mock_api_key: str,
    httpx_mock: HTTPXMock,
    sample_inputs: dict,
    mock_user: str,
) -> None:
    # Configure expected response
    httpx_mock.add_response(
        url="https://api.dify.ai/v1/chat-messages",
        method="POST",
        json={"success": True, "message_id": "msg-123"},
        status_code=200,
    )

    client = ChatClient(api_key=mock_api_key)
    response = await client.create_chat_message(
        inputs=sample_inputs,
        query="Test query",
        user=mock_user,
    )

    # Verify request was made
    requests = httpx_mock.get_requests()
    assert len(requests) == 1
    assert requests[0].method == "POST"

    # Verify response
    assert response.status_code == 200
    assert response.json()["success"] is True
```

**Changes**:
1. `async def test_*` and `await` for async client call
2. Removed `mock_requests_request` and `mock_successful_response` fixtures
3. Added `httpx_mock: HTTPXMock` fixture
4. Configured response with `httpx_mock.add_response()`
5. Used `await` with client method
6. Changed assertions to use `httpx_mock.get_requests()`
7. Response verification uses `response.status_code` and `response.json()`

### Step 3: Run Tests Incrementally

After migrating each file, run tests to verify:

```bash
cd api
uv run pytest tests/dify/test_dify_client.py -v
```

Expected output:
```
tests/dify/test_dify_client.py::TestDifyClientInitialization::test_client_initialization PASSED
tests/dify/test_dify_client.py::TestDifyClientCreateMessage::test_create_message PASSED
...
```

### Step 4: Migrate Remaining Files

Repeat Step 2 for each test file:

1. ✅ `test_dify_client.py` (base client - start here)
2. `test_chat_client.py` (chat operations)
3. `test_completion_client.py` (completion operations)
4. `test_workflow_client.py` (workflow operations)
5. `test_knowledge_base_client.py` (knowledge base operations)
6. `test_workspace_client.py` (workspace operations)

**Estimated time**: 2 hours per file × 6 files = 12 hours total

### Step 5: Final Validation

Run the full test suite:

```bash
cd api
uv run pytest tests/dify/ -v --cov=tests/dify
```

Verify:
- ✅ All tests pass (100% success rate)
- ✅ No import errors or async-related errors
- ✅ Coverage ≥80%
- ✅ No warnings about event loops or pytest-asyncio

## Common Patterns

### Pattern 1: Simple GET Request

```python
async def test_get_operation(
    httpx_mock: HTTPXMock,
    mock_api_key: str,
) -> None:
    httpx_mock.add_response(
        url="https://api.dify.ai/v1/resource",
        method="GET",
        json={"data": "value"},
    )

    client = Client(api_key=mock_api_key)
    response = await client.get_resource()

    assert response.json()["data"] == "value"
```

### Pattern 2: POST with Request Body Validation

```python
async def test_post_operation(
    httpx_mock: HTTPXMock,
    mock_api_key: str,
) -> None:
    httpx_mock.add_response(
        url="https://api.dify.ai/v1/create",
        method="POST",
        json={"id": "new-123"},
    )

    client = Client(api_key=mock_api_key)
    await client.create_resource(name="test")

    # Verify request body
    request = httpx_mock.get_request()
    assert request.method == "POST"
    assert request.read() == b'{"name": "test"}'
```

### Pattern 3: Error Response Handling

```python
async def test_error_handling(
    httpx_mock: HTTPXMock,
    mock_api_key: str,
) -> None:
    httpx_mock.add_response(
        url="https://api.dify.ai/v1/invalid",
        method="GET",
        json={"error": "Not Found"},
        status_code=404,
    )

    client = Client(api_key=mock_api_key)

    with pytest.raises(httpx.HTTPStatusError) as exc_info:
        await client.get_invalid()

    assert exc_info.value.response.status_code == 404
```

### Pattern 4: Streaming Response

```python
async def test_streaming(
    httpx_mock: HTTPXMock,
    mock_api_key: str,
) -> None:
    httpx_mock.add_response(
        url="https://api.dify.ai/v1/stream",
        method="POST",
        content=b'data: {"chunk": 1}\ndata: {"chunk": 2}\n',
        headers={"Content-Type": "text/event-stream"},
    )

    client = Client(api_key=mock_api_key)
    chunks = []

    async for line in client.stream_data():
        chunks.append(line)

    assert len(chunks) == 2
```

### Pattern 5: Multiple Requests in One Test

```python
async def test_multiple_operations(
    httpx_mock: HTTPXMock,
    mock_api_key: str,
) -> None:
    # Configure multiple responses in order
    httpx_mock.add_response(
        url="https://api.dify.ai/v1/first",
        json={"step": 1},
    )
    httpx_mock.add_response(
        url="https://api.dify.ai/v1/second",
        json={"step": 2},
    )

    client = Client(api_key=mock_api_key)

    response1 = await client.first_operation()
    assert response1.json()["step"] == 1

    response2 = await client.second_operation()
    assert response2.json()["step"] == 2

    # Verify both requests were made
    requests = httpx_mock.get_requests()
    assert len(requests) == 2
```

## Troubleshooting

### Issue: "RuntimeError: no running event loop"

**Cause**: Test method is not `async def`

**Fix**: Change `def test_*` to `async def test_*`

---

### Issue: "TypeError: object Mock can't be used in 'await' expression"

**Cause**: Using old `Mock` objects with async methods

**Fix**: Remove manual `Mock` creation, use `httpx_mock` fixture instead

---

### Issue: "AttributeError: 'HTTPXMock' object has no attribute 'return_value'"

**Cause**: Trying to use `requests.Mock` patterns with `httpx_mock`

**Fix**: Use `httpx_mock.add_response()` instead of `mock.return_value`

---

### Issue: Tests pass but pytest-asyncio warnings appear

**Cause**: Missing or incorrect pytest.ini configuration

**Fix**: Ensure `asyncio_mode = auto` is set in `pytest.ini`

---

### Issue: "httpx.InvalidURL: URL too short"

**Cause**: URL in `add_response()` doesn't match actual SDK request URL

**Fix**: Check SDK source code to find exact URL being requested

---

## Next Steps

After completing the migration:

1. **Update agent context** (automatically done by `/speckit.plan`):
   ```bash
   .specify/scripts/bash/update-agent-context.sh claude
   ```

2. **Run full test suite**:
   ```bash
   cd api
   uv run pytest tests/dify/ -v --cov
   ```

3. **Verify coverage**:
   - Ensure ≥80% coverage maintained
   - Check for any untested async branches

4. **Update documentation** (if needed):
   - Add async testing examples to README
   - Document pytest-httpx usage patterns

5. **Create pull request**:
   - Follow conventional commit format
   - Link to issue with `Fixes #<number>`
   - Ensure all quality checks pass

## Reference

- **Full Research**: [research.md](./research.md)
- **Data Model**: [data-model.md](./data-model.md)
- **Implementation Plan**: [plan.md](./plan.md)
- **pytest-httpx Docs**: https://colin-b.github.io/pytest_httpx/
- **httpx Async Guide**: https://www.python-httpx.org/async/
