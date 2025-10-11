# httpx Async Testing Migration Research

**Date**: 2025-10-11
**Purpose**: Research best practices for migrating from synchronous to asynchronous httpx testing patterns
**Status**: Complete

## Executive Summary

This document provides comprehensive research for migrating Dify SDK tests from synchronous `requests` mocking to asynchronous `httpx.AsyncClient` patterns. The recommended approach is to use **pytest-httpx** for mocking, which provides superior developer experience and maintainability compared to manual AsyncMock patterns.

**Key Decision**: Use `pytest-httpx` library for httpx mocking instead of manual `unittest.mock.AsyncMock` patterns.

**Rationale**:
- Cleaner, more readable test code
- Built specifically for httpx (both sync and async)
- Handles async context managers automatically
- Simpler response/request matching
- Better error messages
- Active maintenance and community support

---

## 1. httpx.AsyncClient Best Practices

### 1.1 Understanding AsyncClient

`httpx.AsyncClient` is the asynchronous HTTP client that requires:
- Async context managers (`async with`)
- Awaiting all async methods
- Proper event loop management

```python
# Basic AsyncClient usage
async with httpx.AsyncClient() as client:
    response = await client.get("https://api.example.com/endpoint")
    data = response.json()  # Note: .json() is synchronous!
```

### 1.2 Mocking Approaches Comparison

#### Approach A: pytest-httpx (RECOMMENDED)

**Pros**:
- Clean, declarative API
- No manual mock setup required
- Automatic handling of async context managers
- Built-in request matching and assertions
- Works identically for sync and async clients

**Cons**:
- Additional dependency (but lightweight)
- Another API to learn (minimal learning curve)

**Example**:
```python
import pytest
import httpx
from pytest_httpx import HTTPXMock

@pytest.mark.asyncio
async def test_create_chat_message(httpx_mock: HTTPXMock):
    # Setup mock response
    httpx_mock.add_response(
        method="POST",
        url="https://api.dify.ai/v1/chat-messages",
        json={"success": True, "data": {"message": "Operation successful"}},
        status_code=200
    )

    # Use real client
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.dify.ai/v1/chat-messages",
            json={"query": "What is AI?", "user": "test-user"}
        )

    # Assertions
    assert response.status_code == 200
    assert response.json()["success"] is True

    # Verify request was made
    request = httpx_mock.get_request()
    assert request.method == "POST"
    assert "query" in request.read().decode()
```

#### Approach B: MockTransport

**Pros**:
- No external dependencies
- Full control over transport layer
- Good for complex scenarios

**Cons**:
- More boilerplate code
- Manual response construction
- More complex for simple cases

**Example**:
```python
import httpx

def test_with_mock_transport():
    def handler(request):
        return httpx.Response(
            200,
            json={"success": True, "data": {"message": "Operation successful"}}
        )

    transport = httpx.MockTransport(handler)

    async with httpx.AsyncClient(transport=transport) as client:
        response = await client.get("https://api.dify.ai/v1/endpoint")
        assert response.status_code == 200
```

#### Approach C: unittest.mock.AsyncMock (NOT RECOMMENDED)

**Pros**:
- No external dependencies
- Familiar for unittest users

**Cons**:
- Complex setup for async context managers
- Manual configuration of __aenter__, __aexit__
- Error-prone
- Less readable
- Requires deep understanding of async mocking

**Example** (for reference only):
```python
from unittest.mock import AsyncMock, patch
import pytest

@pytest.mark.asyncio
async def test_with_async_mock():
    # Complex setup required
    mock_response = AsyncMock()
    mock_response.status_code = 200
    mock_response.json = lambda: {"success": True}
    mock_response.text = "success"
    mock_response.headers = {}

    mock_client = AsyncMock()
    mock_client.__aenter__.return_value = mock_client
    mock_client.__aexit__.return_value = None
    mock_client.post.return_value = mock_response

    with patch('httpx.AsyncClient', return_value=mock_client):
        async with httpx.AsyncClient() as client:
            response = await client.post("https://api.dify.ai/v1/endpoint")
            assert response.status_code == 200
```

### 1.3 Patching Strategy

**Decision**: Patch at the SDK module level, not at httpx module level.

**Rationale**:
- SDK imports httpx at module load time
- Patching httpx globally affects all tests
- Module-level patching is more isolated
- Easier to understand test scope

**Example**:
```python
# ✅ GOOD: Patch at SDK level (if using manual mocks)
with patch('dify_client.httpx.AsyncClient') as mock_client:
    ...

# ❌ BAD: Patch httpx globally
with patch('httpx.AsyncClient') as mock_client:
    ...

# ✅ BEST: Use pytest-httpx (no patching needed)
def test_something(httpx_mock: HTTPXMock):
    httpx_mock.add_response(...)
```

---

## 2. pytest-asyncio Configuration

### 2.1 Current Configuration

The project already has optimal pytest-asyncio configuration in `pyproject.toml`:

```toml
[tool.pytest.ini_options]
pythonpath = ["."]
testpaths = ["tests"]
asyncio_mode = "auto"
```

### 2.2 Understanding asyncio_mode

#### Auto Mode (CURRENT - RECOMMENDED)

**Behavior**:
- Automatically detects async test functions
- Automatically converts `@pytest.fixture` to async fixtures when needed
- No explicit `@pytest.mark.asyncio` required
- Most convenient for majority of use cases

**Example**:
```python
# In auto mode, this is automatically recognized as async test
async def test_async_operation():
    result = await some_async_function()
    assert result == expected

# Fixtures are also auto-detected
@pytest.fixture
async def async_database():
    db = await create_db_connection()
    yield db
    await db.close()
```

#### Strict Mode

**Behavior**:
- Requires explicit `@pytest.mark.asyncio` on all async tests
- More explicit but more verbose
- Better for mixed sync/async test suites

**Example**:
```python
import pytest

@pytest.mark.asyncio  # Required in strict mode
async def test_async_operation():
    result = await some_async_function()
    assert result == expected
```

**Decision**: Keep `auto` mode - it's already configured and provides the best developer experience.

### 2.3 Event Loop Scopes

pytest-asyncio supports different event loop scopes:

- **function** (default): New loop for each test function
- **class**: Shared loop for all tests in a class
- **module**: Shared loop for all tests in a module
- **session**: Single loop for entire test session

**Current Recommendation**: Use default `function` scope.

**Rationale**:
- Better test isolation
- Prevents test interdependencies
- Easier to debug failures
- Minimal performance impact for our test suite size

**If needed later**, can configure per-test:
```python
@pytest.mark.asyncio(loop_scope="module")
async def test_shared_loop():
    ...
```

Or set default in config:
```toml
[tool.pytest.ini_options]
asyncio_default_test_loop_scope = "function"
```

### 2.4 Async Fixtures

**Pattern**:
```python
import pytest

@pytest.fixture
async def async_database():
    """Auto mode automatically detects this as async fixture."""
    db = await create_db_connection()
    await db.execute("CREATE TABLE test_table")

    yield db

    await db.execute("DROP TABLE test_table")
    await db.close()

@pytest.fixture
async def mock_api_client(httpx_mock):
    """Combining sync and async fixtures."""
    httpx_mock.add_response(json={"status": "ok"})

    async with httpx.AsyncClient() as client:
        yield client
```

---

## 3. httpx.Response Mocking

### 3.1 Synchronous Methods

These httpx.Response methods are **synchronous** (no await needed):

| Method | Type | Description | Example |
|--------|------|-------------|---------|
| `.json()` | sync | Parse JSON response body | `data = response.json()` |
| `.text` | property | Get response body as string | `text = response.text` |
| `.content` | property | Get raw bytes | `bytes = response.content` |
| `.status_code` | property | HTTP status code | `code = response.status_code` |
| `.headers` | property | Response headers | `ct = response.headers["content-type"]` |
| `.cookies` | property | Response cookies | `cookies = response.cookies` |
| `.links` | property | Parsed Link headers | `links = response.links` |
| `.is_error` | property | Whether response is 4xx/5xx | `if response.is_error: ...` |
| `.raise_for_status()` | sync | Raise exception on error | `response.raise_for_status()` |

**Example**:
```python
@pytest.mark.asyncio
async def test_response_sync_methods(httpx_mock):
    httpx_mock.add_response(
        json={"key": "value"},
        status_code=200,
        headers={"Content-Type": "application/json"}
    )

    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.example.com/endpoint")

    # All of these are synchronous - NO await
    assert response.status_code == 200
    assert response.json() == {"key": "value"}
    assert response.text == '{"key": "value"}'
    assert response.headers["Content-Type"] == "application/json"
```

### 3.2 Asynchronous Methods

These httpx.Response methods are **asynchronous** (require await):

| Method | Type | Description | Example |
|--------|------|-------------|---------|
| `.aread()` | async | Read entire response body | `body = await response.aread()` |
| `.aiter_bytes()` | async iter | Stream response as bytes | `async for chunk in response.aiter_bytes(): ...` |
| `.aiter_text()` | async iter | Stream response as text | `async for line in response.aiter_text(): ...` |
| `.aiter_lines()` | async iter | Stream response as lines | `async for line in response.aiter_lines(): ...` |
| `.aiter_raw()` | async iter | Stream raw bytes | `async for chunk in response.aiter_raw(): ...` |
| `.aclose()` | async | Close response | `await response.aclose()` |

**Example**:
```python
@pytest.mark.asyncio
async def test_streaming_response(httpx_mock):
    from pytest_httpx import IteratorStream

    httpx_mock.add_response(
        stream=IteratorStream([b"chunk1", b"chunk2", b"chunk3"])
    )

    async with httpx.AsyncClient() as client:
        async with client.stream("GET", "https://api.example.com/stream") as response:
            chunks = []
            async for chunk in response.aiter_bytes():
                chunks.append(chunk)

    assert chunks == [b"chunk1", b"chunk2", b"chunk3"]
```

### 3.3 Mocking Different Response Types

#### JSON Response
```python
httpx_mock.add_response(
    json={"success": True, "data": {"id": 123}},
    status_code=200
)
```

#### Text Response
```python
httpx_mock.add_response(
    content=b"Plain text response",
    status_code=200,
    headers={"Content-Type": "text/plain"}
)
```

#### Error Response
```python
httpx_mock.add_response(
    json={"error": "Bad Request", "message": "Invalid parameters"},
    status_code=400
)
```

#### Streaming Response
```python
from pytest_httpx import IteratorStream

httpx_mock.add_response(
    stream=IteratorStream([
        b'data: {"event": "message", "content": "Hello"}\n',
        b'data: {"event": "message", "content": " World"}\n',
        b'data: {"event": "done"}\n'
    ]),
    headers={"Content-Type": "text/event-stream"}
)
```

---

## 4. Async Test Patterns

### 4.1 Converting Synchronous Tests to Async

#### Pattern 1: Simple Test Conversion

**Before (Synchronous)**:
```python
def test_get_application_parameters(
    mock_api_key: str,
    mock_requests_request: Mock,
    mock_successful_response: Mock,
    mock_user: str,
) -> None:
    """Test retrieving application parameters."""
    mock_requests_request.return_value = mock_successful_response

    client = DifyClient(api_key=mock_api_key)
    response = client.get_application_parameters(user=mock_user)

    mock_requests_request.assert_called_once()
    assert response == mock_successful_response
```

**After (Asynchronous)**:
```python
@pytest.mark.asyncio  # Optional in auto mode, but explicit is fine
async def test_get_application_parameters(
    mock_api_key: str,
    httpx_mock: HTTPXMock,
    mock_user: str,
) -> None:
    """Test retrieving application parameters."""
    httpx_mock.add_response(
        method="GET",
        url="https://api.dify.ai/v1/parameters",
        json={"success": True, "data": {"message": "Operation successful"}},
        status_code=200
    )

    client = DifyClient(api_key=mock_api_key)
    response = await client.get_application_parameters(user=mock_user)

    # Verify request
    request = httpx_mock.get_request()
    assert request.method == "GET"
    assert "parameters" in str(request.url)

    # Verify response
    assert response.status_code == 200
    assert response.json()["success"] is True
```

**Key Changes**:
1. Add `async` before `def test_*`
2. Add `await` before async method calls
3. Replace `mock_requests_request` with `httpx_mock`
4. Use `httpx_mock.add_response()` instead of mock return values
5. Use `httpx_mock.get_request()` for assertions

#### Pattern 2: Streaming Test Conversion

**Before (Synchronous)**:
```python
def test_create_chat_message_streaming(
    mock_api_key: str,
    mock_requests_request: Mock,
    mock_streaming_response: Mock,
    sample_inputs: dict,
    mock_user: str,
) -> None:
    """Test creating a chat message in streaming mode."""
    mock_requests_request.return_value = mock_streaming_response

    client = ChatClient(api_key=mock_api_key)
    response = client.create_chat_message(
        inputs=sample_inputs,
        query="Explain quantum computing",
        user=mock_user,
        response_mode="streaming",
    )

    assert response == mock_streaming_response
```

**After (Asynchronous)**:
```python
@pytest.mark.asyncio
async def test_create_chat_message_streaming(
    mock_api_key: str,
    httpx_mock: HTTPXMock,
    sample_inputs: dict,
    mock_user: str,
) -> None:
    """Test creating a chat message in streaming mode."""
    from pytest_httpx import IteratorStream

    httpx_mock.add_response(
        method="POST",
        url="https://api.dify.ai/v1/chat-messages",
        stream=IteratorStream([
            b'data: {"event": "message", "content": "Quantum"}\n',
            b'data: {"event": "message", "content": " computing"}\n',
            b'data: {"event": "done"}\n'
        ]),
        headers={"Content-Type": "text/event-stream"}
    )

    client = ChatClient(api_key=mock_api_key)

    async with client.create_chat_message(
        inputs=sample_inputs,
        query="Explain quantum computing",
        user=mock_user,
        response_mode="streaming",
    ) as response:
        chunks = []
        async for chunk in response.aiter_lines():
            chunks.append(chunk)

    assert len(chunks) == 3
    assert b"Quantum" in chunks[0]
```

### 4.2 Assertion Patterns

#### Verifying Request Details
```python
@pytest.mark.asyncio
async def test_request_verification(httpx_mock: HTTPXMock):
    httpx_mock.add_response(json={"status": "ok"})

    async with httpx.AsyncClient() as client:
        await client.post(
            "https://api.example.com/endpoint",
            json={"key": "value"},
            headers={"Authorization": "Bearer token"}
        )

    # Get the request that was made
    request = httpx_mock.get_request()

    # Verify method and URL
    assert request.method == "POST"
    assert str(request.url) == "https://api.example.com/endpoint"

    # Verify headers
    assert request.headers["Authorization"] == "Bearer token"

    # Verify body
    import json
    body = json.loads(request.read())
    assert body["key"] == "value"
```

#### Verifying Multiple Requests
```python
@pytest.mark.asyncio
async def test_multiple_requests(httpx_mock: HTTPXMock):
    httpx_mock.add_response(json={"status": "ok"})
    httpx_mock.add_response(json={"status": "ok"})

    async with httpx.AsyncClient() as client:
        await client.get("https://api.example.com/endpoint1")
        await client.get("https://api.example.com/endpoint2")

    # Get all requests
    requests = httpx_mock.get_requests()
    assert len(requests) == 2
    assert "endpoint1" in str(requests[0].url)
    assert "endpoint2" in str(requests[1].url)
```

#### Verifying No Request Was Made
```python
@pytest.mark.asyncio
async def test_no_request(httpx_mock: HTTPXMock):
    # No response added, no request should be made

    # Verify no request
    assert httpx_mock.get_request() is None
    assert len(httpx_mock.get_requests()) == 0
```

### 4.3 Error Handling Patterns

#### Testing Exception Raising
```python
@pytest.mark.asyncio
async def test_timeout_exception(httpx_mock: HTTPXMock):
    httpx_mock.add_exception(
        httpx.ReadTimeout("Unable to read within timeout")
    )

    async with httpx.AsyncClient() as client:
        with pytest.raises(httpx.ReadTimeout) as exc_info:
            await client.get("https://api.example.com/slow")

    assert "timeout" in str(exc_info.value).lower()
```

#### Testing HTTP Error Responses
```python
@pytest.mark.asyncio
async def test_http_error(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        json={"error": "Not Found", "message": "Resource does not exist"},
        status_code=404
    )

    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.example.com/missing")

    assert response.status_code == 404
    assert response.json()["error"] == "Not Found"

    # Verify raise_for_status works
    with pytest.raises(httpx.HTTPStatusError):
        response.raise_for_status()
```

---

## 5. Common Pitfalls and Solutions

### 5.1 Event Loop Errors

#### Pitfall: RuntimeError: This event loop is already running
```python
# ❌ BAD: Trying to run async code in sync context
def test_bad():
    async def inner():
        return "result"

    result = asyncio.run(inner())  # ERROR if event loop already exists
```

**Solution**: Make the entire test async
```python
# ✅ GOOD: Entire test is async
@pytest.mark.asyncio
async def test_good():
    async def inner():
        return "result"

    result = await inner()
    assert result == "result"
```

### 5.2 Mock Attribute Errors

#### Pitfall: AsyncMock missing __aenter__ and __aexit__

```python
# ❌ BAD: Manual mock without context manager support
from unittest.mock import AsyncMock

mock_client = AsyncMock()
async with mock_client:  # AttributeError: __aenter__
    pass
```

**Solution A**: Use pytest-httpx (no manual mocking)
```python
# ✅ GOOD: pytest-httpx handles everything
@pytest.mark.asyncio
async def test_with_httpx_mock(httpx_mock: HTTPXMock):
    httpx_mock.add_response(json={"status": "ok"})

    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.example.com")

    assert response.json()["status"] == "ok"
```

**Solution B**: Properly configure AsyncMock (complex, not recommended)
```python
# ✅ ACCEPTABLE: Manual AsyncMock with context manager
from unittest.mock import AsyncMock

mock_client = AsyncMock()
mock_client.__aenter__.return_value = mock_client
mock_client.__aexit__.return_value = None

async with mock_client:
    pass  # Works but complex
```

### 5.3 Forgotten await Statements

#### Pitfall: Forgetting to await async calls

```python
# ❌ BAD: Missing await
@pytest.mark.asyncio
async def test_missing_await(httpx_mock: HTTPXMock):
    httpx_mock.add_response(json={"status": "ok"})

    async with httpx.AsyncClient() as client:
        response = client.get("https://api.example.com")  # Returns coroutine!

    assert response.status_code == 200  # Error: coroutine has no attribute 'status_code'
```

**Solution**: Always await async method calls
```python
# ✅ GOOD: Proper await
@pytest.mark.asyncio
async def test_with_await(httpx_mock: HTTPXMock):
    httpx_mock.add_response(json={"status": "ok"})

    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.example.com")  # ✓ await added

    assert response.status_code == 200  # Works!
```

### 5.4 Streaming Response Iteration

#### Pitfall: Using sync iteration on async iterators

```python
# ❌ BAD: Sync iteration on async iterator
@pytest.mark.asyncio
async def test_bad_streaming(httpx_mock: HTTPXMock):
    from pytest_httpx import IteratorStream

    httpx_mock.add_response(stream=IteratorStream([b"chunk1", b"chunk2"]))

    async with httpx.AsyncClient() as client:
        async with client.stream("GET", "https://api.example.com") as response:
            for chunk in response.aiter_bytes():  # ❌ Missing 'async'
                print(chunk)  # Gets coroutine objects, not bytes!
```

**Solution**: Use async iteration
```python
# ✅ GOOD: Async iteration
@pytest.mark.asyncio
async def test_good_streaming(httpx_mock: HTTPXMock):
    from pytest_httpx import IteratorStream

    httpx_mock.add_response(stream=IteratorStream([b"chunk1", b"chunk2"]))

    async with httpx.AsyncClient() as client:
        async with client.stream("GET", "https://api.example.com") as response:
            async for chunk in response.aiter_bytes():  # ✓ 'async for'
                print(chunk)  # Gets actual bytes!
```

### 5.5 Response Body Reading Multiple Times

#### Pitfall: Response body consumed on first read

```python
# ❌ BAD: Trying to read response body twice
@pytest.mark.asyncio
async def test_double_read(httpx_mock: HTTPXMock):
    httpx_mock.add_response(json={"key": "value"})

    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.example.com")

    data1 = response.json()  # Works
    data2 = response.json()  # May fail or return empty!
```

**Solution**: Read once and store
```python
# ✅ GOOD: Read once
@pytest.mark.asyncio
async def test_single_read(httpx_mock: HTTPXMock):
    httpx_mock.add_response(json={"key": "value"})

    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.example.com")

    data = response.json()  # Read once

    # Use 'data' multiple times
    assert data["key"] == "value"
    assert "key" in data
```

### 5.6 Fixture Scope Mismatches

#### Pitfall: Using function-scoped async fixture with module-scoped test

```python
# ❌ BAD: Scope mismatch
@pytest.fixture(scope="module")
async def database():
    # This won't work properly with module scope
    db = await create_db()
    yield db
    await db.close()
```

**Solution**: Match scopes or use function scope
```python
# ✅ GOOD: Matching scopes
@pytest.fixture(scope="function")
async def database():
    db = await create_db()
    yield db
    await db.close()

# Or for module-scoped event loop:
@pytest.fixture(scope="module", loop_scope="module")
async def database():
    db = await create_db()
    yield db
    await db.close()
```

---

## 6. Recommended Approach

### 6.1 Technology Stack

**Selected Libraries**:
- ✅ `pytest-asyncio` (already installed: >=0.21.0)
- ✅ `pytest-httpx` (NEW - needs to be added)
- ✅ `httpx` (already installed: >=0.24.0)

**Add to pyproject.toml**:
```toml
[dependency-groups]
dev = [
    # ... existing dependencies ...
    "pytest-httpx>=0.30.0",  # Add this line
]
```

### 6.2 Migration Strategy

**Phase 1: Setup** (1 hour)
1. Add pytest-httpx to dependencies
2. Update conftest.py with new fixtures
3. Document patterns in this file

**Phase 2: Convert Fixtures** (2 hours)
1. Convert mock response fixtures from requests.Response to httpx.Response patterns
2. Remove mock_requests_request fixture
3. Add httpx_mock-based fixture helpers

**Phase 3: Migrate Tests** (8-12 hours)
1. Convert test methods to async (add `async def`)
2. Replace mock_requests_request usage with httpx_mock
3. Add `await` to all async calls
4. Update assertions to use httpx_mock.get_request()

**Phase 4: Validation** (2 hours)
1. Run full test suite
2. Verify coverage remains high
3. Fix any edge cases

### 6.3 Code Patterns to Use

#### Standard Test Pattern
```python
import pytest
from pytest_httpx import HTTPXMock
from dify_client import DifyClient

@pytest.mark.asyncio
async def test_operation(
    mock_api_key: str,
    httpx_mock: HTTPXMock,
    mock_user: str,
) -> None:
    """Test description."""
    # Setup mock
    httpx_mock.add_response(
        method="GET",
        url="https://api.dify.ai/v1/endpoint",
        json={"success": True, "data": {}},
        status_code=200
    )

    # Execute
    client = DifyClient(api_key=mock_api_key)
    response = await client.method(user=mock_user)

    # Verify request
    request = httpx_mock.get_request()
    assert request.method == "GET"
    assert "endpoint" in str(request.url)

    # Verify response
    assert response.status_code == 200
    assert response.json()["success"] is True
```

#### File Upload Test Pattern
```python
@pytest.mark.asyncio
async def test_file_upload(
    mock_api_key: str,
    httpx_mock: HTTPXMock,
    sample_files: dict,
    mock_user: str,
) -> None:
    """Test file upload."""
    httpx_mock.add_response(
        method="POST",
        url="https://api.dify.ai/v1/files/upload",
        json={"file_id": "file-123"},
        status_code=200
    )

    client = DifyClient(api_key=mock_api_key)
    response = await client.file_upload(user=mock_user, files=sample_files)

    request = httpx_mock.get_request()
    assert request.method == "POST"
    # File upload uses multipart form data
    assert "multipart/form-data" in request.headers.get("content-type", "")
```

#### Streaming Test Pattern
```python
@pytest.mark.asyncio
async def test_streaming(
    mock_api_key: str,
    httpx_mock: HTTPXMock,
    mock_user: str,
) -> None:
    """Test streaming response."""
    from pytest_httpx import IteratorStream

    httpx_mock.add_response(
        method="POST",
        url="https://api.dify.ai/v1/chat-messages",
        stream=IteratorStream([
            b'data: {"event": "message", "content": "Hello"}\n',
            b'data: {"event": "done"}\n'
        ]),
        headers={"Content-Type": "text/event-stream"}
    )

    client = ChatClient(api_key=mock_api_key)

    async with client.create_chat_message(
        inputs={},
        query="Hello",
        user=mock_user,
        response_mode="streaming"
    ) as response:
        chunks = []
        async for line in response.aiter_lines():
            chunks.append(line)

    assert len(chunks) == 2
    assert b"Hello" in chunks[0]
```

---

## 7. Migration Checklist

### Pre-Migration
- [x] Research async testing patterns
- [x] Document best practices
- [ ] Add pytest-httpx to dependencies
- [ ] Update conftest.py with new fixtures
- [ ] Create example test migration

### Test File Migration (Repeat for each file)
- [ ] Add `@pytest.mark.asyncio` to test classes (optional in auto mode)
- [ ] Convert test methods: `def test_*` → `async def test_*`
- [ ] Replace `mock_requests_request` with `httpx_mock` in signatures
- [ ] Replace `mock_requests_request.return_value` with `httpx_mock.add_response()`
- [ ] Add `await` before all async method calls
- [ ] Update assertions to use `httpx_mock.get_request()`
- [ ] Run tests: `uv run pytest tests/dify/test_*.py -v`
- [ ] Fix any failures
- [ ] Verify coverage maintained

### Post-Migration
- [ ] Run full test suite: `uv run pytest tests/`
- [ ] Verify coverage: `uv run pytest --cov=src tests/`
- [ ] Update documentation if needed
- [ ] Remove deprecated fixtures from conftest.py
- [ ] Code review

---

## 8. Reference Examples

### Complete Before/After Example

**Before: tests/dify/test_dify_client.py (excerpt)**
```python
from unittest.mock import Mock
from dify_client import DifyClient

class TestDifyClientInitialization:
    """Test DifyClient initialization and configuration."""

    def test_client_initialization_with_defaults(self, mock_api_key: str) -> None:
        """Test that client initializes with default base URL."""
        client = DifyClient(api_key=mock_api_key)

        assert client.api_key == mock_api_key
        assert client.base_url == "https://api.dify.ai/v1"

class TestDifyClientRequestMethods:
    """Test DifyClient HTTP request methods."""

    def test_send_request_get_method(
        self,
        mock_api_key: str,
        mock_base_url: str,
        mock_requests_request: Mock,
        mock_successful_response: Mock,
    ) -> None:
        """Test GET request with query parameters."""
        mock_requests_request.return_value = mock_successful_response

        client = DifyClient(api_key=mock_api_key, base_url=mock_base_url)
        params = {"user": "test-user"}

        response = client._send_request("GET", "/test-endpoint", params=params)

        # Verify request was made correctly
        mock_requests_request.assert_called_once_with(
            "GET",
            f"{mock_base_url}/test-endpoint",
            json=None,
            params=params,
            headers={
                "Authorization": f"Bearer {mock_api_key}",
                "Content-Type": "application/json",
            },
            stream=False,
        )
        assert response == mock_successful_response
```

**After: tests/dify/test_dify_client.py (migrated)**
```python
import pytest
from pytest_httpx import HTTPXMock
from dify_client import DifyClient

class TestDifyClientInitialization:
    """Test DifyClient initialization and configuration."""

    async def test_client_initialization_with_defaults(self, mock_api_key: str) -> None:
        """Test that client initializes with default base URL."""
        client = DifyClient(api_key=mock_api_key)

        assert client.api_key == mock_api_key
        assert client.base_url == "https://api.dify.ai/v1"

class TestDifyClientRequestMethods:
    """Test DifyClient HTTP request methods."""

    async def test_send_request_get_method(
        self,
        mock_api_key: str,
        mock_base_url: str,
        httpx_mock: HTTPXMock,
    ) -> None:
        """Test GET request with query parameters."""
        # Setup mock response
        httpx_mock.add_response(
            method="GET",
            url=f"{mock_base_url}/test-endpoint?user=test-user",
            json={"success": True, "data": {"message": "Operation successful"}},
            status_code=200,
            headers={"Content-Type": "application/json"}
        )

        client = DifyClient(api_key=mock_api_key, base_url=mock_base_url)
        params = {"user": "test-user"}

        response = await client._send_request("GET", "/test-endpoint", params=params)

        # Verify request details
        request = httpx_mock.get_request()
        assert request.method == "GET"
        assert str(request.url) == f"{mock_base_url}/test-endpoint?user=test-user"
        assert request.headers["Authorization"] == f"Bearer {mock_api_key}"
        assert request.headers["Content-Type"] == "application/json"

        # Verify response
        assert response.status_code == 200
        assert response.json()["success"] is True
```

### Updated conftest.py Fixtures

**Add to tests/dify/conftest.py**:
```python
"""
Dify SDK test configuration and fixtures.

This module provides shared test fixtures and utilities for testing Dify SDK clients.
All tests use pytest-httpx to mock HTTP calls.
"""

from collections.abc import Generator
from typing import Any

import pytest
from pytest_httpx import HTTPXMock


@pytest.fixture
def mock_api_key() -> str:
    """Provide a mock API key for testing."""
    return "test-api-key-12345"


@pytest.fixture
def mock_base_url() -> str:
    """Provide a mock base URL for testing."""
    return "https://test-api.dify.ai/v1"


@pytest.fixture
def mock_user() -> str:
    """Provide a mock user identifier for testing."""
    return "test-user-123"


# Removed: mock_requests_request, mock_successful_response, mock_error_response
# Replaced by httpx_mock fixture from pytest-httpx

@pytest.fixture
def sample_successful_response_data() -> dict[str, Any]:
    """Sample successful response data."""
    return {
        "success": True,
        "data": {"message": "Operation successful"},
    }


@pytest.fixture
def sample_error_response_data() -> dict[str, Any]:
    """Sample error response data."""
    return {
        "error": "Bad Request",
        "message": "Invalid request parameters",
    }


@pytest.fixture
def sample_streaming_chunks() -> list[bytes]:
    """Sample streaming response chunks."""
    return [
        b'data: {"event": "message", "content": "Hello"}\n',
        b'data: {"event": "message", "content": " World"}\n',
        b'data: {"event": "done"}\n',
    ]


# Keep existing sample data fixtures
@pytest.fixture
def sample_inputs() -> dict[str, Any]:
    """Provide sample input data for testing."""
    return {
        "query": "What is the weather today?",
        "context": "User is asking about weather",
    }


@pytest.fixture
def sample_files() -> dict[str, Any]:
    """Provide sample file data for testing."""
    return {
        "file": ("test.txt", b"test content", "text/plain"),
    }


@pytest.fixture
def sample_conversation_id() -> str:
    """Provide a sample conversation ID."""
    return "conv-12345-abcde"


# ... rest of existing fixtures unchanged ...
```

---

## 9. Additional Resources

### Official Documentation
- [httpx Documentation](https://www.python-httpx.org/)
- [httpx AsyncClient Guide](https://www.python-httpx.org/async/)
- [pytest-asyncio Documentation](https://pytest-asyncio.readthedocs.io/)
- [pytest-httpx Documentation](https://colin-b.github.io/pytest_httpx/)

### Key Concepts
- Async/await in Python: https://docs.python.org/3/library/asyncio.html
- AsyncMock: https://docs.python.org/3/library/unittest.mock.html#unittest.mock.AsyncMock
- Event loops: https://docs.python.org/3/library/asyncio-eventloop.html

### Related Libraries
- `respx`: Alternative httpx mocking library (more complex than pytest-httpx)
- `aioresponses`: For aiohttp (not applicable here)

---

## 10. Conclusion

**Recommended Path Forward**:

1. **Add pytest-httpx dependency** - It's the right tool for the job
2. **Update conftest.py** - Prepare new fixtures and remove old ones
3. **Migrate tests incrementally** - One file at a time
4. **Validate thoroughly** - Ensure coverage and functionality maintained

**Benefits of This Approach**:
- ✅ Clean, readable test code
- ✅ Better maintainability
- ✅ Proper async patterns
- ✅ Future-proof (httpx is actively maintained)
- ✅ Easier to onboard new developers

**Estimated Effort**: 12-16 hours total for full migration of all test files.

**Next Steps**:
1. Review and approve this research document
2. Add pytest-httpx to dependencies
3. Begin migration with one test file as proof of concept
4. Complete remaining test files
5. Remove deprecated fixtures and mock patterns
