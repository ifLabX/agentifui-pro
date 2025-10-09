"""
Tests for CompletionClient.

This module tests the CompletionClient functionality including:
- Completion message creation (blocking and streaming modes)
- Input handling and file attachments
"""

from unittest.mock import Mock

from dify_client import CompletionClient


class TestCompletionClientInitialization:
    """Test CompletionClient initialization."""

    def test_completion_client_inherits_from_dify_client(
        self, mock_api_key: str
    ) -> None:
        """Test that CompletionClient inherits from DifyClient."""
        client = CompletionClient(api_key=mock_api_key)

        assert hasattr(client, "api_key")
        assert hasattr(client, "base_url")
        assert client.api_key == mock_api_key


class TestCompletionClientCreateMessage:
    """Test completion message creation."""

    def test_create_completion_message_blocking(
        self,
        mock_api_key: str,
        mock_requests_request: Mock,
        mock_successful_response: Mock,
        sample_inputs: dict,
        mock_user: str,
    ) -> None:
        """Test creating a completion message in blocking mode."""
        mock_requests_request.return_value = mock_successful_response

        client = CompletionClient(api_key=mock_api_key)
        response = client.create_completion_message(
            inputs=sample_inputs,
            response_mode="blocking",
            user=mock_user,
        )

        # Verify request
        mock_requests_request.assert_called_once()
        call_args, call_kwargs = mock_requests_request.call_args
        assert call_args[0] == "POST"
        assert "/completion-messages" in call_args[1]
        assert call_kwargs["json"]["inputs"] == sample_inputs
        assert call_kwargs["json"]["response_mode"] == "blocking"
        assert call_kwargs["json"]["user"] == mock_user
        assert call_kwargs["stream"] is False
        assert response == mock_successful_response

    def test_create_completion_message_streaming(
        self,
        mock_api_key: str,
        mock_requests_request: Mock,
        mock_streaming_response: Mock,
        sample_inputs: dict,
        mock_user: str,
    ) -> None:
        """Test creating a completion message in streaming mode."""
        mock_requests_request.return_value = mock_streaming_response

        client = CompletionClient(api_key=mock_api_key)
        response = client.create_completion_message(
            inputs=sample_inputs,
            response_mode="streaming",
            user=mock_user,
        )

        # Verify streaming is enabled
        call_kwargs = mock_requests_request.call_args[1]
        assert call_kwargs["json"]["response_mode"] == "streaming"
        assert call_kwargs["stream"] is True
        assert response == mock_streaming_response

    def test_create_completion_message_with_files(
        self,
        mock_api_key: str,
        mock_requests_request: Mock,
        mock_successful_response: Mock,
        sample_inputs: dict,
        sample_files: dict,
        mock_user: str,
    ) -> None:
        """Test creating a completion message with file attachments."""
        mock_requests_request.return_value = mock_successful_response

        client = CompletionClient(api_key=mock_api_key)
        response = client.create_completion_message(
            inputs=sample_inputs,
            response_mode="blocking",
            user=mock_user,
            files=sample_files,
        )

        # Verify files are included
        call_kwargs = mock_requests_request.call_args[1]
        assert call_kwargs["json"]["files"] == sample_files
        assert response == mock_successful_response

    def test_create_completion_message_without_files(
        self,
        mock_api_key: str,
        mock_requests_request: Mock,
        mock_successful_response: Mock,
        sample_inputs: dict,
        mock_user: str,
    ) -> None:
        """Test creating a completion message without files."""
        mock_requests_request.return_value = mock_successful_response

        client = CompletionClient(api_key=mock_api_key)
        response = client.create_completion_message(
            inputs=sample_inputs,
            response_mode="blocking",
            user=mock_user,
            files=None,
        )

        # Verify files is None
        call_kwargs = mock_requests_request.call_args[1]
        assert call_kwargs["json"]["files"] is None
        assert response == mock_successful_response

    def test_create_completion_message_various_inputs(
        self,
        mock_api_key: str,
        mock_requests_request: Mock,
        mock_successful_response: Mock,
        mock_user: str,
    ) -> None:
        """Test creating completion message with various input types."""
        mock_requests_request.return_value = mock_successful_response

        client = CompletionClient(api_key=mock_api_key)
        complex_inputs = {
            "text": "Generate a report",
            "format": "json",
            "parameters": {
                "max_length": 1000,
                "temperature": 0.7,
            },
        }

        response = client.create_completion_message(
            inputs=complex_inputs,
            response_mode="blocking",
            user=mock_user,
        )

        # Verify complex inputs are passed correctly
        call_kwargs = mock_requests_request.call_args[1]
        assert call_kwargs["json"]["inputs"] == complex_inputs
        assert response == mock_successful_response
