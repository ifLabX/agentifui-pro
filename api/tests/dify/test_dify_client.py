"""
Tests for AsyncDifyClient base class.

This module tests the core functionality of the AsyncDifyClient base class including:
- Initialization and configuration
- HTTP request handling (GET, POST, DELETE)
- File upload operations
- Common API endpoints (feedback, parameters, files, audio, meta, info)

Async Testing Pattern:
- All tests are async methods (async def test_*)
- All client method calls use await keyword
- HTTPXMock fixture provided by pytest-httpx for request mocking
- Use httpx_mock.add_response() to configure mock responses
- Use httpx_mock.get_requests() to verify request details
"""

from dify_client.async_client import AsyncDifyClient
from pytest_httpx import HTTPXMock


class TestDifyClientInitialization:
    """Test DifyClient initialization and configuration."""

    async def test_client_initialization_with_defaults(self, mock_api_key: str) -> None:
        """Test that client initializes with default base URL."""
        client = AsyncDifyClient(api_key=mock_api_key)

        assert client.api_key == mock_api_key
        assert client.base_url == "https://api.dify.ai/v1"

    async def test_client_initialization_with_custom_base_url(self, mock_api_key: str, mock_base_url: str) -> None:
        """Test that client initializes with custom base URL."""
        client = AsyncDifyClient(api_key=mock_api_key, base_url=mock_base_url)

        assert client.api_key == mock_api_key
        assert client.base_url == mock_base_url

    async def test_client_stores_api_key_correctly(self, mock_api_key: str) -> None:
        """Test that API key is stored correctly."""
        client = AsyncDifyClient(api_key=mock_api_key)

        assert client.api_key == mock_api_key


class TestDifyClientRequestMethods:
    """Test DifyClient HTTP request methods."""

    async def test_send_request_get_method(
        self,
        httpx_mock: HTTPXMock,
        mock_api_key: str,
        mock_base_url: str,
    ) -> None:
        """Test GET request with query parameters."""
        httpx_mock.add_response(
            url=f"{mock_base_url}/test-endpoint?user=test-user",
            method="GET",
            json={"success": True, "data": {"message": "Operation successful"}},
            status_code=200,
        )

        client = AsyncDifyClient(api_key=mock_api_key, base_url=mock_base_url)
        params = {"user": "test-user"}

        response = await client._send_request("GET", "/test-endpoint", params=params)

        # Verify request was made correctly
        requests = httpx_mock.get_requests()
        assert len(requests) == 1
        assert requests[0].method == "GET"
        assert str(requests[0].url) == f"{mock_base_url}/test-endpoint?user=test-user"
        assert requests[0].headers["Authorization"] == f"Bearer {mock_api_key}"
        assert requests[0].headers["Content-Type"] == "application/json"
        assert response.status_code == 200

    async def test_send_request_post_method(
        self,
        httpx_mock: HTTPXMock,
        mock_api_key: str,
        mock_base_url: str,
    ) -> None:
        """Test POST request with JSON data."""
        httpx_mock.add_response(
            url=f"{mock_base_url}/test-endpoint",
            method="POST",
            json={"success": True, "data": {"message": "Operation successful"}},
            status_code=200,
        )

        client = AsyncDifyClient(api_key=mock_api_key, base_url=mock_base_url)
        data = {"key": "value", "user": "test-user"}

        response = await client._send_request("POST", "/test-endpoint", json=data)

        # Verify request was made correctly
        requests = httpx_mock.get_requests()
        assert len(requests) == 1
        assert requests[0].method == "POST"
        assert str(requests[0].url) == f"{mock_base_url}/test-endpoint"
        assert requests[0].headers["Authorization"] == f"Bearer {mock_api_key}"
        assert requests[0].headers["Content-Type"] == "application/json"
        assert response.status_code == 200

    async def test_send_request_with_streaming(
        self,
        httpx_mock: HTTPXMock,
        mock_api_key: str,
        mock_base_url: str,
    ) -> None:
        """Test request with streaming enabled."""
        stream_content = (
            b'data: {"event": "message", "content": "Hello"}\n'
            b'data: {"event": "message", "content": " World"}\n'
            b'data: {"event": "done"}\n'
        )
        httpx_mock.add_response(
            url=f"{mock_base_url}/test-endpoint",
            method="POST",
            content=stream_content,
            headers={"Content-Type": "text/event-stream"},
            status_code=200,
        )

        client = AsyncDifyClient(api_key=mock_api_key, base_url=mock_base_url)
        data = {"response_mode": "streaming"}

        response = await client._send_request("POST", "/test-endpoint", json=data, stream=True)

        # Verify streaming response
        assert response.status_code == 200
        assert response.headers["Content-Type"] == "text/event-stream"

    async def test_send_request_includes_authorization_header(
        self,
        httpx_mock: HTTPXMock,
        mock_api_key: str,
        mock_base_url: str,
    ) -> None:
        """Test that Authorization header is included in requests."""
        httpx_mock.add_response(
            url=f"{mock_base_url}/test-endpoint",
            method="GET",
            json={"success": True},
            status_code=200,
        )

        client = AsyncDifyClient(api_key=mock_api_key, base_url=mock_base_url)
        await client._send_request("GET", "/test-endpoint")

        # Verify Authorization header
        requests = httpx_mock.get_requests()
        assert len(requests) == 1
        assert "Authorization" in requests[0].headers
        assert requests[0].headers["Authorization"] == f"Bearer {mock_api_key}"

    async def test_send_request_constructs_correct_url(
        self,
        httpx_mock: HTTPXMock,
        mock_api_key: str,
        mock_base_url: str,
    ) -> None:
        """Test that request URL is constructed correctly."""
        endpoint = "/messages/123/feedbacks"
        httpx_mock.add_response(
            url=f"{mock_base_url}{endpoint}",
            method="POST",
            json={"success": True},
            status_code=200,
        )

        client = AsyncDifyClient(api_key=mock_api_key, base_url=mock_base_url)
        await client._send_request("POST", endpoint)

        # Verify URL construction
        requests = httpx_mock.get_requests()
        assert len(requests) == 1
        assert str(requests[0].url) == f"{mock_base_url}{endpoint}"


class TestDifyClientFileUpload:
    """Test DifyClient file upload functionality."""

    async def test_send_request_with_files(
        self,
        httpx_mock: HTTPXMock,
        mock_api_key: str,
        mock_base_url: str,
        sample_files: dict,
    ) -> None:
        """Test file upload request."""
        httpx_mock.add_response(
            url=f"{mock_base_url}/files/upload",
            method="POST",
            json={"success": True, "file_id": "file-12345"},
            status_code=200,
        )

        client = AsyncDifyClient(api_key=mock_api_key, base_url=mock_base_url)
        data = {"user": "test-user"}

        response = await client._send_request_with_files("POST", "/files/upload", data=data, files=sample_files)

        # Verify file upload request
        requests = httpx_mock.get_requests()
        assert len(requests) == 1
        assert requests[0].method == "POST"
        assert str(requests[0].url) == f"{mock_base_url}/files/upload"
        assert requests[0].headers["Authorization"] == f"Bearer {mock_api_key}"
        assert response.status_code == 200

    async def test_send_request_with_files_no_content_type_header(
        self,
        httpx_mock: HTTPXMock,
        mock_api_key: str,
        sample_files: dict,
    ) -> None:
        """Test that Content-Type header is not set for file uploads."""
        httpx_mock.add_response(
            url="https://api.dify.ai/v1/files/upload",
            method="POST",
            json={"success": True},
            status_code=200,
        )

        client = AsyncDifyClient(api_key=mock_api_key)
        await client._send_request_with_files("POST", "/files/upload", data={}, files=sample_files)

        # Verify Content-Type is not in headers (httpx sets it automatically)
        requests = httpx_mock.get_requests()
        assert len(requests) == 1
        content_type = requests[0].headers.get("Content-Type", "")
        assert "Content-Type" not in requests[0].headers or "multipart/form-data" in content_type


class TestDifyClientMessageFeedback:
    """Test message feedback API."""

    async def test_message_feedback_like(
        self,
        httpx_mock: HTTPXMock,
        mock_api_key: str,
        sample_message_id: str,
        mock_user: str,
    ) -> None:
        """Test sending positive feedback for a message."""
        httpx_mock.add_response(
            url=f"https://api.dify.ai/v1/messages/{sample_message_id}/feedbacks",
            method="POST",
            json={"success": True},
            status_code=200,
        )

        client = AsyncDifyClient(api_key=mock_api_key)
        response = await client.message_feedback(message_id=sample_message_id, rating="like", user=mock_user)

        # Verify request
        requests = httpx_mock.get_requests()
        assert len(requests) == 1
        assert requests[0].method == "POST"
        assert f"/messages/{sample_message_id}/feedbacks" in str(requests[0].url)
        assert response.status_code == 200

    async def test_message_feedback_dislike(
        self,
        httpx_mock: HTTPXMock,
        mock_api_key: str,
        sample_message_id: str,
        mock_user: str,
    ) -> None:
        """Test sending negative feedback for a message."""
        httpx_mock.add_response(
            url=f"https://api.dify.ai/v1/messages/{sample_message_id}/feedbacks",
            method="POST",
            json={"success": True},
            status_code=200,
        )

        client = AsyncDifyClient(api_key=mock_api_key)
        response = await client.message_feedback(message_id=sample_message_id, rating="dislike", user=mock_user)

        assert response.status_code == 200


class TestDifyClientApplicationParameters:
    """Test application parameters API."""

    async def test_get_application_parameters(
        self,
        httpx_mock: HTTPXMock,
        mock_api_key: str,
        mock_user: str,
    ) -> None:
        """Test retrieving application parameters."""
        httpx_mock.add_response(
            url=f"https://api.dify.ai/v1/parameters?user={mock_user}",
            method="GET",
            json={"success": True, "data": {"param1": "value1"}},
            status_code=200,
        )

        client = AsyncDifyClient(api_key=mock_api_key)
        response = await client.get_application_parameters(user=mock_user)

        # Verify request
        requests = httpx_mock.get_requests()
        assert len(requests) == 1
        assert requests[0].method == "GET"
        assert "/parameters" in str(requests[0].url)
        assert response.status_code == 200


class TestDifyClientFileUploadAPI:
    """Test file upload API endpoint."""

    async def test_file_upload(
        self,
        httpx_mock: HTTPXMock,
        mock_api_key: str,
        mock_user: str,
        sample_files: dict,
    ) -> None:
        """Test file upload API endpoint."""
        httpx_mock.add_response(
            url="https://api.dify.ai/v1/files/upload",
            method="POST",
            json={"success": True, "file_id": "file-67890"},
            status_code=200,
        )

        client = AsyncDifyClient(api_key=mock_api_key)
        response = await client.file_upload(user=mock_user, files=sample_files)

        # Verify request
        requests = httpx_mock.get_requests()
        assert len(requests) == 1
        assert requests[0].method == "POST"
        assert "/files/upload" in str(requests[0].url)
        assert response.status_code == 200


class TestDifyClientTextToAudio:
    """Test text-to-audio conversion API."""

    async def test_text_to_audio_non_streaming(
        self,
        httpx_mock: HTTPXMock,
        mock_api_key: str,
        mock_user: str,
    ) -> None:
        """Test text-to-audio conversion without streaming."""
        httpx_mock.add_response(
            url="https://api.dify.ai/v1/text-to-audio",
            method="POST",
            json={"success": True, "audio_data": "base64encodedaudio"},
            status_code=200,
        )

        client = AsyncDifyClient(api_key=mock_api_key)
        text = "Hello, this is a test."
        response = await client.text_to_audio(text=text, user=mock_user, streaming=False)

        # Verify request
        requests = httpx_mock.get_requests()
        assert len(requests) == 1
        assert requests[0].method == "POST"
        assert "/text-to-audio" in str(requests[0].url)
        assert response.status_code == 200

    async def test_text_to_audio_streaming(
        self,
        httpx_mock: HTTPXMock,
        mock_api_key: str,
        mock_user: str,
    ) -> None:
        """Test text-to-audio conversion with streaming."""
        httpx_mock.add_response(
            url="https://api.dify.ai/v1/text-to-audio",
            method="POST",
            content=b"audio stream data",
            headers={"Content-Type": "audio/mpeg"},
            status_code=200,
        )

        client = AsyncDifyClient(api_key=mock_api_key)
        text = "Hello, this is a streaming test."
        response = await client.text_to_audio(text=text, user=mock_user, streaming=True)

        assert response.status_code == 200


class TestDifyClientMetaAPI:
    """Test meta information API."""

    async def test_get_meta(
        self,
        httpx_mock: HTTPXMock,
        mock_api_key: str,
        mock_user: str,
    ) -> None:
        """Test retrieving meta information."""
        httpx_mock.add_response(
            url=f"https://api.dify.ai/v1/meta?user={mock_user}",
            method="GET",
            json={"success": True, "meta": {"version": "1.0"}},
            status_code=200,
        )

        client = AsyncDifyClient(api_key=mock_api_key)
        response = await client.get_meta(user=mock_user)

        # Verify request
        requests = httpx_mock.get_requests()
        assert len(requests) == 1
        assert requests[0].method == "GET"
        assert "/meta" in str(requests[0].url)
        assert response.status_code == 200


class TestDifyClientAppInfo:
    """Test application info APIs."""

    async def test_get_app_info(
        self,
        httpx_mock: HTTPXMock,
        mock_api_key: str,
    ) -> None:
        """Test retrieving application information."""
        httpx_mock.add_response(
            url="https://api.dify.ai/v1/info",
            method="GET",
            json={"success": True, "app": {"name": "Test App"}},
            status_code=200,
        )

        client = AsyncDifyClient(api_key=mock_api_key)
        response = await client.get_app_info()

        # Verify request
        requests = httpx_mock.get_requests()
        assert len(requests) == 1
        assert requests[0].method == "GET"
        assert "/info" in str(requests[0].url)
        assert response.status_code == 200

    async def test_get_app_site_info(
        self,
        httpx_mock: HTTPXMock,
        mock_api_key: str,
    ) -> None:
        """Test retrieving application site information."""
        httpx_mock.add_response(
            url="https://api.dify.ai/v1/site",
            method="GET",
            json={"success": True, "site": {"domain": "example.com"}},
            status_code=200,
        )

        client = AsyncDifyClient(api_key=mock_api_key)
        response = await client.get_app_site_info()

        # Verify request
        requests = httpx_mock.get_requests()
        assert len(requests) == 1
        assert requests[0].method == "GET"
        assert "/site" in str(requests[0].url)
        assert response.status_code == 200


class TestDifyClientFilePreview:
    """Test file preview API."""

    async def test_get_file_preview(
        self,
        httpx_mock: HTTPXMock,
        mock_api_key: str,
    ) -> None:
        """Test retrieving file preview."""
        file_id = "file-12345"
        httpx_mock.add_response(
            url=f"https://api.dify.ai/v1/files/{file_id}/preview",
            method="GET",
            json={"success": True, "preview_url": "https://example.com/preview"},
            status_code=200,
        )

        client = AsyncDifyClient(api_key=mock_api_key)
        response = await client.get_file_preview(file_id=file_id)

        # Verify request
        requests = httpx_mock.get_requests()
        assert len(requests) == 1
        assert requests[0].method == "GET"
        assert f"/files/{file_id}/preview" in str(requests[0].url)
        assert response.status_code == 200
