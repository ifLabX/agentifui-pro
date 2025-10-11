# Data Model: Test Infrastructure Entities

**Feature**: Update Dify SDK Test Suite for httpx Migration
**Date**: 2025-10-11

## Overview

This document defines the test infrastructure entities (fixtures, mocks, and configuration objects) required for the httpx async test migration. These entities represent the testing abstractions rather than production data models.

## Core Entities

### 1. AsyncClient Mock

**Purpose**: Mock httpx.AsyncClient for testing SDK HTTP operations

**Attributes**:
```python
class AsyncClientMock:
    """Fixture-provided mock for httpx.AsyncClient"""

    # Async context manager support
    __aenter__: AsyncMock  # Returns self when entering async context
    __aexit__: AsyncMock   # Cleans up when exiting async context

    # HTTP method mocks (all async)
    get: AsyncMock         # Mocked GET requests
    post: AsyncMock        # Mocked POST requests
    put: AsyncMock         # Mocked PUT requests
    delete: AsyncMock      # Mocked DELETE requests
    patch: AsyncMock       # Mocked PATCH requests
    request: AsyncMock     # Generic request method
```

**Relationships**:
- Returns → `Response Mock` (configured via pytest-httpx)
- Used by → All test files via `httpx_mock` fixture
- Patched at → SDK module level (e.g., `dify_client.base._client`)

**State Transitions**: N/A (stateless mock)

**Validation Rules**:
- Must support async context manager protocol
- All HTTP methods must return awaitable responses
- Must track call history for assertion verification

---

### 2. Response Mock

**Purpose**: Mock httpx.Response for testing HTTP response handling

**Attributes**:
```python
class ResponseMock:
    """Represents mocked HTTP response from pytest-httpx"""

    # Synchronous data access (matches real httpx behavior)
    status_code: int              # HTTP status code (200, 404, etc.)
    headers: dict[str, str]       # Response headers
    json: Callable[[], dict]      # Parse JSON response (sync)
    text: str                     # Response body as text (sync)
    content: bytes                # Raw response bytes (sync)

    # Async streaming methods
    aiter_bytes: AsyncIterator[bytes]    # Async byte chunks
    aiter_text: AsyncIterator[str]       # Async text chunks
    aiter_lines: AsyncIterator[str]      # Async line-by-line

    # Error handling
    is_error: bool                # True if 4xx/5xx status
    raise_for_status: Callable    # Raise HTTPStatusError if error
```

**Relationships**:
- Returned by → `AsyncClient Mock` HTTP methods
- Used by → SDK client methods for response processing
- Configured via → pytest-httpx `add_response()` method

**State Transitions**: N/A (immutable mock)

**Validation Rules**:
- `status_code` must be valid HTTP status (100-599)
- `.json()` method must be synchronous (no await)
- Streaming methods must be async iterators
- Error responses must include proper httpx exception types

---

### 3. Test Fixtures (conftest.py)

**Purpose**: Reusable test setup and teardown utilities

**Fixture Catalog**:

```python
# Configuration fixtures
@pytest.fixture
def mock_api_key() -> str:
    """Provide mock API key for SDK initialization"""
    return "test-api-key-12345"

@pytest.fixture
def mock_base_url() -> str:
    """Provide mock base URL for API endpoints"""
    return "https://test-api.dify.ai/v1"

@pytest.fixture
def mock_user() -> str:
    """Provide mock user identifier"""
    return "test-user-123"

# pytest-httpx fixture (automatically provided)
# httpx_mock: HTTPXMock - Main fixture for mocking HTTP requests

# Sample data fixtures
@pytest.fixture
def sample_inputs() -> dict[str, Any]:
    """Sample input data for SDK methods"""
    return {"query": "test query", "context": "test context"}

@pytest.fixture
def sample_files() -> dict[str, Any]:
    """Sample file upload data"""
    return {"file": ("test.txt", b"content", "text/plain")}

# ID fixtures (for resource references)
@pytest.fixture
def sample_conversation_id() -> str:
    return "conv-12345-abcde"

@pytest.fixture
def sample_message_id() -> str:
    return "msg-67890-fghij"

# ... (additional ID fixtures as needed)
```

**Relationships**:
- Consumed by → All test methods via dependency injection
- Configured via → pytest fixture discovery
- Scope → Function-level (default) for isolation

**Validation Rules**:
- All fixtures must have type annotations
- Fixture names must be descriptive and unique
- Sample data must be realistic and complete

---

### 4. pytest Configuration

**Purpose**: Configure pytest and pytest-asyncio behavior

**Configuration File**: `api/pytest.ini`

```ini
[pytest]
asyncio_mode = auto
asyncio_default_fixture_loop_scope = function
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
```

**Attributes**:
- `asyncio_mode`: Auto-discover async test functions
- `asyncio_default_fixture_loop_scope`: Event loop per test function
- `testpaths`: Root directory for test discovery
- `python_files`: Test file naming pattern
- `python_classes`: Test class naming pattern
- `python_functions`: Test method naming pattern

**Relationships**:
- Affects → All test execution and discovery
- Required by → pytest-asyncio plugin
- Configures → Event loop management

**Validation Rules**:
- `asyncio_mode` must be "auto" for zero-decorator pattern
- Fixture loop scope should match test isolation requirements
- Test paths must point to valid test directories

---

### 5. HTTPXMock Request Configuration

**Purpose**: Configure expected HTTP requests and responses

**Structure**:
```python
from pytest_httpx import HTTPXMock

# Success response
httpx_mock.add_response(
    url="https://test-api.dify.ai/v1/chat-messages",
    method="POST",
    json={"success": True, "data": {"id": "msg-123"}},
    status_code=200,
    headers={"Content-Type": "application/json"}
)

# Error response
httpx_mock.add_response(
    url="https://test-api.dify.ai/v1/invalid",
    status_code=404,
    json={"error": "Not Found"}
)

# Streaming response
httpx_mock.add_response(
    url="https://test-api.dify.ai/v1/stream",
    content=b'data: {"chunk": 1}\ndata: {"chunk": 2}\n',
    headers={"Content-Type": "text/event-stream"}
)
```

**Attributes**:
- `url`: Target URL (exact match or pattern)
- `method`: HTTP method (GET, POST, etc.)
- `json`: JSON response body
- `content`: Raw bytes response
- `status_code`: HTTP status code
- `headers`: Response headers dict

**Relationships**:
- Configured by → Test methods before SDK calls
- Matched against → httpx.AsyncClient requests
- Returns → Response Mock to SDK

**Validation Rules**:
- URL must match SDK's actual request URL
- Method must match SDK's HTTP method
- Response format must match SDK's expected format
- One response per unique (url, method) combination

---

## Entity Lifecycle

### Test Execution Flow

```
1. pytest discovers async test_* functions
   ↓
2. pytest-asyncio creates event loop (auto mode)
   ↓
3. Fixtures injected via dependency injection
   ↓
4. httpx_mock configured with expected responses
   ↓
5. SDK method called → httpx.AsyncClient.method()
   ↓
6. pytest-httpx intercepts request, returns mock response
   ↓
7. Assertions verify response and call history
   ↓
8. Event loop cleaned up automatically
```

### Mock Object Lifecycle

```
conftest.py fixtures (session scope)
    ↓
httpx_mock fixture (function scope - auto-reset per test)
    ↓
add_response() configurations (per test)
    ↓
SDK method invocation
    ↓
Response returned
    ↓
Mock history available for assertions
    ↓
Automatic cleanup after test
```

---

## Migration Impact

### Changed Entities

| Entity | Before (requests) | After (httpx) | Impact |
|--------|-------------------|---------------|--------|
| HTTP Client Mock | `requests.request` patched | `httpx.AsyncClient` via pytest-httpx | Complete replacement |
| Response Mock | `requests.Response` Mock | `httpx.Response` via pytest-httpx | Behavior change (sync/async) |
| Test Methods | `def test_*` | `async def test_*` | Async conversion required |
| Fixtures | Sync fixtures | Async-compatible fixtures | May need async versions |
| Assertions | Sync mock.assert_called | httpx_mock.get_requests() | Different assertion patterns |

### Preserved Entities

| Entity | Status | Notes |
|--------|--------|-------|
| Sample Data Fixtures | Unchanged | Still use sync fixtures (no async needed) |
| Test Organization | Unchanged | Same file structure and naming |
| Test Logic | Unchanged | Business assertions remain identical |
| Coverage Requirements | Unchanged | Still ≥80% coverage |

---

## Validation Requirements

### Test Fixture Validation
- All fixtures must have type annotations
- Async fixtures must use `@pytest.fixture` (not `@pytest_asyncio.fixture` in auto mode)
- Fixture dependencies must form valid DAG (no circular dependencies)

### Mock Configuration Validation
- pytest-httpx responses must match actual SDK request patterns
- Response format must match SDK's expected response structure
- Error responses must include proper httpx exception behaviors

### Test Method Validation
- All test methods must be `async def test_*`
- SDK client calls must use `await`
- Assertions must use pytest-httpx patterns (`.get_requests()`, `.get_request()`)
- No synchronous test methods remaining after migration

---

## References

- **pytest-httpx Documentation**: https://colin-b.github.io/pytest_httpx/
- **httpx AsyncClient**: https://www.python-httpx.org/async/
- **pytest-asyncio**: https://pytest-asyncio.readthedocs.io/
- **Research Document**: [research.md](./research.md)
