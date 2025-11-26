# Dify SDK Test Suite

Comprehensive pytest test suite for all Dify SDK clients and APIs.

## Overview

This test suite provides **117 comprehensive tests** covering all APIs across 6 Dify SDK clients:

- **DifyClient** (Base Client) - 18 tests
- **ChatClient** - 27 tests
- **CompletionClient** - 6 tests
- **WorkflowClient** - 16 tests
- **WorkspaceClient** - 7 tests
- **KnowledgeBaseClient** - 43 tests

## Test Structure

```
tests/dify/
├── conftest.py                    # Shared fixtures and test utilities
├── test_dify_client.py            # Base DifyClient tests
├── test_chat_client.py            # ChatClient tests
├── test_completion_client.py      # CompletionClient tests
├── test_workflow_client.py        # WorkflowClient tests
├── test_workspace_client.py       # WorkspaceClient tests
├── test_knowledge_base_client.py  # KnowledgeBaseClient tests
└── README.md                      # This file
```

## Running Tests

### Run all Dify tests
```bash
cd api
uv run pytest tests/dify/ -v
```

### Run specific client tests
```bash
# Test ChatClient only
uv run pytest tests/dify/test_chat_client.py -v

# Test KnowledgeBaseClient only
uv run pytest tests/dify/test_knowledge_base_client.py -v
```

### Run specific test class
```bash
# Test chat message creation
uv run pytest tests/dify/test_chat_client.py::TestChatClientCreateMessage -v

# Test workflow logs
uv run pytest tests/dify/test_workflow_client.py::TestWorkflowClientGetLogs -v
```

### Run with custom output
```bash
# Show test names only
uv run pytest tests/dify/ --collect-only

# Show short test summary
uv run pytest tests/dify/ -v --tb=short
```

## Test Coverage

### DifyClient (Base Client)
✅ **Initialization & Configuration**
- Default and custom base URL initialization
- API key storage and management

✅ **HTTP Request Methods**
- GET, POST, DELETE requests
- Request headers (Authorization, Content-Type)
- URL construction and parameter handling
- Streaming support

✅ **File Operations**
- File upload with multipart/form-data
- File preview retrieval

✅ **Common APIs**
- Message feedback (like/dislike)
- Application parameters
- File upload endpoint
- Text-to-audio conversion (streaming & non-streaming)
- Meta information retrieval
- App info and site info
- File preview

### ChatClient
✅ **Message Creation**
- Blocking and streaming modes
- Conversation continuity (conversation_id)
- File attachments support
- Default parameter handling

✅ **Conversation Management**
- List conversations (pagination, pinned filter)
- Rename conversations (manual and auto-generated names)
- Delete conversations
- Get conversation messages (pagination, filters)

✅ **Message Operations**
- Get suggested messages
- Stop message generation
- Audio-to-text conversion

✅ **Annotation APIs**
- Enable/disable annotation reply
- Get annotation status
- List annotations (pagination, keyword filter)
- Create, update, delete annotations
- Validation error handling

### CompletionClient
✅ **Completion Messages**
- Blocking and streaming response modes
- Input validation and handling
- File attachments support
- Complex input structures

### WorkflowClient
✅ **Workflow Execution**
- Run workflows (blocking and streaming)
- Stop running workflows
- Get workflow results
- Run specific workflow by ID

✅ **Workflow Logs**
- Default pagination
- Keyword filtering
- Status filtering (succeeded, failed, stopped)
- Date range filtering (before/after)
- Creator filtering (session ID, account)
- Combined filter scenarios

### WorkspaceClient
✅ **Model Management**
- Get available models by type:
  - LLM models
  - Text embedding models
  - Rerank models
  - Speech-to-text models
  - Text-to-speech models
  - Moderation models

### KnowledgeBaseClient (Most Comprehensive)
✅ **Dataset Management**
- Create datasets
- List datasets (pagination)
- Delete datasets

✅ **Document Operations - Text-based**
- Create documents from text
- Update documents with text
- Custom indexing techniques
- Process rules configuration

✅ **Document Operations - File-based**
- Create documents from files
- Update documents with files
- Original document replacement
- File handling and upload

✅ **Document Listing & Deletion**
- List documents (pagination, keyword filter)
- Delete documents
- Batch indexing status

✅ **Segment Management**
- Add segments to documents
- Query segments (filters, status)
- Update document segments
- Delete document segments

✅ **Advanced Features**
- Hit testing (with/without retrieval models)
- External retrieval models

✅ **Metadata Management**
- Get, create, update dataset metadata
- Built-in metadata operations
- Bulk document metadata updates

✅ **Dataset Tags**
- List all available tags
- Bind tags to datasets
- Unbind tags from datasets
- Get dataset-specific tags

✅ **RAG Pipeline**
- Get datasource plugins
- Run datasource nodes (streaming)
- Run RAG pipeline (blocking and streaming)
- Upload pipeline files

## Test Fixtures

All tests use comprehensive fixtures defined in `conftest.py`:

### API Configuration
- `mock_api_key` - Test API key
- `mock_base_url` - Test base URL
- `mock_user` - Test user identifier

### HTTP Mocking
- `mock_successful_response` - Successful API response
- `mock_error_response` - Error API response
- `mock_streaming_response` - Streaming API response
- `mock_requests_request` - Mocked requests.request

### Test Data
- `sample_inputs` - Sample input data
- `sample_files` - Sample file data
- `sample_conversation_id` - Test conversation ID
- `sample_message_id` - Test message ID
- `sample_task_id` - Test task ID
- `sample_document_id` - Test document ID
- `sample_dataset_id` - Test dataset ID
- `sample_workflow_id` - Test workflow ID
- `sample_segment_data` - Sample segment data
- `sample_metadata` - Sample metadata
- `sample_retrieval_model` - Sample retrieval model config
- `sample_process_rule` - Sample document processing rules
- `sample_annotation_data` - Sample annotation data
- `sample_rag_pipeline_data` - Sample RAG pipeline data

## Testing Approach

### Mocking Strategy
All tests use **mock HTTP requests** to avoid real API calls:
- No external dependencies required
- Fast test execution (<1 second for all 117 tests)
- No API rate limiting concerns
- Reproducible test results

### Test Organization
Tests are organized by:
1. **Client type** (separate file per client)
2. **Functionality** (test classes per feature area)
3. **Scenario** (individual test methods for specific cases)

### Naming Conventions
- Test files: `test_<client_name>_client.py`
- Test classes: `Test<Client><Feature>`
- Test methods: `test_<specific_scenario>`

## Key Features Tested

### Request Validation
✅ HTTP method correctness (GET, POST, DELETE, PATCH, PUT)
✅ URL construction and endpoint paths
✅ Request headers (Authorization Bearer tokens)
✅ JSON payload structure
✅ Query parameters
✅ File upload handling

### Response Handling
✅ Successful responses
✅ Streaming responses
✅ Error responses
✅ Response mode switching (blocking vs streaming)

### Edge Cases
✅ None/null value handling
✅ Optional parameter defaults
✅ Missing required parameters (ValueError)
✅ Empty collections
✅ Pagination boundaries

### Client Inheritance
✅ All clients inherit from DifyClient
✅ Base client functionality available in all clients
✅ Proper initialization patterns

## Quality Assurance

### Type Safety
- All test methods have complete type annotations
- Fixtures are properly typed
- Mock objects use `spec` parameter for type checking

### Documentation
- Every test has a descriptive docstring
- Complex scenarios explained in comments
- README provides comprehensive overview

### Maintainability
- DRY principle applied through fixtures
- Clear test organization
- Consistent naming patterns
- Isolated test cases (no dependencies between tests)

## Test Results

```
============================= test session starts ==============================
platform darwin -- Python 3.12.11, pytest-8.4.2, pluggy-1.6.0
collected 117 items

tests/dify/test_chat_client.py::.................... [ 23%]
tests/dify/test_completion_client.py::...... [ 28%]
tests/dify/test_dify_client.py::.................... [ 53%]
tests/dify/test_knowledge_base_client.py::.............................. [ 90%]
tests/dify/test_workflow_client.py::............... [ 94%]
tests/dify/test_workspace_client.py::....... [100%]

============================= 117 passed in 0.13s ==============================
```

**All 117 tests pass successfully** ✅

## Future Enhancements

Potential areas for expansion:
- Integration tests with real Dify API (optional)
- Performance benchmarking tests
- Error handling edge cases
- Concurrent request testing
- Retry logic validation
- Rate limiting behavior

## Contributing

When adding new tests:
1. Follow existing naming conventions
2. Add comprehensive docstrings
3. Use appropriate fixtures from `conftest.py`
4. Test both success and error scenarios
5. Update this README with new coverage

## References

- [Dify SDK Source](https://github.com/langgenius/dify/tree/main/sdks/python-client)
- [pytest Documentation](https://docs.pytest.org/)
- [Project Test Standards](../../../AGENTS.md#testing-requirements)
