"""
Tests for CompletionClient.

This module tests the CompletionClient functionality including:
- Completion message creation (blocking and streaming modes)
- Input handling and file attachments
"""

import json

from dify_client.async_client import AsyncCompletionClient
from pytest_httpx import HTTPXMock


class TestCompletionClientInitialization:
    """Test CompletionClient initialization."""

    async def test_completion_client_inherits_from_dify_client(self, mock_api_key: str) -> None:
        """Test that CompletionClient inherits from DifyClient."""
        client = AsyncCompletionClient(api_key=mock_api_key)

        assert hasattr(client, "api_key")
        assert hasattr(client, "base_url")
        assert client.api_key == mock_api_key


class TestCompletionClientCreateMessage:
    """Test completion message creation."""

    async def test_create_completion_message_blocking(
        self,
        httpx_mock: HTTPXMock,
        mock_api_key: str,
        sample_inputs: dict,
        mock_user: str,
    ) -> None:
        """Test creating a completion message in blocking mode."""
        httpx_mock.add_response(
            url="https://api.dify.ai/v1/completion-messages",
            method="POST",
            json={"success": True, "message_id": "msg-123"},
            status_code=200,
        )

        client = AsyncCompletionClient(api_key=mock_api_key)
        response = await client.create_completion_message(
            inputs=sample_inputs,
            response_mode="blocking",
            user=mock_user,
        )

        # Verify request
        requests = httpx_mock.get_requests()
        assert len(requests) == 1
        request = requests[0]
        assert request.method == "POST"
        assert "/completion-messages" in str(request.url)

        request_body = json.loads(request.content)
        assert request_body["inputs"] == sample_inputs
        assert request_body["response_mode"] == "blocking"
        assert request_body["user"] == mock_user
        assert response.status_code == 200

    async def test_create_completion_message_streaming(
        self,
        httpx_mock: HTTPXMock,
        mock_api_key: str,
        sample_inputs: dict,
        mock_user: str,
    ) -> None:
        """Test creating a completion message in streaming mode."""
        httpx_mock.add_response(
            url="https://api.dify.ai/v1/completion-messages",
            method="POST",
            json={"success": True, "message_id": "msg-123"},
            status_code=200,
        )

        client = AsyncCompletionClient(api_key=mock_api_key)
        response = await client.create_completion_message(
            inputs=sample_inputs,
            response_mode="streaming",
            user=mock_user,
        )

        # Verify request
        requests = httpx_mock.get_requests()
        assert len(requests) == 1
        request = requests[0]
        assert request.method == "POST"
        assert "/completion-messages" in str(request.url)

        request_body = json.loads(request.content)
        assert request_body["inputs"] == sample_inputs
        assert request_body["response_mode"] == "streaming"
        assert request_body["user"] == mock_user
        assert response.status_code == 200

    async def test_create_completion_message_with_files(
        self,
        httpx_mock: HTTPXMock,
        mock_api_key: str,
        sample_inputs: dict,
        mock_user: str,
    ) -> None:
        """Test creating a completion message with file attachments."""
        httpx_mock.add_response(
            url="https://api.dify.ai/v1/completion-messages",
            method="POST",
            json={"success": True, "message_id": "msg-123"},
            status_code=200,
        )

        # Use JSON-serializable file references instead of raw bytes
        json_serializable_files = {
            "file_id": "file-123",
            "type": "document",
        }

        client = AsyncCompletionClient(api_key=mock_api_key)
        response = await client.create_completion_message(
            inputs=sample_inputs,
            response_mode="blocking",
            user=mock_user,
            files=json_serializable_files,
        )

        # Verify request
        requests = httpx_mock.get_requests()
        assert len(requests) == 1
        request = requests[0]
        assert request.method == "POST"
        assert "/completion-messages" in str(request.url)

        request_body = json.loads(request.content)
        assert request_body["inputs"] == sample_inputs
        assert request_body["response_mode"] == "blocking"
        assert request_body["user"] == mock_user
        assert request_body["files"] == json_serializable_files
        assert response.status_code == 200

    async def test_create_completion_message_without_files(
        self,
        httpx_mock: HTTPXMock,
        mock_api_key: str,
        sample_inputs: dict,
        mock_user: str,
    ) -> None:
        """Test creating a completion message without files."""
        httpx_mock.add_response(
            url="https://api.dify.ai/v1/completion-messages",
            method="POST",
            json={"success": True, "message_id": "msg-123"},
            status_code=200,
        )

        client = AsyncCompletionClient(api_key=mock_api_key)
        response = await client.create_completion_message(
            inputs=sample_inputs,
            response_mode="blocking",
            user=mock_user,
            files=None,
        )

        # Verify request
        requests = httpx_mock.get_requests()
        assert len(requests) == 1
        request = requests[0]
        assert request.method == "POST"
        assert "/completion-messages" in str(request.url)

        request_body = json.loads(request.content)
        assert request_body["inputs"] == sample_inputs
        assert request_body["response_mode"] == "blocking"
        assert request_body["user"] == mock_user
        assert response.status_code == 200

    async def test_create_completion_message_various_inputs(
        self,
        httpx_mock: HTTPXMock,
        mock_api_key: str,
        mock_user: str,
    ) -> None:
        """Test creating completion message with various input types."""
        httpx_mock.add_response(
            url="https://api.dify.ai/v1/completion-messages",
            method="POST",
            json={"success": True, "message_id": "msg-123"},
            status_code=200,
        )

        client = AsyncCompletionClient(api_key=mock_api_key)
        complex_inputs = {
            "text": "Generate a report",
            "format": "json",
            "parameters": {
                "max_length": 1000,
                "temperature": 0.7,
            },
        }

        response = await client.create_completion_message(
            inputs=complex_inputs,
            response_mode="blocking",
            user=mock_user,
        )

        # Verify request
        requests = httpx_mock.get_requests()
        assert len(requests) == 1
        request = requests[0]
        assert request.method == "POST"
        assert "/completion-messages" in str(request.url)

        request_body = json.loads(request.content)
        assert request_body["inputs"] == complex_inputs
        assert request_body["response_mode"] == "blocking"
        assert request_body["user"] == mock_user
        assert response.status_code == 200
