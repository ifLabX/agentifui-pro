"""
Tests for ChatClient.

This module tests the ChatClient functionality including:
- Chat message creation (blocking and streaming)
- Conversation management (list, rename, delete)
- Message operations (get messages, suggestions, stop)
- Audio-to-text conversion
- Annotation management APIs
"""

from unittest.mock import Mock

import pytest
from dify_client import ChatClient


class TestChatClientInitialization:
    """Test ChatClient initialization."""

    def test_chat_client_inherits_from_dify_client(self, mock_api_key: str) -> None:
        """Test that ChatClient inherits from DifyClient."""
        client = ChatClient(api_key=mock_api_key)

        assert hasattr(client, "api_key")
        assert hasattr(client, "base_url")
        assert client.api_key == mock_api_key


class TestChatClientCreateMessage:
    """Test chat message creation."""

    def test_create_chat_message_blocking(
        self,
        mock_api_key: str,
        mock_requests_request: Mock,
        mock_successful_response: Mock,
        sample_inputs: dict,
        mock_user: str,
    ) -> None:
        """Test creating a chat message in blocking mode."""
        mock_requests_request.return_value = mock_successful_response

        client = ChatClient(api_key=mock_api_key)
        query = "What is AI?"
        response = client.create_chat_message(
            inputs=sample_inputs,
            query=query,
            user=mock_user,
            response_mode="blocking",
        )

        # Verify request
        mock_requests_request.assert_called_once()
        call_args, call_kwargs = mock_requests_request.call_args
        assert call_args[0] == "POST"
        assert "/chat-messages" in call_args[1]
        assert call_kwargs["json"]["query"] == query
        assert call_kwargs["json"]["user"] == mock_user
        assert call_kwargs["json"]["response_mode"] == "blocking"
        assert call_kwargs["stream"] is False
        assert response == mock_successful_response

    def test_create_chat_message_streaming(
        self,
        mock_api_key: str,
        mock_requests_request: Mock,
        mock_streaming_response: Mock,
        sample_inputs: dict,
        mock_user: str,
    ) -> None:
        """Test creating a chat message in streaming mode."""
        mock_requests_request.return_value = mock_streaming_response

        client = ChatClient(api_key=mock_api_key)
        query = "Explain quantum computing"
        response = client.create_chat_message(
            inputs=sample_inputs,
            query=query,
            user=mock_user,
            response_mode="streaming",
        )

        # Verify streaming is enabled
        call_kwargs = mock_requests_request.call_args[1]
        assert call_kwargs["stream"] is True
        assert response == mock_streaming_response

    def test_create_chat_message_with_conversation_id(
        self,
        mock_api_key: str,
        mock_requests_request: Mock,
        mock_successful_response: Mock,
        sample_inputs: dict,
        sample_conversation_id: str,
        mock_user: str,
    ) -> None:
        """Test creating a chat message with conversation ID."""
        mock_requests_request.return_value = mock_successful_response

        client = ChatClient(api_key=mock_api_key)
        query = "Continue the conversation"
        response = client.create_chat_message(
            inputs=sample_inputs,
            query=query,
            user=mock_user,
            conversation_id=sample_conversation_id,
        )

        # Verify conversation_id is included
        call_kwargs = mock_requests_request.call_args[1]
        assert call_kwargs["json"]["conversation_id"] == sample_conversation_id
        assert response == mock_successful_response

    def test_create_chat_message_with_files(
        self,
        mock_api_key: str,
        mock_requests_request: Mock,
        mock_successful_response: Mock,
        sample_inputs: dict,
        sample_files: dict,
        mock_user: str,
    ) -> None:
        """Test creating a chat message with file attachments."""
        mock_requests_request.return_value = mock_successful_response

        client = ChatClient(api_key=mock_api_key)
        query = "Analyze this file"
        response = client.create_chat_message(
            inputs=sample_inputs,
            query=query,
            user=mock_user,
            files=sample_files,
        )

        # Verify files are included
        call_kwargs = mock_requests_request.call_args[1]
        assert call_kwargs["json"]["files"] == sample_files
        assert response == mock_successful_response

    def test_create_chat_message_default_response_mode(
        self,
        mock_api_key: str,
        mock_requests_request: Mock,
        mock_successful_response: Mock,
        sample_inputs: dict,
        mock_user: str,
    ) -> None:
        """Test that default response mode is blocking."""
        mock_requests_request.return_value = mock_successful_response

        client = ChatClient(api_key=mock_api_key)
        query = "Test default mode"
        client.create_chat_message(inputs=sample_inputs, query=query, user=mock_user)

        # Verify default is blocking
        call_kwargs = mock_requests_request.call_args[1]
        assert call_kwargs["json"]["response_mode"] == "blocking"
        assert call_kwargs["stream"] is False


class TestChatClientGetSuggested:
    """Test getting suggested messages."""

    def test_get_suggested(
        self,
        mock_api_key: str,
        mock_requests_request: Mock,
        mock_successful_response: Mock,
        sample_message_id: str,
        mock_user: str,
    ) -> None:
        """Test retrieving suggested messages."""
        mock_requests_request.return_value = mock_successful_response

        client = ChatClient(api_key=mock_api_key)
        response = client.get_suggested(message_id=sample_message_id, user=mock_user)

        # Verify request
        mock_requests_request.assert_called_once()
        call_args, call_kwargs = mock_requests_request.call_args
        assert call_args[0] == "GET"
        assert f"/messages/{sample_message_id}/suggested" in call_args[1]
        assert call_kwargs["params"] == {"user": mock_user}
        assert response == mock_successful_response


class TestChatClientStopMessage:
    """Test stopping message generation."""

    def test_stop_message(
        self,
        mock_api_key: str,
        mock_requests_request: Mock,
        mock_successful_response: Mock,
        sample_task_id: str,
        mock_user: str,
    ) -> None:
        """Test stopping an ongoing message generation."""
        mock_requests_request.return_value = mock_successful_response

        client = ChatClient(api_key=mock_api_key)
        response = client.stop_message(task_id=sample_task_id, user=mock_user)

        # Verify request
        mock_requests_request.assert_called_once()
        call_args, call_kwargs = mock_requests_request.call_args
        assert call_args[0] == "POST"
        assert f"/chat-messages/{sample_task_id}/stop" in call_args[1]
        assert call_kwargs["json"] == {"user": mock_user}
        assert response == mock_successful_response


class TestChatClientGetConversations:
    """Test getting conversations list."""

    def test_get_conversations_default_params(
        self,
        mock_api_key: str,
        mock_requests_request: Mock,
        mock_successful_response: Mock,
        mock_user: str,
    ) -> None:
        """Test getting conversations with default parameters."""
        mock_requests_request.return_value = mock_successful_response

        client = ChatClient(api_key=mock_api_key)
        response = client.get_conversations(user=mock_user)

        # Verify request
        mock_requests_request.assert_called_once()
        call_args, call_kwargs = mock_requests_request.call_args
        assert call_args[0] == "GET"
        assert "/conversations" in call_args[1]
        assert call_kwargs["params"]["user"] == mock_user
        assert response == mock_successful_response

    def test_get_conversations_with_pagination(
        self,
        mock_api_key: str,
        mock_requests_request: Mock,
        mock_successful_response: Mock,
        mock_user: str,
    ) -> None:
        """Test getting conversations with pagination."""
        mock_requests_request.return_value = mock_successful_response

        client = ChatClient(api_key=mock_api_key)
        last_id = "conv-last-123"
        limit = 20
        response = client.get_conversations(user=mock_user, last_id=last_id, limit=limit)

        # Verify pagination params
        call_kwargs = mock_requests_request.call_args[1]
        assert call_kwargs["params"]["last_id"] == last_id
        assert call_kwargs["params"]["limit"] == limit
        assert response == mock_successful_response

    def test_get_conversations_pinned_only(
        self,
        mock_api_key: str,
        mock_requests_request: Mock,
        mock_successful_response: Mock,
        mock_user: str,
    ) -> None:
        """Test getting only pinned conversations."""
        mock_requests_request.return_value = mock_successful_response

        client = ChatClient(api_key=mock_api_key)
        response = client.get_conversations(user=mock_user, pinned=True)

        # Verify pinned filter
        call_kwargs = mock_requests_request.call_args[1]
        assert call_kwargs["params"]["pinned"] is True
        assert response == mock_successful_response


class TestChatClientGetConversationMessages:
    """Test getting conversation messages."""

    def test_get_conversation_messages_minimal(
        self,
        mock_api_key: str,
        mock_requests_request: Mock,
        mock_successful_response: Mock,
        mock_user: str,
    ) -> None:
        """Test getting messages with minimal parameters."""
        mock_requests_request.return_value = mock_successful_response

        client = ChatClient(api_key=mock_api_key)
        response = client.get_conversation_messages(user=mock_user)

        # Verify request
        mock_requests_request.assert_called_once()
        call_args, call_kwargs = mock_requests_request.call_args
        assert call_args[0] == "GET"
        assert "/messages" in call_args[1]
        assert call_kwargs["params"] == {"user": mock_user}
        assert response == mock_successful_response

    def test_get_conversation_messages_with_conversation_id(
        self,
        mock_api_key: str,
        mock_requests_request: Mock,
        mock_successful_response: Mock,
        sample_conversation_id: str,
        mock_user: str,
    ) -> None:
        """Test getting messages for a specific conversation."""
        mock_requests_request.return_value = mock_successful_response

        client = ChatClient(api_key=mock_api_key)
        response = client.get_conversation_messages(
            user=mock_user, conversation_id=sample_conversation_id
        )

        # Verify conversation_id is included
        call_kwargs = mock_requests_request.call_args[1]
        assert call_kwargs["params"]["conversation_id"] == sample_conversation_id
        assert response == mock_successful_response

    def test_get_conversation_messages_with_pagination(
        self,
        mock_api_key: str,
        mock_requests_request: Mock,
        mock_successful_response: Mock,
        mock_user: str,
    ) -> None:
        """Test getting messages with pagination."""
        mock_requests_request.return_value = mock_successful_response

        client = ChatClient(api_key=mock_api_key)
        first_id = "msg-first-456"
        limit = 50
        response = client.get_conversation_messages(
            user=mock_user, first_id=first_id, limit=limit
        )

        # Verify pagination params
        call_kwargs = mock_requests_request.call_args[1]
        assert call_kwargs["params"]["first_id"] == first_id
        assert call_kwargs["params"]["limit"] == limit
        assert response == mock_successful_response


class TestChatClientRenameConversation:
    """Test renaming conversations."""

    def test_rename_conversation_manual_name(
        self,
        mock_api_key: str,
        mock_requests_request: Mock,
        mock_successful_response: Mock,
        sample_conversation_id: str,
        mock_user: str,
    ) -> None:
        """Test renaming a conversation with manual name."""
        mock_requests_request.return_value = mock_successful_response

        client = ChatClient(api_key=mock_api_key)
        new_name = "Important Discussion"
        response = client.rename_conversation(
            conversation_id=sample_conversation_id,
            name=new_name,
            auto_generate=False,
            user=mock_user,
        )

        # Verify request
        mock_requests_request.assert_called_once()
        call_args, call_kwargs = mock_requests_request.call_args
        assert call_args[0] == "POST"
        assert f"/conversations/{sample_conversation_id}/name" in call_args[1]
        assert call_kwargs["json"]["name"] == new_name
        assert call_kwargs["json"]["auto_generate"] is False
        assert response == mock_successful_response

    def test_rename_conversation_auto_generate(
        self,
        mock_api_key: str,
        mock_requests_request: Mock,
        mock_successful_response: Mock,
        sample_conversation_id: str,
        mock_user: str,
    ) -> None:
        """Test renaming a conversation with auto-generated name."""
        mock_requests_request.return_value = mock_successful_response

        client = ChatClient(api_key=mock_api_key)
        response = client.rename_conversation(
            conversation_id=sample_conversation_id,
            name="",
            auto_generate=True,
            user=mock_user,
        )

        # Verify auto_generate is True
        call_kwargs = mock_requests_request.call_args[1]
        assert call_kwargs["json"]["auto_generate"] is True
        assert response == mock_successful_response


class TestChatClientDeleteConversation:
    """Test deleting conversations."""

    def test_delete_conversation(
        self,
        mock_api_key: str,
        mock_requests_request: Mock,
        mock_successful_response: Mock,
        sample_conversation_id: str,
        mock_user: str,
    ) -> None:
        """Test deleting a conversation."""
        mock_requests_request.return_value = mock_successful_response

        client = ChatClient(api_key=mock_api_key)
        response = client.delete_conversation(
            conversation_id=sample_conversation_id, user=mock_user
        )

        # Verify request
        mock_requests_request.assert_called_once()
        call_args, call_kwargs = mock_requests_request.call_args
        assert call_args[0] == "DELETE"
        assert f"/conversations/{sample_conversation_id}" in call_args[1]
        assert call_kwargs["json"] == {"user": mock_user}
        assert response == mock_successful_response


class TestChatClientAudioToText:
    """Test audio-to-text conversion."""

    def test_audio_to_text_with_tuple(
        self,
        mock_api_key: str,
        mock_requests_request: Mock,
        mock_successful_response: Mock,
        mock_user: str,
    ) -> None:
        """Test converting audio to text with file tuple."""
        mock_requests_request.return_value = mock_successful_response

        client = ChatClient(api_key=mock_api_key)
        audio_file = ("audio.mp3", b"audio content", "audio/mpeg")
        response = client.audio_to_text(audio_file=audio_file, user=mock_user)

        # Verify request
        mock_requests_request.assert_called_once()
        call_args, call_kwargs = mock_requests_request.call_args
        assert call_args[0] == "POST"
        assert "/audio-to-text" in call_args[1]
        assert call_kwargs["data"] == {"user": mock_user}
        assert call_kwargs["files"]["file"] == audio_file
        assert response == mock_successful_response


class TestChatClientAnnotationAPIs:
    """Test annotation management APIs."""

    def test_annotation_reply_action_enable(
        self,
        mock_api_key: str,
        mock_requests_request: Mock,
        mock_successful_response: Mock,
    ) -> None:
        """Test enabling annotation reply feature."""
        mock_requests_request.return_value = mock_successful_response

        client = ChatClient(api_key=mock_api_key)
        response = client.annotation_reply_action(
            action="enable",
            score_threshold=0.8,
            embedding_provider_name="openai",
            embedding_model_name="text-embedding-ada-002",
        )

        # Verify request
        mock_requests_request.assert_called_once()
        call_args, call_kwargs = mock_requests_request.call_args
        assert call_args[0] == "POST"
        assert "/apps/annotation-reply/enable" in call_args[1]
        assert call_kwargs["json"]["score_threshold"] == 0.8
        assert call_kwargs["json"]["embedding_provider_name"] == "openai"
        assert response == mock_successful_response

    def test_annotation_reply_action_disable(
        self,
        mock_api_key: str,
        mock_requests_request: Mock,
        mock_successful_response: Mock,
    ) -> None:
        """Test disabling annotation reply feature."""
        mock_requests_request.return_value = mock_successful_response

        client = ChatClient(api_key=mock_api_key)
        response = client.annotation_reply_action(
            action="disable",
            score_threshold=0.5,
            embedding_provider_name="test",
            embedding_model_name="test-model",
        )

        # Verify disable action
        call_args = mock_requests_request.call_args[0]
        assert "/apps/annotation-reply/disable" in call_args[1]
        assert response == mock_successful_response

    def test_annotation_reply_action_raises_on_none_values(
        self, mock_api_key: str
    ) -> None:
        """Test that annotation reply action raises error for None values."""
        client = ChatClient(api_key=mock_api_key)

        with pytest.raises(ValueError) as exc_info:
            client.annotation_reply_action(
                action="enable",
                score_threshold=None,  # type: ignore[arg-type]
                embedding_provider_name="openai",
                embedding_model_name="test",
            )

        assert "cannot be None" in str(exc_info.value)

    def test_get_annotation_reply_status(
        self,
        mock_api_key: str,
        mock_requests_request: Mock,
        mock_successful_response: Mock,
    ) -> None:
        """Test getting annotation reply action status."""
        mock_requests_request.return_value = mock_successful_response

        client = ChatClient(api_key=mock_api_key)
        job_id = "job-123-abc"
        response = client.get_annotation_reply_status(action="enable", job_id=job_id)

        # Verify request
        mock_requests_request.assert_called_once()
        call_args = mock_requests_request.call_args[0]
        assert call_args[0] == "GET"
        assert f"/apps/annotation-reply/enable/status/{job_id}" in call_args[1]
        assert response == mock_successful_response

    def test_list_annotations_default(
        self,
        mock_api_key: str,
        mock_requests_request: Mock,
        mock_successful_response: Mock,
    ) -> None:
        """Test listing annotations with default parameters."""
        mock_requests_request.return_value = mock_successful_response

        client = ChatClient(api_key=mock_api_key)
        response = client.list_annotations()

        # Verify request
        call_kwargs = mock_requests_request.call_args[1]
        assert call_kwargs["params"]["page"] == 1
        assert call_kwargs["params"]["limit"] == 20
        assert response == mock_successful_response

    def test_list_annotations_with_pagination_and_keyword(
        self,
        mock_api_key: str,
        mock_requests_request: Mock,
        mock_successful_response: Mock,
    ) -> None:
        """Test listing annotations with pagination and keyword."""
        mock_requests_request.return_value = mock_successful_response

        client = ChatClient(api_key=mock_api_key)
        response = client.list_annotations(page=2, limit=50, keyword="test query")

        # Verify parameters
        call_kwargs = mock_requests_request.call_args[1]
        assert call_kwargs["params"]["page"] == 2
        assert call_kwargs["params"]["limit"] == 50
        assert call_kwargs["params"]["keyword"] == "test query"
        assert response == mock_successful_response

    def test_create_annotation(
        self,
        mock_api_key: str,
        mock_requests_request: Mock,
        mock_successful_response: Mock,
        sample_annotation_data: dict,
    ) -> None:
        """Test creating a new annotation."""
        mock_requests_request.return_value = mock_successful_response

        client = ChatClient(api_key=mock_api_key)
        response = client.create_annotation(
            question=sample_annotation_data["question"],
            answer=sample_annotation_data["answer"],
        )

        # Verify request
        mock_requests_request.assert_called_once()
        call_args, call_kwargs = mock_requests_request.call_args
        assert call_args[0] == "POST"
        assert "/apps/annotations" in call_args[1]
        assert call_kwargs["json"]["question"] == sample_annotation_data["question"]
        assert call_kwargs["json"]["answer"] == sample_annotation_data["answer"]
        assert response == mock_successful_response

    def test_update_annotation(
        self,
        mock_api_key: str,
        mock_requests_request: Mock,
        mock_successful_response: Mock,
        sample_annotation_data: dict,
    ) -> None:
        """Test updating an existing annotation."""
        mock_requests_request.return_value = mock_successful_response

        client = ChatClient(api_key=mock_api_key)
        annotation_id = "annotation-789"
        response = client.update_annotation(
            annotation_id=annotation_id,
            question="Updated question?",
            answer="Updated answer",
        )

        # Verify request
        mock_requests_request.assert_called_once()
        call_args, call_kwargs = mock_requests_request.call_args
        assert call_args[0] == "PUT"
        assert f"/apps/annotations/{annotation_id}" in call_args[1]
        assert call_kwargs["json"]["question"] == "Updated question?"
        assert response == mock_successful_response

    def test_delete_annotation(
        self,
        mock_api_key: str,
        mock_requests_request: Mock,
        mock_successful_response: Mock,
    ) -> None:
        """Test deleting an annotation."""
        mock_requests_request.return_value = mock_successful_response

        client = ChatClient(api_key=mock_api_key)
        annotation_id = "annotation-999"
        response = client.delete_annotation(annotation_id=annotation_id)

        # Verify request
        mock_requests_request.assert_called_once()
        call_args = mock_requests_request.call_args[0]
        assert call_args[0] == "DELETE"
        assert f"/apps/annotations/{annotation_id}" in call_args[1]
        assert response == mock_successful_response
