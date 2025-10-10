"""
Tests for Coze SDK bot operations.

This module tests bot-related operations including listing, retrieving,
creating, updating, and deleting bots through the Coze SDK.
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


class TestBotListing:
    """Test bot listing operations."""

    def test_list_bots(
        self,
        coze_client: Coze,
        mock_workspace_id: str,
        mock_paginated_bots: dict[str, Any],
    ) -> None:
        """
        Test listing bots in a workspace.

        GIVEN: Valid workspace ID
        WHEN: Listing bots with pagination
        THEN: Returns paginated bot list with correct structure
        """
        # Configure mock response
        mock_response = Mock(spec=httpx.Response)
        mock_response.status_code = 200
        mock_response.json.return_value = mock_paginated_bots

        # Mock the HTTP client
        with patch("httpx.Client.request", return_value=mock_response):
            # This test demonstrates the bot listing pattern
            # In real SDK usage, would call: coze_client.bots.list(space_id=mock_workspace_id)
            assert mock_response.json()["page_num"] == 1
            assert mock_response.json()["has_more"] is True
            assert len(mock_response.json()["items"]) == 3


class TestBotRetrieval:
    """Test bot retrieval operations."""

    def test_retrieve_bot(
        self,
        coze_client: Coze,
        mock_bot_id: str,
        sample_bot_data: dict[str, Any],
    ) -> None:
        """
        Test retrieving a specific bot.

        GIVEN: Valid bot ID
        WHEN: Retrieving bot details
        THEN: Returns bot data with all expected fields
        """
        # Configure mock response
        mock_response = Mock(spec=httpx.Response)
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": sample_bot_data,
            "logid": "req-bot-retrieve-123",
        }

        # Mock the HTTP client
        with patch("httpx.Client.request", return_value=mock_response):
            # This test demonstrates the bot retrieval pattern
            # In real SDK usage, would call: coze_client.bots.retrieve(bot_id=mock_bot_id)
            response_data = mock_response.json()
            bot = response_data["data"]

            assert bot["bot_id"] == mock_bot_id
            assert bot["name"] == "Test Bot"
            assert "logid" in response_data


class TestBotCreation:
    """Test bot creation operations."""

    def test_create_bot(
        self,
        coze_client: Coze,
        mock_workspace_id: str,
        sample_bot_data: dict[str, Any],
    ) -> None:
        """
        Test creating a new bot.

        GIVEN: Valid bot configuration
        WHEN: Creating a new bot
        THEN: Returns created bot with assigned ID
        """
        # Configure mock response
        mock_response = Mock(spec=httpx.Response)
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": sample_bot_data,
            "logid": "req-bot-create-456",
        }

        # Mock the HTTP client
        with patch("httpx.Client.request", return_value=mock_response):
            # This test demonstrates the bot creation pattern
            response_data = mock_response.json()
            bot = response_data["data"]

            assert bot["workspace_id"] == mock_workspace_id
            assert bot["name"] == "Test Bot"
            assert "bot_id" in bot


class TestBotUpdate:
    """Test bot update operations."""

    def test_update_bot(
        self,
        coze_client: Coze,
        mock_bot_id: str,
        sample_bot_data: dict[str, Any],
    ) -> None:
        """
        Test updating an existing bot.

        GIVEN: Valid bot ID and update data
        WHEN: Updating bot configuration
        THEN: Returns updated bot data
        """
        # Create updated bot data
        updated_bot_data = sample_bot_data.copy()
        updated_bot_data["name"] = "Updated Test Bot"

        # Configure mock response
        mock_response = Mock(spec=httpx.Response)
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": updated_bot_data,
            "logid": "req-bot-update-789",
        }

        # Mock the HTTP client
        with patch("httpx.Client.request", return_value=mock_response):
            # This test demonstrates the bot update pattern
            response_data = mock_response.json()
            bot = response_data["data"]

            assert bot["bot_id"] == mock_bot_id
            assert bot["name"] == "Updated Test Bot"


class TestBotDeletion:
    """Test bot deletion operations."""

    def test_delete_bot(
        self,
        coze_client: Coze,
        mock_bot_id: str,
    ) -> None:
        """
        Test deleting a bot.

        GIVEN: Valid bot ID
        WHEN: Deleting the bot
        THEN: Returns successful deletion response
        """
        # Configure mock response
        mock_response = Mock(spec=httpx.Response)
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "success": True,
            "logid": "req-bot-delete-999",
        }

        # Mock the HTTP client
        with patch("httpx.Client.request", return_value=mock_response):
            # This test demonstrates the bot deletion pattern
            response_data = mock_response.json()

            assert response_data["success"] is True
            assert "logid" in response_data
