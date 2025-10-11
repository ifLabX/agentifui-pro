"""
Tests for ChatClient.

This module tests the ChatClient functionality including:
- Chat message creation (blocking and streaming)
- Conversation management (list, rename, delete)
- Message operations (get messages, suggestions, stop)
- Audio-to-text conversion
- Annotation management APIs
"""

import json
import re

from dify_client.async_client import AsyncChatClient
from pytest_httpx import HTTPXMock


class TestChatClientInitialization:
    """Test ChatClient initialization."""

    async def test_chat_client_inherits_from_dify_client(self, mock_api_key: str) -> None:
        """Test that ChatClient inherits from DifyClient."""
        client = AsyncChatClient(api_key=mock_api_key)

        assert hasattr(client, "api_key")
        assert hasattr(client, "base_url")
        assert client.api_key == mock_api_key


class TestChatClientCreateMessage:
    """Test chat message creation."""

    async def test_create_chat_message_blocking(
        self,
        httpx_mock: HTTPXMock,
        mock_api_key: str,
        sample_inputs: dict,
        mock_user: str,
    ) -> None:
        """Test creating a chat message in blocking mode."""
        query = "What is AI?"
        httpx_mock.add_response(
            url="https://api.dify.ai/v1/chat-messages",
            method="POST",
            json={"result": "success", "message_id": "msg-123"},
            status_code=200,
        )

        client = AsyncChatClient(api_key=mock_api_key)
        response = await client.create_chat_message(
            inputs=sample_inputs,
            query=query,
            user=mock_user,
            response_mode="blocking",
        )

        # Verify request
        requests = httpx_mock.get_requests()
        assert len(requests) == 1
        request = requests[0]
        assert request.method == "POST"
        assert "/chat-messages" in str(request.url)

        request_body = json.loads(request.content)
        assert request_body["query"] == query
        assert request_body["user"] == mock_user
        assert request_body["response_mode"] == "blocking"
        assert response.status_code == 200

    async def test_create_chat_message_streaming(
        self,
        httpx_mock: HTTPXMock,
        mock_api_key: str,
        sample_inputs: dict,
        mock_user: str,
    ) -> None:
        """Test creating a chat message in streaming mode."""
        query = "Explain quantum computing"
        httpx_mock.add_response(
            url="https://api.dify.ai/v1/chat-messages",
            method="POST",
            text="data: {}\n\n",
            status_code=200,
        )

        client = AsyncChatClient(api_key=mock_api_key)
        response = await client.create_chat_message(
            inputs=sample_inputs,
            query=query,
            user=mock_user,
            response_mode="streaming",
        )

        # Verify request was made
        requests = httpx_mock.get_requests()
        assert len(requests) == 1
        assert response.status_code == 200

    async def test_create_chat_message_with_conversation_id(
        self,
        httpx_mock: HTTPXMock,
        mock_api_key: str,
        sample_inputs: dict,
        sample_conversation_id: str,
        mock_user: str,
    ) -> None:
        """Test creating a chat message with conversation ID."""
        query = "Continue the conversation"
        httpx_mock.add_response(
            url="https://api.dify.ai/v1/chat-messages",
            method="POST",
            json={"result": "success"},
            status_code=200,
        )

        client = AsyncChatClient(api_key=mock_api_key)
        response = await client.create_chat_message(
            inputs=sample_inputs,
            query=query,
            user=mock_user,
            conversation_id=sample_conversation_id,
        )

        # Verify conversation_id is included
        request = httpx_mock.get_request()
        request_body = json.loads(request.content)
        assert request_body["conversation_id"] == sample_conversation_id
        assert response.status_code == 200

    async def test_create_chat_message_with_files(
        self,
        httpx_mock: HTTPXMock,
        mock_api_key: str,
        sample_inputs: dict,
        mock_user: str,
    ) -> None:
        """Test creating a chat message with file attachments."""
        query = "Analyze this file"
        # Files should be file IDs or upload references, not binary data
        files = [{"type": "image", "transfer_method": "remote_url", "url": "https://example.com/image.jpg"}]

        httpx_mock.add_response(
            url="https://api.dify.ai/v1/chat-messages",
            method="POST",
            json={"result": "success"},
            status_code=200,
        )

        client = AsyncChatClient(api_key=mock_api_key)
        response = await client.create_chat_message(
            inputs=sample_inputs,
            query=query,
            user=mock_user,
            files=files,
        )

        # Verify files are included
        request = httpx_mock.get_request()
        request_body = json.loads(request.content)
        assert request_body["files"] == files
        assert response.status_code == 200

    async def test_create_chat_message_default_response_mode(
        self,
        httpx_mock: HTTPXMock,
        mock_api_key: str,
        sample_inputs: dict,
        mock_user: str,
    ) -> None:
        """Test that default response mode is blocking."""
        query = "Test default mode"
        httpx_mock.add_response(
            url="https://api.dify.ai/v1/chat-messages",
            method="POST",
            json={"result": "success"},
            status_code=200,
        )

        client = AsyncChatClient(api_key=mock_api_key)
        await client.create_chat_message(inputs=sample_inputs, query=query, user=mock_user)

        # Verify default is blocking
        request = httpx_mock.get_request()
        request_body = json.loads(request.content)
        assert request_body["response_mode"] == "blocking"


class TestChatClientGetSuggested:
    """Test getting suggested messages."""

    async def test_get_suggested(
        self,
        httpx_mock: HTTPXMock,
        mock_api_key: str,
        sample_message_id: str,
        mock_user: str,
    ) -> None:
        """Test retrieving suggested messages."""
        httpx_mock.add_response(
            url=re.compile(rf"https://api\.dify\.ai/v1/messages/{re.escape(sample_message_id)}/suggested(\?.*)?$"),
            method="GET",
            json={"suggestions": []},
            status_code=200,
        )

        client = AsyncChatClient(api_key=mock_api_key)
        response = await client.get_suggested(message_id=sample_message_id, user=mock_user)

        # Verify request
        requests = httpx_mock.get_requests()
        assert len(requests) == 1
        request = requests[0]
        assert request.method == "GET"
        assert f"/messages/{sample_message_id}/suggested" in str(request.url)
        assert response.status_code == 200


class TestChatClientStopMessage:
    """Test stopping message generation."""

    async def test_stop_message(
        self,
        httpx_mock: HTTPXMock,
        mock_api_key: str,
        sample_task_id: str,
        mock_user: str,
    ) -> None:
        """Test stopping an ongoing message generation."""
        httpx_mock.add_response(
            url=f"https://api.dify.ai/v1/chat-messages/{sample_task_id}/stop",
            method="POST",
            json={"result": "success"},
            status_code=200,
        )

        client = AsyncChatClient(api_key=mock_api_key)
        response = await client.stop_message(task_id=sample_task_id, user=mock_user)

        # Verify request
        requests = httpx_mock.get_requests()
        assert len(requests) == 1
        request = requests[0]
        assert request.method == "POST"
        assert f"/chat-messages/{sample_task_id}/stop" in str(request.url)

        request_body = json.loads(request.content)
        assert request_body == {"user": mock_user}
        assert response.status_code == 200


class TestChatClientGetConversations:
    """Test getting conversations list."""

    async def test_get_conversations_default_params(
        self,
        httpx_mock: HTTPXMock,
        mock_api_key: str,
        mock_user: str,
    ) -> None:
        """Test getting conversations with default parameters."""
        httpx_mock.add_response(
            url=re.compile(r"https://api\.dify\.ai/v1/conversations(\?.*)?$"),
            method="GET",
            json={"conversations": []},
            status_code=200,
        )

        client = AsyncChatClient(api_key=mock_api_key)
        response = await client.get_conversations(user=mock_user)

        # Verify request
        requests = httpx_mock.get_requests()
        assert len(requests) == 1
        request = requests[0]
        assert request.method == "GET"
        assert "/conversations" in str(request.url)
        assert response.status_code == 200

    async def test_get_conversations_with_pagination(
        self,
        httpx_mock: HTTPXMock,
        mock_api_key: str,
        mock_user: str,
    ) -> None:
        """Test getting conversations with pagination."""
        last_id = "conv-last-123"
        limit = 20
        httpx_mock.add_response(
            url=re.compile(r"https://api\.dify\.ai/v1/conversations(\?.*)?$"),
            method="GET",
            json={"conversations": []},
            status_code=200,
        )

        client = AsyncChatClient(api_key=mock_api_key)
        response = await client.get_conversations(user=mock_user, last_id=last_id, limit=limit)

        # Verify pagination params
        request = httpx_mock.get_request()
        assert f"last_id={last_id}" in str(request.url)
        assert f"limit={limit}" in str(request.url)
        assert response.status_code == 200

    async def test_get_conversations_pinned_only(
        self,
        httpx_mock: HTTPXMock,
        mock_api_key: str,
        mock_user: str,
    ) -> None:
        """Test getting only pinned conversations."""
        httpx_mock.add_response(
            url=re.compile(r"https://api\.dify\.ai/v1/conversations(\?.*)?$"),
            method="GET",
            json={"conversations": []},
            status_code=200,
        )

        client = AsyncChatClient(api_key=mock_api_key)
        response = await client.get_conversations(user=mock_user, pinned=True)

        # Verify pinned filter
        request = httpx_mock.get_request()
        assert "pinned=true" in str(request.url)
        assert response.status_code == 200


class TestChatClientGetConversationMessages:
    """Test getting conversation messages."""

    async def test_get_conversation_messages_minimal(
        self,
        httpx_mock: HTTPXMock,
        mock_api_key: str,
        mock_user: str,
    ) -> None:
        """Test getting messages with minimal parameters."""
        httpx_mock.add_response(
            url=re.compile(r"https://api\.dify\.ai/v1/messages(\?.*)?$"),
            method="GET",
            json={"messages": []},
            status_code=200,
        )

        client = AsyncChatClient(api_key=mock_api_key)
        response = await client.get_conversation_messages(user=mock_user)

        # Verify request
        requests = httpx_mock.get_requests()
        assert len(requests) == 1
        request = requests[0]
        assert request.method == "GET"
        assert "/messages" in str(request.url)
        assert response.status_code == 200

    async def test_get_conversation_messages_with_conversation_id(
        self,
        httpx_mock: HTTPXMock,
        mock_api_key: str,
        sample_conversation_id: str,
        mock_user: str,
    ) -> None:
        """Test getting messages for a specific conversation."""
        httpx_mock.add_response(
            url=re.compile(r"https://api\.dify\.ai/v1/messages(\?.*)?$"),
            method="GET",
            json={"messages": []},
            status_code=200,
        )

        client = AsyncChatClient(api_key=mock_api_key)
        response = await client.get_conversation_messages(user=mock_user, conversation_id=sample_conversation_id)

        # Verify conversation_id is included
        request = httpx_mock.get_request()
        assert f"conversation_id={sample_conversation_id}" in str(request.url)
        assert response.status_code == 200

    async def test_get_conversation_messages_with_pagination(
        self,
        httpx_mock: HTTPXMock,
        mock_api_key: str,
        mock_user: str,
    ) -> None:
        """Test getting messages with pagination."""
        first_id = "msg-first-456"
        limit = 50
        httpx_mock.add_response(
            url=re.compile(r"https://api\.dify\.ai/v1/messages(\?.*)?$"),
            method="GET",
            json={"messages": []},
            status_code=200,
        )

        client = AsyncChatClient(api_key=mock_api_key)
        response = await client.get_conversation_messages(user=mock_user, first_id=first_id, limit=limit)

        # Verify pagination params
        request = httpx_mock.get_request()
        assert f"first_id={first_id}" in str(request.url)
        assert f"limit={limit}" in str(request.url)
        assert response.status_code == 200


class TestChatClientRenameConversation:
    """Test renaming conversations."""

    async def test_rename_conversation_manual_name(
        self,
        httpx_mock: HTTPXMock,
        mock_api_key: str,
        sample_conversation_id: str,
        mock_user: str,
    ) -> None:
        """Test renaming a conversation with manual name."""
        new_name = "Important Discussion"
        httpx_mock.add_response(
            url=f"https://api.dify.ai/v1/conversations/{sample_conversation_id}/name",
            method="POST",
            json={"result": "success"},
            status_code=200,
        )

        client = AsyncChatClient(api_key=mock_api_key)
        response = await client.rename_conversation(
            conversation_id=sample_conversation_id,
            name=new_name,
            auto_generate=False,
            user=mock_user,
        )

        # Verify request
        requests = httpx_mock.get_requests()
        assert len(requests) == 1
        request = requests[0]
        assert request.method == "POST"
        assert f"/conversations/{sample_conversation_id}/name" in str(request.url)

        request_body = json.loads(request.content)
        assert request_body["name"] == new_name
        assert request_body["auto_generate"] is False
        assert response.status_code == 200

    async def test_rename_conversation_auto_generate(
        self,
        httpx_mock: HTTPXMock,
        mock_api_key: str,
        sample_conversation_id: str,
        mock_user: str,
    ) -> None:
        """Test renaming a conversation with auto-generated name."""
        httpx_mock.add_response(
            url=f"https://api.dify.ai/v1/conversations/{sample_conversation_id}/name",
            method="POST",
            json={"result": "success"},
            status_code=200,
        )

        client = AsyncChatClient(api_key=mock_api_key)
        response = await client.rename_conversation(
            conversation_id=sample_conversation_id,
            name="",
            auto_generate=True,
            user=mock_user,
        )

        # Verify auto_generate is True
        request = httpx_mock.get_request()
        request_body = json.loads(request.content)
        assert request_body["auto_generate"] is True
        assert response.status_code == 200


class TestChatClientDeleteConversation:
    """Test deleting conversations."""

    async def test_delete_conversation(
        self,
        httpx_mock: HTTPXMock,
        mock_api_key: str,
        sample_conversation_id: str,
        mock_user: str,
    ) -> None:
        """Test deleting a conversation."""
        httpx_mock.add_response(
            url=f"https://api.dify.ai/v1/conversations/{sample_conversation_id}",
            method="DELETE",
            json={"result": "success"},
            status_code=200,
        )

        client = AsyncChatClient(api_key=mock_api_key)
        response = await client.delete_conversation(conversation_id=sample_conversation_id, user=mock_user)

        # Verify request
        requests = httpx_mock.get_requests()
        assert len(requests) == 1
        request = requests[0]
        assert request.method == "DELETE"
        assert f"/conversations/{sample_conversation_id}" in str(request.url)

        request_body = json.loads(request.content)
        assert request_body == {"user": mock_user}
        assert response.status_code == 200


class TestChatClientAudioToText:
    """Test audio-to-text conversion."""

    async def test_audio_to_text_with_tuple(
        self,
        httpx_mock: HTTPXMock,
        mock_api_key: str,
        mock_user: str,
    ) -> None:
        """Test converting audio to text with file tuple."""
        httpx_mock.add_response(
            url="https://api.dify.ai/v1/audio-to-text",
            method="POST",
            json={"text": "transcribed text"},
            status_code=200,
        )

        client = AsyncChatClient(api_key=mock_api_key)
        audio_file = ("audio.mp3", b"audio content", "audio/mpeg")
        response = await client.audio_to_text(audio_file=audio_file, user=mock_user)

        # Verify request
        requests = httpx_mock.get_requests()
        assert len(requests) == 1
        request = requests[0]
        assert request.method == "POST"
        assert "/audio-to-text" in str(request.url)
        assert response.status_code == 200


class TestChatClientAnnotationAPIs:
    """Test annotation management APIs."""

    async def test_annotation_reply_action_enable(
        self,
        httpx_mock: HTTPXMock,
        mock_api_key: str,
    ) -> None:
        """Test enabling annotation reply feature."""
        httpx_mock.add_response(
            url="https://api.dify.ai/v1/apps/annotation-reply/enable",
            method="POST",
            json={"job_id": "job-123"},
            status_code=200,
        )

        client = AsyncChatClient(api_key=mock_api_key)
        response = await client.annotation_reply_action(
            action="enable",
            score_threshold=0.8,
            embedding_provider_name="openai",
            embedding_model_name="text-embedding-ada-002",
        )

        # Verify request
        requests = httpx_mock.get_requests()
        assert len(requests) == 1
        request = requests[0]
        assert request.method == "POST"
        assert "/apps/annotation-reply/enable" in str(request.url)

        request_body = json.loads(request.content)
        assert request_body["score_threshold"] == 0.8
        assert request_body["embedding_provider_name"] == "openai"
        assert response.status_code == 200

    async def test_annotation_reply_action_disable(
        self,
        httpx_mock: HTTPXMock,
        mock_api_key: str,
    ) -> None:
        """Test disabling annotation reply feature."""
        httpx_mock.add_response(
            url="https://api.dify.ai/v1/apps/annotation-reply/disable",
            method="POST",
            json={"result": "success"},
            status_code=200,
        )

        client = AsyncChatClient(api_key=mock_api_key)
        response = await client.annotation_reply_action(
            action="disable",
            score_threshold=0.5,
            embedding_provider_name="test",
            embedding_model_name="test-model",
        )

        # Verify disable action
        request = httpx_mock.get_request()
        assert "/apps/annotation-reply/disable" in str(request.url)
        assert response.status_code == 200

    async def test_annotation_reply_action_with_none_values(
        self, httpx_mock: HTTPXMock, mock_api_key: str
    ) -> None:
        """Test that annotation reply action handles None values (validation deferred to API)."""
        # Mock the API response - it will handle validation server-side
        httpx_mock.add_response(
            url="https://api.dify.ai/v1/apps/annotation-reply/enable",
            method="POST",
            json={"error": "score_threshold is required"},
            status_code=400,
        )

        client = AsyncChatClient(api_key=mock_api_key)
        response = await client.annotation_reply_action(
            action="enable",
            score_threshold=None,  # type: ignore[arg-type]
            embedding_provider_name="openai",
            embedding_model_name="test",
        )

        # The client passes None to API, which returns validation error
        assert response.status_code == 400

    async def test_get_annotation_reply_status(
        self,
        httpx_mock: HTTPXMock,
        mock_api_key: str,
    ) -> None:
        """Test getting annotation reply action status."""
        job_id = "job-123-abc"
        httpx_mock.add_response(
            url=f"https://api.dify.ai/v1/apps/annotation-reply/enable/status/{job_id}",
            method="GET",
            json={"status": "completed"},
            status_code=200,
        )

        client = AsyncChatClient(api_key=mock_api_key)
        response = await client.get_annotation_reply_status(action="enable", job_id=job_id)

        # Verify request
        requests = httpx_mock.get_requests()
        assert len(requests) == 1
        request = requests[0]
        assert request.method == "GET"
        assert f"/apps/annotation-reply/enable/status/{job_id}" in str(request.url)
        assert response.status_code == 200

    async def test_list_annotations_default(
        self,
        httpx_mock: HTTPXMock,
        mock_api_key: str,
    ) -> None:
        """Test listing annotations with default parameters."""
        httpx_mock.add_response(
            url=re.compile(r"https://api\.dify\.ai/v1/apps/annotations(\?.*)?$"),
            method="GET",
            json={"annotations": []},
            status_code=200,
        )

        client = AsyncChatClient(api_key=mock_api_key)
        response = await client.list_annotations()

        # Verify request
        request = httpx_mock.get_request()
        assert "page=1" in str(request.url)
        assert "limit=20" in str(request.url)
        assert response.status_code == 200

    async def test_list_annotations_with_pagination_and_keyword(
        self,
        httpx_mock: HTTPXMock,
        mock_api_key: str,
    ) -> None:
        """Test listing annotations with pagination and keyword."""
        httpx_mock.add_response(
            url=re.compile(r"https://api\.dify\.ai/v1/apps/annotations(\?.*)?$"),
            method="GET",
            json={"annotations": []},
            status_code=200,
        )

        client = AsyncChatClient(api_key=mock_api_key)
        response = await client.list_annotations(page=2, limit=50, keyword="test query")

        # Verify parameters
        request = httpx_mock.get_request()
        assert "page=2" in str(request.url)
        assert "limit=50" in str(request.url)
        assert "keyword=" in str(request.url)
        assert response.status_code == 200

    async def test_create_annotation(
        self,
        httpx_mock: HTTPXMock,
        mock_api_key: str,
        sample_annotation_data: dict,
    ) -> None:
        """Test creating a new annotation."""
        httpx_mock.add_response(
            url="https://api.dify.ai/v1/apps/annotations",
            method="POST",
            json={"id": "annotation-123"},
            status_code=200,
        )

        client = AsyncChatClient(api_key=mock_api_key)
        response = await client.create_annotation(
            question=sample_annotation_data["question"],
            answer=sample_annotation_data["answer"],
        )

        # Verify request
        requests = httpx_mock.get_requests()
        assert len(requests) == 1
        request = requests[0]
        assert request.method == "POST"
        assert "/apps/annotations" in str(request.url)

        request_body = json.loads(request.content)
        assert request_body["question"] == sample_annotation_data["question"]
        assert request_body["answer"] == sample_annotation_data["answer"]
        assert response.status_code == 200

    async def test_update_annotation(
        self,
        httpx_mock: HTTPXMock,
        mock_api_key: str,
        sample_annotation_data: dict,
    ) -> None:
        """Test updating an existing annotation."""
        annotation_id = "annotation-789"
        httpx_mock.add_response(
            url=f"https://api.dify.ai/v1/apps/annotations/{annotation_id}",
            method="PUT",
            json={"result": "success"},
            status_code=200,
        )

        client = AsyncChatClient(api_key=mock_api_key)
        response = await client.update_annotation(
            annotation_id=annotation_id,
            question="Updated question?",
            answer="Updated answer",
        )

        # Verify request
        requests = httpx_mock.get_requests()
        assert len(requests) == 1
        request = requests[0]
        assert request.method == "PUT"
        assert f"/apps/annotations/{annotation_id}" in str(request.url)

        request_body = json.loads(request.content)
        assert request_body["question"] == "Updated question?"
        assert response.status_code == 200

    async def test_delete_annotation(
        self,
        httpx_mock: HTTPXMock,
        mock_api_key: str,
    ) -> None:
        """Test deleting an annotation."""
        annotation_id = "annotation-999"
        httpx_mock.add_response(
            url=f"https://api.dify.ai/v1/apps/annotations/{annotation_id}",
            method="DELETE",
            json={"result": "success"},
            status_code=200,
        )

        client = AsyncChatClient(api_key=mock_api_key)
        response = await client.delete_annotation(annotation_id=annotation_id)

        # Verify request
        requests = httpx_mock.get_requests()
        assert len(requests) == 1
        request = requests[0]
        assert request.method == "DELETE"
        assert f"/apps/annotations/{annotation_id}" in str(request.url)
        assert response.status_code == 200
