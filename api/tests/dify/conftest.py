"""
Dify SDK test configuration and fixtures.

This module provides shared test fixtures and utilities for testing Dify SDK clients.
All tests use mocks to avoid making real API calls.
"""

from collections.abc import Generator
from typing import Any
from unittest.mock import Mock, patch

import pytest
import requests


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
def mock_successful_response() -> Mock:
    """Create a mock successful HTTP response."""
    response = Mock(spec=requests.Response)
    response.status_code = 200
    response.json.return_value = {
        "success": True,
        "data": {"message": "Operation successful"},
    }
    response.text = '{"success": true}'
    response.headers = {"Content-Type": "application/json"}
    response.iter_lines = Mock(return_value=iter([]))
    return response


@pytest.fixture
def mock_error_response() -> Mock:
    """Create a mock error HTTP response."""
    response = Mock(spec=requests.Response)
    response.status_code = 400
    response.json.return_value = {
        "error": "Bad Request",
        "message": "Invalid request parameters",
    }
    response.text = '{"error": "Bad Request"}'
    response.headers = {"Content-Type": "application/json"}
    return response


@pytest.fixture
def mock_streaming_response() -> Mock:
    """Create a mock streaming HTTP response."""
    response = Mock(spec=requests.Response)
    response.status_code = 200
    response.headers = {"Content-Type": "text/event-stream"}

    streaming_data = [
        b'data: {"event": "message", "content": "Hello"}',
        b'data: {"event": "message", "content": " World"}',
        b'data: {"event": "done"}',
    ]
    response.iter_lines = Mock(return_value=iter(streaming_data))
    return response


@pytest.fixture
def mock_requests_request() -> Generator[Mock, None, None]:
    """Mock requests.request to avoid real HTTP calls."""
    with patch("requests.request") as mock_request:
        yield mock_request


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
