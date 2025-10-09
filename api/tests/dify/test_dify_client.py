"""
Tests for DifyClient base class.

This module tests the core functionality of the DifyClient base class including:
- Initialization and configuration
- HTTP request handling (GET, POST, DELETE)
- File upload operations
- Common API endpoints (feedback, parameters, files, audio, meta, info)
"""

from unittest.mock import Mock

from dify_client import DifyClient


class TestDifyClientInitialization:
    """Test DifyClient initialization and configuration."""

    def test_client_initialization_with_defaults(self, mock_api_key: str) -> None:
        """Test that client initializes with default base URL."""
        client = DifyClient(api_key=mock_api_key)

        assert client.api_key == mock_api_key
        assert client.base_url == "https://api.dify.ai/v1"

    def test_client_initialization_with_custom_base_url(
        self, mock_api_key: str, mock_base_url: str
    ) -> None:
        """Test that client initializes with custom base URL."""
        client = DifyClient(api_key=mock_api_key, base_url=mock_base_url)

        assert client.api_key == mock_api_key
        assert client.base_url == mock_base_url

    def test_client_stores_api_key_correctly(self, mock_api_key: str) -> None:
        """Test that API key is stored correctly."""
        client = DifyClient(api_key=mock_api_key)

        assert client.api_key == mock_api_key


class TestDifyClientRequestMethods:
    """Test DifyClient HTTP request methods."""

    def test_send_request_get_method(
        self,
        mock_api_key: str,
        mock_base_url: str,
        mock_requests_request: Mock,
        mock_successful_response: Mock,
    ) -> None:
        """Test GET request with query parameters."""
        mock_requests_request.return_value = mock_successful_response

        client = DifyClient(api_key=mock_api_key, base_url=mock_base_url)
        params = {"user": "test-user"}

        response = client._send_request("GET", "/test-endpoint", params=params)

        # Verify request was made correctly
        mock_requests_request.assert_called_once_with(
            "GET",
            f"{mock_base_url}/test-endpoint",
            json=None,
            params=params,
            headers={
                "Authorization": f"Bearer {mock_api_key}",
                "Content-Type": "application/json",
            },
            stream=False,
        )
        assert response == mock_successful_response

    def test_send_request_post_method(
        self,
        mock_api_key: str,
        mock_base_url: str,
        mock_requests_request: Mock,
        mock_successful_response: Mock,
    ) -> None:
        """Test POST request with JSON data."""
        mock_requests_request.return_value = mock_successful_response

        client = DifyClient(api_key=mock_api_key, base_url=mock_base_url)
        data = {"key": "value", "user": "test-user"}

        response = client._send_request("POST", "/test-endpoint", json=data)

        # Verify request was made correctly
        mock_requests_request.assert_called_once_with(
            "POST",
            f"{mock_base_url}/test-endpoint",
            json=data,
            params=None,
            headers={
                "Authorization": f"Bearer {mock_api_key}",
                "Content-Type": "application/json",
            },
            stream=False,
        )
        assert response == mock_successful_response

    def test_send_request_with_streaming(
        self,
        mock_api_key: str,
        mock_base_url: str,
        mock_requests_request: Mock,
        mock_streaming_response: Mock,
    ) -> None:
        """Test request with streaming enabled."""
        mock_requests_request.return_value = mock_streaming_response

        client = DifyClient(api_key=mock_api_key, base_url=mock_base_url)
        data = {"response_mode": "streaming"}

        response = client._send_request("POST", "/test-endpoint", json=data, stream=True)

        # Verify streaming was enabled
        mock_requests_request.assert_called_once()
        call_kwargs = mock_requests_request.call_args[1]
        assert call_kwargs["stream"] is True
        assert response == mock_streaming_response

    def test_send_request_includes_authorization_header(
        self,
        mock_api_key: str,
        mock_base_url: str,
        mock_requests_request: Mock,
        mock_successful_response: Mock,
    ) -> None:
        """Test that Authorization header is included in requests."""
        mock_requests_request.return_value = mock_successful_response

        client = DifyClient(api_key=mock_api_key, base_url=mock_base_url)
        client._send_request("GET", "/test-endpoint")

        # Verify Authorization header
        call_kwargs = mock_requests_request.call_args[1]
        assert "Authorization" in call_kwargs["headers"]
        assert call_kwargs["headers"]["Authorization"] == f"Bearer {mock_api_key}"

    def test_send_request_constructs_correct_url(
        self,
        mock_api_key: str,
        mock_base_url: str,
        mock_requests_request: Mock,
        mock_successful_response: Mock,
    ) -> None:
        """Test that request URL is constructed correctly."""
        mock_requests_request.return_value = mock_successful_response

        client = DifyClient(api_key=mock_api_key, base_url=mock_base_url)
        endpoint = "/messages/123/feedbacks"

        client._send_request("POST", endpoint)

        # Verify URL construction
        call_args = mock_requests_request.call_args[0]
        assert call_args[1] == f"{mock_base_url}{endpoint}"


class TestDifyClientFileUpload:
    """Test DifyClient file upload functionality."""

    def test_send_request_with_files(
        self,
        mock_api_key: str,
        mock_base_url: str,
        mock_requests_request: Mock,
        mock_successful_response: Mock,
        sample_files: dict,
    ) -> None:
        """Test file upload request."""
        mock_requests_request.return_value = mock_successful_response

        client = DifyClient(api_key=mock_api_key, base_url=mock_base_url)
        data = {"user": "test-user"}

        response = client._send_request_with_files(
            "POST", "/files/upload", data=data, files=sample_files
        )

        # Verify file upload request
        mock_requests_request.assert_called_once_with(
            "POST",
            f"{mock_base_url}/files/upload",
            data=data,
            headers={"Authorization": f"Bearer {mock_api_key}"},
            files=sample_files,
        )
        assert response == mock_successful_response

    def test_send_request_with_files_no_content_type_header(
        self,
        mock_api_key: str,
        mock_requests_request: Mock,
        mock_successful_response: Mock,
        sample_files: dict,
    ) -> None:
        """Test that Content-Type header is not set for file uploads."""
        mock_requests_request.return_value = mock_successful_response

        client = DifyClient(api_key=mock_api_key)
        client._send_request_with_files("POST", "/files/upload", data={}, files=sample_files)

        # Verify Content-Type is not in headers (let requests set it)
        call_kwargs = mock_requests_request.call_args[1]
        assert "Content-Type" not in call_kwargs["headers"]


class TestDifyClientMessageFeedback:
    """Test message feedback API."""

    def test_message_feedback_like(
        self,
        mock_api_key: str,
        mock_requests_request: Mock,
        mock_successful_response: Mock,
        sample_message_id: str,
        mock_user: str,
    ) -> None:
        """Test sending positive feedback for a message."""
        mock_requests_request.return_value = mock_successful_response

        client = DifyClient(api_key=mock_api_key)
        response = client.message_feedback(
            message_id=sample_message_id, rating="like", user=mock_user
        )

        # Verify request
        mock_requests_request.assert_called_once()
        call_args, call_kwargs = mock_requests_request.call_args
        assert call_args[0] == "POST"
        assert f"/messages/{sample_message_id}/feedbacks" in call_args[1]
        assert response == mock_successful_response

    def test_message_feedback_dislike(
        self,
        mock_api_key: str,
        mock_requests_request: Mock,
        mock_successful_response: Mock,
        sample_message_id: str,
        mock_user: str,
    ) -> None:
        """Test sending negative feedback for a message."""
        mock_requests_request.return_value = mock_successful_response

        client = DifyClient(api_key=mock_api_key)
        response = client.message_feedback(
            message_id=sample_message_id, rating="dislike", user=mock_user
        )

        assert response == mock_successful_response


class TestDifyClientApplicationParameters:
    """Test application parameters API."""

    def test_get_application_parameters(
        self,
        mock_api_key: str,
        mock_requests_request: Mock,
        mock_successful_response: Mock,
        mock_user: str,
    ) -> None:
        """Test retrieving application parameters."""
        mock_requests_request.return_value = mock_successful_response

        client = DifyClient(api_key=mock_api_key)
        response = client.get_application_parameters(user=mock_user)

        # Verify request
        mock_requests_request.assert_called_once()
        call_args, call_kwargs = mock_requests_request.call_args
        assert call_args[0] == "GET"
        assert "/parameters" in call_args[1]
        assert call_kwargs["params"] == {"user": mock_user}
        assert response == mock_successful_response


class TestDifyClientFileUploadAPI:
    """Test file upload API endpoint."""

    def test_file_upload(
        self,
        mock_api_key: str,
        mock_requests_request: Mock,
        mock_successful_response: Mock,
        mock_user: str,
        sample_files: dict,
    ) -> None:
        """Test file upload API endpoint."""
        mock_requests_request.return_value = mock_successful_response

        client = DifyClient(api_key=mock_api_key)
        response = client.file_upload(user=mock_user, files=sample_files)

        # Verify request
        mock_requests_request.assert_called_once()
        call_args, call_kwargs = mock_requests_request.call_args
        assert call_args[0] == "POST"
        assert "/files/upload" in call_args[1]
        assert call_kwargs["data"] == {"user": mock_user}
        assert call_kwargs["files"] == sample_files
        assert response == mock_successful_response


class TestDifyClientTextToAudio:
    """Test text-to-audio conversion API."""

    def test_text_to_audio_non_streaming(
        self,
        mock_api_key: str,
        mock_requests_request: Mock,
        mock_successful_response: Mock,
        mock_user: str,
    ) -> None:
        """Test text-to-audio conversion without streaming."""
        mock_requests_request.return_value = mock_successful_response

        client = DifyClient(api_key=mock_api_key)
        text = "Hello, this is a test."
        response = client.text_to_audio(text=text, user=mock_user, streaming=False)

        # Verify request
        mock_requests_request.assert_called_once()
        call_args, call_kwargs = mock_requests_request.call_args
        assert call_args[0] == "POST"
        assert "/text-to-audio" in call_args[1]
        assert call_kwargs["json"]["text"] == text
        assert call_kwargs["json"]["user"] == mock_user
        assert call_kwargs["json"]["streaming"] is False
        assert response == mock_successful_response

    def test_text_to_audio_streaming(
        self,
        mock_api_key: str,
        mock_requests_request: Mock,
        mock_streaming_response: Mock,
        mock_user: str,
    ) -> None:
        """Test text-to-audio conversion with streaming."""
        mock_requests_request.return_value = mock_streaming_response

        client = DifyClient(api_key=mock_api_key)
        text = "Hello, this is a streaming test."
        response = client.text_to_audio(text=text, user=mock_user, streaming=True)

        assert response == mock_streaming_response


class TestDifyClientMetaAPI:
    """Test meta information API."""

    def test_get_meta(
        self,
        mock_api_key: str,
        mock_requests_request: Mock,
        mock_successful_response: Mock,
        mock_user: str,
    ) -> None:
        """Test retrieving meta information."""
        mock_requests_request.return_value = mock_successful_response

        client = DifyClient(api_key=mock_api_key)
        response = client.get_meta(user=mock_user)

        # Verify request
        mock_requests_request.assert_called_once()
        call_args, call_kwargs = mock_requests_request.call_args
        assert call_args[0] == "GET"
        assert "/meta" in call_args[1]
        assert call_kwargs["params"] == {"user": mock_user}
        assert response == mock_successful_response


class TestDifyClientAppInfo:
    """Test application info APIs."""

    def test_get_app_info(
        self,
        mock_api_key: str,
        mock_requests_request: Mock,
        mock_successful_response: Mock,
    ) -> None:
        """Test retrieving application information."""
        mock_requests_request.return_value = mock_successful_response

        client = DifyClient(api_key=mock_api_key)
        response = client.get_app_info()

        # Verify request
        mock_requests_request.assert_called_once()
        call_args = mock_requests_request.call_args[0]
        assert call_args[0] == "GET"
        assert "/info" in call_args[1]
        assert response == mock_successful_response

    def test_get_app_site_info(
        self,
        mock_api_key: str,
        mock_requests_request: Mock,
        mock_successful_response: Mock,
    ) -> None:
        """Test retrieving application site information."""
        mock_requests_request.return_value = mock_successful_response

        client = DifyClient(api_key=mock_api_key)
        response = client.get_app_site_info()

        # Verify request
        mock_requests_request.assert_called_once()
        call_args = mock_requests_request.call_args[0]
        assert call_args[0] == "GET"
        assert "/site" in call_args[1]
        assert response == mock_successful_response


class TestDifyClientFilePreview:
    """Test file preview API."""

    def test_get_file_preview(
        self,
        mock_api_key: str,
        mock_requests_request: Mock,
        mock_successful_response: Mock,
    ) -> None:
        """Test retrieving file preview."""
        mock_requests_request.return_value = mock_successful_response

        client = DifyClient(api_key=mock_api_key)
        file_id = "file-12345"
        response = client.get_file_preview(file_id=file_id)

        # Verify request
        mock_requests_request.assert_called_once()
        call_args = mock_requests_request.call_args[0]
        assert call_args[0] == "GET"
        assert f"/files/{file_id}/preview" in call_args[1]
        assert response == mock_successful_response
