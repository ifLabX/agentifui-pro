# Data Model: Coze Python SDK Integration

**Feature**: Coze Python SDK Integration
**Date**: 2025-10-10
**Status**: Complete

## Overview

This document defines the test data model and mock structures for Coze Python SDK integration testing. Since this is a test-only feature with no persistent storage, the "data model" consists of test fixtures, mock objects, and sample data used to validate SDK functionality.

## Test Entities

### 1. Coze Client Configuration

**Purpose**: Configuration data for initializing Coze SDK clients

**Attributes**:
- **api_token** (string): Authentication token for Coze API
  - Format: Alphanumeric string
  - Example: "test-coze-token-12345"
  - Validation: Non-empty string
- **base_url** (string): Base URL for Coze API endpoint
  - Format: HTTPS URL
  - Example: "https://api.coze.cn/v1" or "https://api.coze.com/v1"
  - Validation: Valid URL format
- **http_client_config** (optional dict): Custom HTTP client settings
  - timeout (float): General operation timeout in seconds
  - connect_timeout (float): Connection timeout in seconds
  - Example: {"timeout": 600.0, "connect": 5.0}

**Relationships**:
- Required for Client instances (both sync and async)
- Used by all test fixtures requiring authenticated clients

**State Transitions**: N/A (immutable configuration)

**Test Fixture**:
```python
@pytest.fixture
def mock_coze_config() -> dict[str, Any]:
    return {
        "api_token": "test-coze-token-12345",
        "base_url": "https://api.coze.cn/v1",
        "http_client_config": {
            "timeout": 600.0,
            "connect": 5.0
        }
    }
```

### 2. Bot Entity

**Purpose**: Represents a Coze bot for testing bot operations

**Attributes**:
- **bot_id** (string): Unique identifier for the bot
  - Format: Numeric string (Coze format)
  - Example: "7379462189365198898"
  - Validation: Non-empty string, typically 19 digits
- **workspace_id** (string): Workspace containing the bot
  - Format: Alphanumeric string with possible hyphens
  - Example: "workspace-12345-abcde"
  - Validation: Non-empty string
- **name** (string, optional): Bot display name
  - Example: "Customer Support Bot"
- **description** (string, optional): Bot purpose description
- **created_at** (int, optional): Unix timestamp of creation

**Relationships**:
- Belongs to a Workspace (workspace_id)
- Can have multiple Conversations
- Referenced in Chat operations

**State Transitions**: N/A (read-only in tests)

**Test Fixtures**:
```python
@pytest.fixture
def mock_bot_id() -> str:
    return "7379462189365198898"

@pytest.fixture
def mock_workspace_id() -> str:
    return "workspace-12345-abcde"

@pytest.fixture
def sample_bot_data() -> dict[str, Any]:
    return {
        "bot_id": "7379462189365198898",
        "name": "Test Bot",
        "description": "Bot for testing",
        "workspace_id": "workspace-12345-abcde",
        "created_at": 1718792949
    }
```

### 3. Chat Entity

**Purpose**: Represents a chat session for testing chat operations

**Attributes**:
- **chat_id** (string): Unique identifier for the chat
  - Format: Numeric string
  - Example: "7382159487131697202"
  - Validation: Non-empty string
- **conversation_id** (string): Associated conversation ID
  - Format: Numeric string
  - Example: "7381473525342978089"
  - Validation: Non-empty string
- **bot_id** (string): Bot handling the chat
  - Links to Bot entity
- **status** (string): Chat status
  - Values: "created", "in_progress", "completed", "failed"
  - Validation: Must be one of allowed values
- **usage** (dict): Token usage statistics
  - token_count (int): Total tokens used
  - input_count (int): Input tokens
  - output_count (int): Output tokens
- **created_at** (int): Unix timestamp of chat creation
- **completed_at** (int, optional): Unix timestamp of completion

**Relationships**:
- Belongs to a Conversation (conversation_id)
- Associated with a Bot (bot_id)
- Contains Messages

**State Transitions**:
```
created → in_progress → completed
created → in_progress → failed
```

**Test Fixtures**:
```python
@pytest.fixture
def mock_chat_id() -> str:
    return "7382159487131697202"

@pytest.fixture
def mock_conversation_id() -> str:
    return "7381473525342978089"

@pytest.fixture
def sample_chat_data() -> dict[str, Any]:
    return {
        "id": "7382159487131697202",
        "conversation_id": "7381473525342978089",
        "bot_id": "7379462189365198898",
        "status": "completed",
        "usage": {
            "token_count": 633,
            "output_count": 19,
            "input_count": 614
        },
        "created_at": 1718792949,
        "completed_at": 1718792949
    }
```

### 4. Message Entity

**Purpose**: Represents chat messages for testing messaging operations

**Attributes**:
- **message_id** (string, optional): Unique message identifier
- **role** (string): Message sender role
  - Values: "user", "assistant"
  - Validation: Must be "user" or "assistant"
- **content** (string): Message text content
  - Validation: Non-empty string for user messages
- **content_type** (string): Type of content
  - Values: "text", "audio", "image"
  - Default: "text"

**Relationships**:
- Belongs to a Conversation
- Part of a Chat session

**Test Fixtures**:
```python
@pytest.fixture
def sample_user_message() -> dict[str, Any]:
    return {
        "role": "user",
        "content": "What is the weather today?",
        "content_type": "text"
    }

@pytest.fixture
def sample_assistant_message() -> dict[str, Any]:
    return {
        "role": "assistant",
        "content": "The weather today is sunny with a high of 75°F.",
        "content_type": "text"
    }
```

### 5. Chat Event Entity

**Purpose**: Represents streaming chat events for testing stream operations

**Attributes**:
- **event** (string): Event type identifier
  - Values: "conversation.message.delta", "conversation.chat.created", "conversation.chat.in_progress", "conversation.chat.completed", "conversation.chat.failed"
  - Validation: Must be recognized ChatEventType
- **message** (dict, optional): Message data for delta events
  - content (string): Partial or complete message content
- **chat** (dict, optional): Chat data for status events
  - id (string): Chat ID
  - status (string): Current status
  - usage (dict): Token usage stats

**Relationships**:
- Associated with a Chat session
- Emitted during streaming operations

**State Transition Events**:
```
conversation.chat.created (initial)
  ↓
conversation.chat.in_progress (processing)
  ↓
conversation.message.delta (content streaming, multiple events)
  ↓
conversation.chat.completed (success)
OR
conversation.chat.failed (error)
```

**Test Fixtures**:
```python
@pytest.fixture
def mock_streaming_events() -> list[bytes]:
    """Mock streaming event data."""
    return [
        b'event: conversation.chat.created\ndata: {"id":"chat-123","status":"created"}',
        b'event: conversation.chat.in_progress\ndata: {"id":"chat-123","status":"in_progress"}',
        b'event: conversation.message.delta\ndata: {"message":{"content":"Hello"}}',
        b'event: conversation.message.delta\ndata: {"message":{"content":" World"}}',
        b'event: conversation.chat.completed\ndata: {"id":"chat-123","status":"completed","usage":{"token_count":633}}',
    ]
```

### 6. Workflow Entity

**Purpose**: Represents workflow execution for testing workflow operations

**Attributes**:
- **workflow_id** (string): Unique workflow identifier
  - Format: Alphanumeric with hyphens
  - Example: "workflow-77777-88888"
  - Validation: Non-empty string
- **workflow_run_id** (string): Specific execution instance ID
  - Format: Alphanumeric with hyphens
  - Example: "run-12345-abc"
- **status** (string): Execution status
  - Values: "running", "succeeded", "failed"
  - Validation: Must be one of allowed values
- **inputs** (dict): Input parameters for workflow
  - Flexible structure based on workflow definition
- **outputs** (dict, optional): Workflow execution results
- **created_at** (int): Unix timestamp of execution start
- **completed_at** (int, optional): Unix timestamp of completion

**Relationships**:
- Belongs to a Bot (implicitly)
- Produces workflow logs

**State Transitions**:
```
running → succeeded
running → failed
```

**Test Fixtures**:
```python
@pytest.fixture
def mock_workflow_id() -> str:
    return "workflow-77777-88888"

@pytest.fixture
def mock_workflow_run_id() -> str:
    return "run-12345-abc"

@pytest.fixture
def sample_workflow_inputs() -> dict[str, Any]:
    return {
        "query": "Process this data",
        "context": "User workflow request",
        "parameters": {"mode": "batch"}
    }

@pytest.fixture
def sample_workflow_data() -> dict[str, Any]:
    return {
        "workflow_id": "workflow-77777-88888",
        "workflow_run_id": "run-12345-abc",
        "status": "succeeded",
        "inputs": {"query": "Process this data"},
        "outputs": {"result": "Data processed successfully"},
        "created_at": 1718792949,
        "completed_at": 1718792955
    }
```

### 7. HTTP Response Entity

**Purpose**: Mock HTTP responses for testing API interactions

**Attributes**:
- **status_code** (int): HTTP status code
  - Validation: Valid HTTP status (200, 400, 500, etc.)
- **headers** (dict): Response headers
  - Content-Type (string): Response content type
  - Example: {"Content-Type": "application/json"}
- **body** (dict or bytes): Response body
  - JSON format for standard responses
  - Bytes for streaming responses
- **logid** (string): Coze-specific request ID for debugging
  - Example: "req-12345-abcde"
  - Present in all Coze API responses

**Response Types**:
1. **Successful Response** (200)
2. **Error Response** (400, 500)
3. **Streaming Response** (200 with event stream)

**Test Fixtures**:
```python
@pytest.fixture
def mock_successful_response() -> Mock:
    """Mock successful HTTP response."""
    response = Mock(spec=httpx.Response)
    response.status_code = 200
    response.json.return_value = {
        "success": True,
        "data": {"message": "Operation successful"},
        "logid": "req-12345-abcde"
    }
    response.headers = {"Content-Type": "application/json"}
    return response

@pytest.fixture
def mock_error_response() -> Mock:
    """Mock error HTTP response."""
    response = Mock(spec=httpx.Response)
    response.status_code = 400
    response.json.return_value = {
        "error": "Bad Request",
        "message": "Invalid parameters",
        "logid": "req-error-789"
    }
    response.headers = {"Content-Type": "application/json"}
    return response

@pytest.fixture
def mock_streaming_response(mock_streaming_events: list[bytes]) -> Mock:
    """Mock streaming HTTP response."""
    response = Mock(spec=httpx.Response)
    response.status_code = 200
    response.headers = {"Content-Type": "text/event-stream"}
    response.iter_lines = Mock(return_value=iter(mock_streaming_events))
    return response
```

### 8. Pagination Entity

**Purpose**: Mock pagination structures for testing list operations

**Attributes**:
- **page_num** (int): Current page number
  - Validation: Positive integer
- **page_size** (int): Items per page
  - Validation: Positive integer, typically 10-100
- **has_more** (bool): Whether more pages exist
- **items** (list): Page items
  - List of Bot, Conversation, or other entities
- **total** (int, optional): Total item count

**Relationships**:
- Contains multiple instances of entity type (Bot, etc.)

**Test Fixtures**:
```python
@pytest.fixture
def mock_paginated_bots() -> dict[str, Any]:
    """Mock paginated bot list response."""
    return {
        "page_num": 1,
        "page_size": 10,
        "has_more": True,
        "total": 25,
        "items": [
            {"bot_id": "bot-1", "name": "Bot One"},
            {"bot_id": "bot-2", "name": "Bot Two"},
            {"bot_id": "bot-3", "name": "Bot Three"},
        ],
        "logid": "req-pagination-123"
    }
```

## Validation Rules

### Client Configuration Validation
- api_token: MUST NOT be empty string
- base_url: MUST be valid HTTPS URL
- Timeout values: MUST be positive numbers

### Bot Validation
- bot_id: MUST match Coze ID format (numeric string)
- workspace_id: MUST NOT be empty string

### Chat Validation
- status: MUST be one of: "created", "in_progress", "completed", "failed"
- usage.token_count: MUST be non-negative integer
- completed_at: MUST be >= created_at if present

### Message Validation
- role: MUST be "user" or "assistant"
- content: MUST NOT be empty for user messages
- content_type: MUST be "text", "audio", or "image"

### Workflow Validation
- status: MUST be one of: "running", "succeeded", "failed"
- inputs: MUST be valid JSON object
- workflow_id: MUST NOT be empty string

### Response Validation
- status_code: MUST be valid HTTP status code (100-599)
- logid: MUST be present in all mock responses
- Streaming responses: MUST include proper event format

## Mock Object Specifications

### Mock Client (httpx.Client)
```python
@pytest.fixture
def mock_httpx_client() -> Mock:
    """Mock httpx.Client for SDK requests."""
    mock_client = Mock(spec=httpx.Client)
    mock_client.request = Mock()
    mock_client.timeout = httpx.Timeout(timeout=600.0, connect=5.0)
    return mock_client
```

### Mock Async Client (httpx.AsyncClient)
```python
@pytest.fixture
async def mock_async_httpx_client() -> Mock:
    """Mock httpx.AsyncClient for async SDK requests."""
    mock_client = Mock(spec=httpx.AsyncClient)
    mock_client.request = AsyncMock()
    mock_client.timeout = httpx.Timeout(timeout=600.0, connect=5.0)
    return mock_client
```

## Entity Relationships Diagram

```
Workspace
    └── Bot (1:N)
        └── Conversation (1:N)
            └── Chat (1:N)
                └── Message (1:N)
                └── ChatEvent (streaming, 1:N)

Bot
    └── Workflow (1:N)
        └── WorkflowRun (1:N)

All entities reference:
    - HTTPResponse (for API interactions)
    - ClientConfig (for authentication)
```

## Test Data Generation Strategies

### Strategy 1: Static Fixtures
- **Use Case**: Stable test data that doesn't change
- **Examples**: API tokens, bot IDs, workspace IDs
- **Implementation**: @pytest.fixture with hardcoded values

### Strategy 2: Parametrized Fixtures
- **Use Case**: Testing multiple scenarios with different data
- **Examples**: Different status codes, multiple event types
- **Implementation**: @pytest.fixture with @pytest.mark.parametrize

### Strategy 3: Factory Fixtures
- **Use Case**: Dynamic test data generation
- **Examples**: Creating multiple bots with different properties
- **Implementation**: @pytest.fixture returning factory function

```python
@pytest.fixture
def bot_factory():
    """Factory for creating bot test data."""
    def _create_bot(bot_id: str, name: str, workspace_id: str) -> dict[str, Any]:
        return {
            "bot_id": bot_id,
            "name": name,
            "workspace_id": workspace_id,
            "created_at": int(time.time())
        }
    return _create_bot

def test_multiple_bots(bot_factory):
    bot1 = bot_factory("bot-1", "First Bot", "workspace-1")
    bot2 = bot_factory("bot-2", "Second Bot", "workspace-1")
    # test with multiple bots
```

## Mock Data Realism

### Coze-Specific Patterns

1. **ID Format**: Numeric strings (e.g., "7379462189365198898")
2. **Timestamps**: Unix timestamps (seconds since epoch)
3. **Logid**: Always present in responses (format: "req-{uuid}")
4. **Event Format**: Server-Sent Events (SSE) format for streaming
5. **Usage Stats**: Always include token_count, input_count, output_count

### Response Structure Consistency

All mock responses follow Coze API patterns from official documentation:
- Success responses include `logid` field
- Error responses include `error` and `message` fields
- Streaming responses use SSE format: `event: {type}\ndata: {json}`
- Pagination responses include `page_num`, `has_more`, `items`

## Summary

This data model provides a comprehensive foundation for Coze SDK integration testing. All test entities, fixtures, and validation rules are designed to:

1. **Mirror Real API Behavior**: Mock structures match actual Coze API responses
2. **Support All Test Scenarios**: Cover client initialization, operations, streaming, pagination
3. **Enable Type Safety**: All fixtures include type hints for mypy compliance
4. **Promote Reusability**: Shared fixtures reduce duplication across test modules
5. **Facilitate Maintenance**: Clear structure makes updating tests straightforward

The test data model serves as both documentation and implementation guide for creating the comprehensive Coze SDK test suite.
