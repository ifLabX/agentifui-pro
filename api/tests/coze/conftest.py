"""
Coze SDK test configuration and fixtures.

This module provides shared test fixtures and utilities for testing Coze SDK clients.
All tests use mocks to avoid making real API calls.
"""

from typing import Any
from unittest.mock import Mock

import httpx
import pytest


# ============================================================================
# Authentication Fixtures
# ============================================================================


@pytest.fixture
def mock_coze_api_token() -> str:
    """Provide a mock API token for Coze authentication."""
    return "test-coze-token-12345"


@pytest.fixture
def mock_coze_base_url() -> str:
    """Provide a mock base URL for Coze API."""
    return "https://api.coze.cn/v1"


# ============================================================================
# Entity ID Fixtures
# ============================================================================


@pytest.fixture
def mock_bot_id() -> str:
    """Provide a sample bot ID in Coze format."""
    return "7379462189365198898"


@pytest.fixture
def mock_workspace_id() -> str:
    """Provide a sample workspace ID."""
    return "workspace-12345-abcde"


@pytest.fixture
def mock_conversation_id() -> str:
    """Provide a sample conversation ID."""
    return "7381473525342978089"


@pytest.fixture
def mock_chat_id() -> str:
    """Provide a sample chat ID."""
    return "7382159487131697202"


@pytest.fixture
def mock_workflow_id() -> str:
    """Provide a sample workflow ID."""
    return "workflow-77777-88888"


@pytest.fixture
def mock_workflow_run_id() -> str:
    """Provide a sample workflow run ID."""
    return "run-12345-abc"


# ============================================================================
# HTTP Response Fixtures
# ============================================================================


@pytest.fixture
def mock_successful_response() -> Mock:
    """Create a mock successful HTTP response."""
    response = Mock(spec=httpx.Response)
    response.status_code = 200
    response.json.return_value = {
        "success": True,
        "data": {"message": "Operation successful"},
        "logid": "req-12345-abcde",
    }
    response.headers = {"Content-Type": "application/json"}
    return response


@pytest.fixture
def mock_error_response() -> Mock:
    """Create a mock error HTTP response."""
    response = Mock(spec=httpx.Response)
    response.status_code = 400
    response.json.return_value = {
        "error": "Bad Request",
        "message": "Invalid parameters",
        "logid": "req-error-789",
    }
    response.headers = {"Content-Type": "application/json"}
    return response


@pytest.fixture
def mock_streaming_events() -> list[bytes]:
    """Mock streaming event data for chat/workflow streaming."""
    return [
        b'event: conversation.chat.created\ndata: {"id":"chat-123","status":"created"}',
        b'event: conversation.chat.in_progress\ndata: {"id":"chat-123","status":"in_progress"}',
        b'event: conversation.message.delta\ndata: {"message":{"content":"Hello"}}',
        b'event: conversation.message.delta\ndata: {"message":{"content":" World"}}',
        b'event: conversation.chat.completed\ndata: {"id":"chat-123","status":"completed","usage":{"token_count":633}}',
    ]


@pytest.fixture
def mock_streaming_response(mock_streaming_events: list[bytes]) -> Mock:
    """Create a mock streaming HTTP response."""
    response = Mock(spec=httpx.Response)
    response.status_code = 200
    response.headers = {"Content-Type": "text/event-stream"}
    response.iter_lines = Mock(return_value=iter(mock_streaming_events))
    return response


# ============================================================================
# Sample Entity Data Fixtures
# ============================================================================


@pytest.fixture
def sample_bot_data() -> dict[str, Any]:
    """Provide sample bot data for testing."""
    return {
        "bot_id": "7379462189365198898",
        "name": "Test Bot",
        "description": "Bot for testing",
        "workspace_id": "workspace-12345-abcde",
        "created_at": 1718792949,
    }


@pytest.fixture
def sample_chat_data() -> dict[str, Any]:
    """Provide sample chat data for testing."""
    return {
        "id": "7382159487131697202",
        "conversation_id": "7381473525342978089",
        "bot_id": "7379462189365198898",
        "status": "completed",
        "usage": {
            "token_count": 633,
            "output_count": 19,
            "input_count": 614,
        },
        "created_at": 1718792949,
        "completed_at": 1718792949,
    }


@pytest.fixture
def sample_user_message() -> dict[str, Any]:
    """Provide sample user message data."""
    return {
        "role": "user",
        "content": "What is the weather today?",
        "content_type": "text",
    }


@pytest.fixture
def sample_assistant_message() -> dict[str, Any]:
    """Provide sample assistant message data."""
    return {
        "role": "assistant",
        "content": "The weather today is sunny with a high of 75°F.",
        "content_type": "text",
    }


@pytest.fixture
def sample_workflow_inputs() -> dict[str, Any]:
    """Provide sample workflow input data."""
    return {
        "query": "Process this data",
        "context": "User workflow request",
        "parameters": {"mode": "batch"},
    }


@pytest.fixture
def sample_workflow_data() -> dict[str, Any]:
    """Provide sample workflow execution data."""
    return {
        "workflow_id": "workflow-77777-88888",
        "workflow_run_id": "run-12345-abc",
        "status": "succeeded",
        "inputs": {"query": "Process this data"},
        "outputs": {"result": "Data processed successfully"},
        "created_at": 1718792949,
        "completed_at": 1718792955,
    }


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
        "logid": "req-pagination-123",
    }
