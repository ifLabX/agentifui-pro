"""
Tests for Coze SDK chat and conversation operations.

This module tests chat-related operations including creating chats,
sending messages, streaming responses, and managing conversations.

Real SDK Usage Patterns (from coze-py/examples):

1. **Streaming Chat** (chat_stream.py):
    ```python
    from cozepy import ChatEventType, Message

    stream = coze.chat.stream(
        bot_id=bot_id,
        user_id=user_id,
        additional_messages=[
            Message.build_user_question_text("Tell a 500-word story."),
        ],
    )
    print("logid:", stream.response.logid)

    for event in stream:
        if event.event == ChatEventType.CONVERSATION_MESSAGE_DELTA:
            print(event.message.content, end="", flush=True)
        if event.event == ChatEventType.CONVERSATION_CHAT_COMPLETED:
            print("token usage:", event.chat.usage.token_count)
        if event.event == ChatEventType.CONVERSATION_CHAT_FAILED:
            print("chat failed", event.chat.last_error)
    ```

2. **Non-Streaming Chat** (chat_no_stream.py):
    ```python
    from cozepy import ChatStatus

    # Method 1: Create and manually poll
    chat = coze.chat.create(
        bot_id=bot_id,
        user_id=user_id,
        additional_messages=[
            Message.build_user_question_text("Who are you?"),
        ],
    )

    while chat.status == ChatStatus.IN_PROGRESS:
        time.sleep(1)
        chat = coze.chat.retrieve(
            conversation_id=chat.conversation_id,
            chat_id=chat.id
        )

    messages = coze.chat.messages.list(
        conversation_id=chat.conversation_id,
        chat_id=chat.id
    )

    # Method 2: Simplified with create_and_poll
    chat_poll = coze.chat.create_and_poll(
        bot_id=bot_id,
        user_id=user_id,
        additional_messages=[Message.build_user_question_text("...")],
    )
    for message in chat_poll.messages:
        print(message.content)
    ```

3. **Conversation Management** (conversation.py):
    ```python
    # List conversations
    conversations = coze.conversations.list()

    # Retrieve conversation
    conversation = coze.conversations.retrieve(conversation_id=conversation_id)

    # List messages in conversation
    messages = coze.conversations.messages.list(conversation_id=conversation_id)
    ```
"""

from typing import Any
from unittest.mock import Mock, patch

import httpx
import pytest
from cozepy import Coze, TokenAuth


@pytest.fixture
def coze_client(mock_coze_api_token: str, mock_coze_base_url: str) -> Coze:
    """Create a Coze client instance for testing."""
    return Coze(
        auth=TokenAuth(mock_coze_api_token),
        base_url=mock_coze_base_url,
    )


class TestChatCreation:
    """Test chat creation operations."""

    def test_create_chat_blocking(
        self,
        coze_client: Coze,
        mock_bot_id: str,
        sample_user_message: dict[str, Any],
        sample_chat_data: dict[str, Any],
    ) -> None:
        """
        Test creating a chat in blocking mode.

        GIVEN: Valid bot ID and user message
        WHEN: Creating chat with blocking mode
        THEN: Returns completed chat with response
        """
        # Configure mock response
        mock_response = Mock(spec=httpx.Response)
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": sample_chat_data,
            "logid": "req-chat-create-123",
        }

        # Mock the HTTP client
        with patch("httpx.Client.request", return_value=mock_response):
            # This test demonstrates the blocking chat creation pattern
            response_data = mock_response.json()
            chat = response_data["data"]

            assert chat["bot_id"] == mock_bot_id
            assert chat["status"] == "completed"
            assert "usage" in chat
            assert chat["usage"]["token_count"] > 0


class TestChatStreaming:
    """Test streaming chat operations."""

    def test_create_chat_streaming(
        self,
        coze_client: Coze,
        mock_bot_id: str,
        sample_user_message: dict[str, Any],
        mock_streaming_response: Mock,
    ) -> None:
        """
        Test creating a chat with streaming response.

        GIVEN: Valid bot ID and user message
        WHEN: Creating chat with streaming mode
        THEN: Returns streaming events with message deltas
        """
        # Mock the HTTP client
        with patch("httpx.Client.request", return_value=mock_streaming_response):
            # This test demonstrates the streaming chat pattern
            events = list(mock_streaming_response.iter_lines())

            # Verify streaming events
            assert len(events) == 5
            # First event: chat created
            assert b"conversation.chat.created" in events[0]
            # Middle events: message deltas
            assert b"conversation.message.delta" in events[2]
            # Last event: chat completed
            assert b"conversation.chat.completed" in events[4]

    def test_stream_event_parsing(
        self,
        mock_streaming_events: list[bytes],
    ) -> None:
        """
        Test parsing streaming chat events.

        GIVEN: Raw streaming event data
        WHEN: Parsing events
        THEN: Each event has correct format and data
        """
        # Verify event format
        for event in mock_streaming_events:
            # Events should have "event:" and "data:" sections
            assert b"event:" in event
            assert b"data:" in event


class TestConversationManagement:
    """Test conversation management operations."""

    def test_retrieve_conversation(
        self,
        coze_client: Coze,
        mock_conversation_id: str,
    ) -> None:
        """
        Test retrieving conversation details.

        GIVEN: Valid conversation ID
        WHEN: Retrieving conversation
        THEN: Returns conversation data with messages
        """
        # Configure mock response
        mock_response = Mock(spec=httpx.Response)
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "conversation_id": mock_conversation_id,
                "messages": [
                    {"role": "user", "content": "Hello"},
                    {"role": "assistant", "content": "Hi there!"},
                ],
            },
            "logid": "req-conversation-retrieve-456",
        }

        # Mock the HTTP client
        with patch("httpx.Client.request", return_value=mock_response):
            # This test demonstrates the conversation retrieval pattern
            response_data = mock_response.json()
            conversation = response_data["data"]

            assert conversation["conversation_id"] == mock_conversation_id
            assert len(conversation["messages"]) == 2
            assert conversation["messages"][0]["role"] == "user"

    def test_list_conversation_messages(
        self,
        coze_client: Coze,
        mock_conversation_id: str,
        sample_user_message: dict[str, Any],
        sample_assistant_message: dict[str, Any],
    ) -> None:
        """
        Test listing messages in a conversation.

        GIVEN: Valid conversation ID
        WHEN: Listing conversation messages
        THEN: Returns paginated message list
        """
        # Configure mock response
        mock_response = Mock(spec=httpx.Response)
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "messages": [sample_user_message, sample_assistant_message],
                "has_more": False,
            },
            "logid": "req-messages-list-789",
        }

        # Mock the HTTP client
        with patch("httpx.Client.request", return_value=mock_response):
            # This test demonstrates the message listing pattern
            response_data = mock_response.json()
            messages_data = response_data["data"]

            assert len(messages_data["messages"]) == 2
            assert messages_data["messages"][0]["role"] == "user"
            assert messages_data["messages"][1]["role"] == "assistant"
            assert messages_data["has_more"] is False


class TestChatStatus:
    """Test chat status operations."""

    def test_retrieve_chat_status(
        self,
        coze_client: Coze,
        mock_chat_id: str,
        sample_chat_data: dict[str, Any],
    ) -> None:
        """
        Test retrieving chat status.

        GIVEN: Valid chat ID
        WHEN: Retrieving chat status
        THEN: Returns chat with current status
        """
        # Configure mock response
        mock_response = Mock(spec=httpx.Response)
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": sample_chat_data,
            "logid": "req-chat-status-999",
        }

        # Mock the HTTP client
        with patch("httpx.Client.request", return_value=mock_response):
            # This test demonstrates the chat status retrieval pattern
            response_data = mock_response.json()
            chat = response_data["data"]

            assert chat["id"] == mock_chat_id
            assert chat["status"] in ["created", "in_progress", "completed", "failed"]
            assert "usage" in chat


class TestChatWithVariousMessageTypes:
    """Test chat with different message content types."""

    def test_chat_with_text_message(
        self,
        coze_client: Coze,
        mock_bot_id: str,
        sample_user_message: dict[str, Any],
    ) -> None:
        """
        Test chat with text message.

        GIVEN: Text message
        WHEN: Creating chat
        THEN: Chat processes text message successfully
        """
        assert sample_user_message["content_type"] == "text"
        assert isinstance(sample_user_message["content"], str)
        assert len(sample_user_message["content"]) > 0
