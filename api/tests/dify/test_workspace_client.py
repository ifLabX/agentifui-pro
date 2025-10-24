"""
Tests for AsyncWorkspaceClient.

This module tests the AsyncWorkspaceClient functionality including:
- Getting available models by model type
"""

from dify_client.async_client import AsyncWorkspaceClient
from pytest_httpx import HTTPXMock


class TestWorkspaceClientInitialization:
    """Test AsyncWorkspaceClient initialization."""

    async def test_workspace_client_inherits_from_dify_client(self, mock_api_key: str) -> None:
        """Test that AsyncWorkspaceClient inherits from AsyncDifyClient."""
        client = AsyncWorkspaceClient(api_key=mock_api_key)

        assert hasattr(client, "api_key")
        assert hasattr(client, "base_url")
        assert client.api_key == mock_api_key


class TestWorkspaceClientGetAvailableModels:
    """Test getting available models."""

    async def test_get_available_models_llm(
        self,
        httpx_mock: HTTPXMock,
        mock_api_key: str,
    ) -> None:
        """Test getting available LLM models."""
        httpx_mock.add_response(
            url="https://api.dify.ai/v1/workspaces/current/models/model-types/llm",
            method="GET",
            json={"data": []},
            status_code=200,
        )

        client = AsyncWorkspaceClient(api_key=mock_api_key)
        response = await client.get_available_models(model_type="llm")

        # Verify request
        requests = httpx_mock.get_requests()
        assert len(requests) == 1
        assert requests[0].method == "GET"
        assert "/workspaces/current/models/model-types/llm" in str(requests[0].url)
        assert response.status_code == 200

    async def test_get_available_models_text_embedding(
        self,
        httpx_mock: HTTPXMock,
        mock_api_key: str,
    ) -> None:
        """Test getting available text embedding models."""
        httpx_mock.add_response(
            url="https://api.dify.ai/v1/workspaces/current/models/model-types/text-embedding",
            method="GET",
            json={"data": []},
            status_code=200,
        )

        client = AsyncWorkspaceClient(api_key=mock_api_key)
        response = await client.get_available_models(model_type="text-embedding")

        # Verify request
        requests = httpx_mock.get_requests()
        assert len(requests) == 1
        assert "/workspaces/current/models/model-types/text-embedding" in str(requests[0].url)
        assert response.status_code == 200

    async def test_get_available_models_rerank(
        self,
        httpx_mock: HTTPXMock,
        mock_api_key: str,
    ) -> None:
        """Test getting available rerank models."""
        httpx_mock.add_response(
            url="https://api.dify.ai/v1/workspaces/current/models/model-types/rerank",
            method="GET",
            json={"data": []},
            status_code=200,
        )

        client = AsyncWorkspaceClient(api_key=mock_api_key)
        response = await client.get_available_models(model_type="rerank")

        # Verify request
        requests = httpx_mock.get_requests()
        assert len(requests) == 1
        assert "/workspaces/current/models/model-types/rerank" in str(requests[0].url)
        assert response.status_code == 200

    async def test_get_available_models_speech_to_text(
        self,
        httpx_mock: HTTPXMock,
        mock_api_key: str,
    ) -> None:
        """Test getting available speech-to-text models."""
        httpx_mock.add_response(
            url="https://api.dify.ai/v1/workspaces/current/models/model-types/speech2text",
            method="GET",
            json={"data": []},
            status_code=200,
        )

        client = AsyncWorkspaceClient(api_key=mock_api_key)
        response = await client.get_available_models(model_type="speech2text")

        # Verify request
        requests = httpx_mock.get_requests()
        assert len(requests) == 1
        assert "/workspaces/current/models/model-types/speech2text" in str(requests[0].url)
        assert response.status_code == 200

    async def test_get_available_models_text_to_speech(
        self,
        httpx_mock: HTTPXMock,
        mock_api_key: str,
    ) -> None:
        """Test getting available text-to-speech models."""
        httpx_mock.add_response(
            url="https://api.dify.ai/v1/workspaces/current/models/model-types/tts",
            method="GET",
            json={"data": []},
            status_code=200,
        )

        client = AsyncWorkspaceClient(api_key=mock_api_key)
        response = await client.get_available_models(model_type="tts")

        # Verify request
        requests = httpx_mock.get_requests()
        assert len(requests) == 1
        assert "/workspaces/current/models/model-types/tts" in str(requests[0].url)
        assert response.status_code == 200

    async def test_get_available_models_moderation(
        self,
        httpx_mock: HTTPXMock,
        mock_api_key: str,
    ) -> None:
        """Test getting available moderation models."""
        httpx_mock.add_response(
            url="https://api.dify.ai/v1/workspaces/current/models/model-types/moderation",
            method="GET",
            json={"data": []},
            status_code=200,
        )

        client = AsyncWorkspaceClient(api_key=mock_api_key)
        response = await client.get_available_models(model_type="moderation")

        # Verify request
        requests = httpx_mock.get_requests()
        assert len(requests) == 1
        assert "/workspaces/current/models/model-types/moderation" in str(requests[0].url)
        assert response.status_code == 200
