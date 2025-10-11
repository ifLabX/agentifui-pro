r"""
Dify SDK test configuration and fixtures.

This module provides shared test fixtures and utilities for testing Dify SDK clients.
All tests use mocks to avoid making real API calls.

HTTP Request Mocking:
- This module uses pytest-httpx for mocking httpx.AsyncClient requests.
- The `httpx_mock` fixture is automatically provided by pytest-httpx (no manual definition needed).
- All tests should be async functions (`async def test_*`) due to pytest-asyncio auto mode.
- Configure responses with: httpx_mock.add_response(url="...", method="POST", json={...}, status_code=200)
- Verify requests with: httpx_mock.get_requests() or httpx_mock.get_request()

Migration from requests to httpx:
- Use async client classes: AsyncDifyClient, AsyncChatClient, AsyncWorkflowClient, etc.
  from dify_client.async_client import AsyncDifyClient
- All client method calls must use await keyword:
  response = await client.operation()
- Import json module for request body parsing in assertions:
  import json
  request_body = json.loads(request.content)
- Use regex patterns for URLs with query parameters:
  import re
  httpx_mock.add_response(url=re.compile(r"https://api\.dify\.ai/v1/endpoint\?.*"), ...)

Example async test pattern:
    async def test_operation(httpx_mock: HTTPXMock, mock_api_key: str):
        httpx_mock.add_response(
            url="https://api.dify.ai/v1/endpoint",
            method="POST",
            json={"success": True},
            status_code=200,
        )
        client = AsyncDifyClient(api_key=mock_api_key)
        response = await client.operation()

        # Verify request
        requests = httpx_mock.get_requests()
        assert len(requests) == 1
        assert requests[0].method == "POST"
        assert response.status_code == 200

File Upload Tests:
- File upload tests require special async file handling with aiofiles
- Standard httpx_mock patterns may not work for multipart/form-data with file objects
- Consider using async context managers for file operations in these tests
"""

import os
from typing import Any

import pytest


@pytest.fixture(scope="session", autouse=True)
def disable_proxy_for_tests():
    """Disable proxy settings during tests to avoid SOCKS proxy issues with httpx."""
    original_env = {}
    proxy_vars = ["http_proxy", "https_proxy", "all_proxy", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY"]

    for var in proxy_vars:
        if var in os.environ:
            original_env[var] = os.environ[var]
            del os.environ[var]

    yield

    # Restore original proxy settings
    for var, value in original_env.items():
        os.environ[var] = value


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


@pytest.fixture
def sample_message_id() -> str:
    """Provide a sample message ID."""
    return "msg-67890-fghij"


@pytest.fixture
def sample_task_id() -> str:
    """Provide a sample task ID."""
    return "task-11111-22222"


@pytest.fixture
def sample_document_id() -> str:
    """Provide a sample document ID."""
    return "doc-33333-44444"


@pytest.fixture
def sample_dataset_id() -> str:
    """Provide a sample dataset ID."""
    return "dataset-55555-66666"


@pytest.fixture
def sample_workflow_id() -> str:
    """Provide a sample workflow ID."""
    return "workflow-77777-88888"


@pytest.fixture
def sample_segment_data() -> dict[str, Any]:
    """Provide sample segment data for knowledge base testing."""
    return {
        "content": "This is a test segment",
        "answer": "This is the answer",
        "keywords": ["test", "segment"],
    }


@pytest.fixture
def sample_metadata() -> dict[str, Any]:
    """Provide sample metadata for testing."""
    return {
        "key": "test_metadata",
        "value": "test_value",
        "type": "string",
    }


@pytest.fixture
def sample_retrieval_model() -> dict[str, Any]:
    """Provide sample retrieval model configuration."""
    return {
        "search_method": "semantic",
        "reranking_enable": True,
        "reranking_model": {
            "reranking_provider_name": "test_provider",
            "reranking_model_name": "test_model",
        },
        "top_k": 5,
        "score_threshold_enabled": True,
        "score_threshold": 0.7,
    }


class MockFile:
    """Mock file object for testing file operations."""

    def __init__(self, content: bytes = b"test content", filename: str = "test.txt"):
        self.content = content
        self.filename = filename
        self.closed = False

    def read(self) -> bytes:
        return self.content

    def close(self) -> None:
        self.closed = True

    def __enter__(self) -> "MockFile":
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.close()


@pytest.fixture
def mock_file() -> MockFile:
    """Provide a mock file object for testing."""
    return MockFile()


@pytest.fixture
def sample_process_rule() -> dict[str, Any]:
    """Provide sample process rule for document processing."""
    return {
        "mode": "custom",
        "rules": {
            "pre_processing_rules": [
                {"id": "remove_extra_spaces", "enabled": True},
                {"id": "remove_urls_emails", "enabled": True},
            ],
            "segmentation": {
                "separator": "\n",
                "max_tokens": 500,
            },
        },
    }


@pytest.fixture
def sample_annotation_data() -> dict[str, Any]:
    """Provide sample annotation data for testing."""
    return {
        "question": "What is AI?",
        "answer": "Artificial Intelligence is...",
    }


@pytest.fixture
def sample_rag_pipeline_data() -> dict[str, Any]:
    """Provide sample RAG pipeline data for testing."""
    return {
        "inputs": {"query": "test query"},
        "datasource_type": "external",
        "datasource_info_list": [
            {
                "datasource_id": "ds-123",
                "config": {"api_key": "test"},
            }
        ],
        "start_node_id": "node-start",
    }
