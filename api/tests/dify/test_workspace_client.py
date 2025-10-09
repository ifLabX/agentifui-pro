"""
Tests for WorkspaceClient.

This module tests the WorkspaceClient functionality including:
- Getting available models by model type
"""

from unittest.mock import Mock

from dify_client import WorkspaceClient


class TestWorkspaceClientInitialization:
    """Test WorkspaceClient initialization."""

    def test_workspace_client_inherits_from_dify_client(
        self, mock_api_key: str
    ) -> None:
        """Test that WorkspaceClient inherits from DifyClient."""
        client = WorkspaceClient(api_key=mock_api_key)

        assert hasattr(client, "api_key")
        assert hasattr(client, "base_url")
        assert client.api_key == mock_api_key


class TestWorkspaceClientGetAvailableModels:
    """Test getting available models."""

    def test_get_available_models_llm(
        self,
        mock_api_key: str,
        mock_requests_request: Mock,
        mock_successful_response: Mock,
    ) -> None:
        """Test getting available LLM models."""
        mock_requests_request.return_value = mock_successful_response

        client = WorkspaceClient(api_key=mock_api_key)
        response = client.get_available_models(model_type="llm")

        # Verify request
        mock_requests_request.assert_called_once()
        call_args = mock_requests_request.call_args[0]
        assert call_args[0] == "GET"
        assert "/workspaces/current/models/model-types/llm" in call_args[1]
        assert response == mock_successful_response

    def test_get_available_models_text_embedding(
        self,
        mock_api_key: str,
        mock_requests_request: Mock,
        mock_successful_response: Mock,
    ) -> None:
        """Test getting available text embedding models."""
        mock_requests_request.return_value = mock_successful_response

        client = WorkspaceClient(api_key=mock_api_key)
        response = client.get_available_models(model_type="text-embedding")

        # Verify request
        call_args = mock_requests_request.call_args[0]
        assert "/workspaces/current/models/model-types/text-embedding" in call_args[1]
        assert response == mock_successful_response

    def test_get_available_models_rerank(
        self,
        mock_api_key: str,
        mock_requests_request: Mock,
        mock_successful_response: Mock,
    ) -> None:
        """Test getting available rerank models."""
        mock_requests_request.return_value = mock_successful_response

        client = WorkspaceClient(api_key=mock_api_key)
        response = client.get_available_models(model_type="rerank")

        # Verify request
        call_args = mock_requests_request.call_args[0]
        assert "/workspaces/current/models/model-types/rerank" in call_args[1]
        assert response == mock_successful_response

    def test_get_available_models_speech_to_text(
        self,
        mock_api_key: str,
        mock_requests_request: Mock,
        mock_successful_response: Mock,
    ) -> None:
        """Test getting available speech-to-text models."""
        mock_requests_request.return_value = mock_successful_response

        client = WorkspaceClient(api_key=mock_api_key)
        response = client.get_available_models(model_type="speech2text")

        # Verify request
        call_args = mock_requests_request.call_args[0]
        assert "/workspaces/current/models/model-types/speech2text" in call_args[1]
        assert response == mock_successful_response

    def test_get_available_models_text_to_speech(
        self,
        mock_api_key: str,
        mock_requests_request: Mock,
        mock_successful_response: Mock,
    ) -> None:
        """Test getting available text-to-speech models."""
        mock_requests_request.return_value = mock_successful_response

        client = WorkspaceClient(api_key=mock_api_key)
        response = client.get_available_models(model_type="tts")

        # Verify request
        call_args = mock_requests_request.call_args[0]
        assert "/workspaces/current/models/model-types/tts" in call_args[1]
        assert response == mock_successful_response

    def test_get_available_models_moderation(
        self,
        mock_api_key: str,
        mock_requests_request: Mock,
        mock_successful_response: Mock,
    ) -> None:
        """Test getting available moderation models."""
        mock_requests_request.return_value = mock_successful_response

        client = WorkspaceClient(api_key=mock_api_key)
        response = client.get_available_models(model_type="moderation")

        # Verify request
        call_args = mock_requests_request.call_args[0]
        assert "/workspaces/current/models/model-types/moderation" in call_args[1]
        assert response == mock_successful_response
