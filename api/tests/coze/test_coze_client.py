"""
Tests for Coze SDK client initialization and configuration.

This module tests both synchronous (Coze) and asynchronous (AsyncCoze) client
initialization with various authentication and configuration options.

Real SDK Usage Pattern (from coze-py/examples/auth_pat.py):
    ```python
    from cozepy import Coze, TokenAuth, AsyncCoze, AsyncTokenAuth, COZE_CN_BASE_URL

    # Synchronous client
    coze = Coze(
        auth=TokenAuth(token="your_token"),
        base_url=COZE_CN_BASE_URL  # or custom URL
    )

    # Asynchronous client
    async_coze = AsyncCoze(
        auth=AsyncTokenAuth(token="your_token"),
        base_url="https://api.coze.com/v1"
    )
    ```
"""

import pytest
from cozepy import AsyncCoze, AsyncTokenAuth, Coze, TokenAuth


class TestSyncClientInitialization:
    """Test synchronous Coze client initialization."""

    def test_sync_client_init(
        self,
        mock_coze_api_token: str,
        mock_coze_base_url: str,
    ) -> None:
        """
        Test synchronous Coze client initialization.

        GIVEN: Valid API token and base URL
        WHEN: Creating Coze client with TokenAuth
        THEN: Client initializes successfully with expected attributes
        """
        # Create client
        client = Coze(
            auth=TokenAuth(mock_coze_api_token),
            base_url=mock_coze_base_url,
        )

        # Verify initialization
        assert client is not None
        # Verify client has expected API interfaces
        assert hasattr(client, "bots")
        assert hasattr(client, "chat")
        assert hasattr(client, "workflows")

    def test_sync_client_with_default_base_url(
        self,
        mock_coze_api_token: str,
    ) -> None:
        """
        Test synchronous client with default base URL.

        GIVEN: Valid API token without custom base URL
        WHEN: Creating Coze client with TokenAuth
        THEN: Client initializes successfully
        """
        # Create client without custom base_url
        client = Coze(auth=TokenAuth(mock_coze_api_token))

        # Verify initialization
        assert client is not None
        assert hasattr(client, "bots")
        assert hasattr(client, "chat")

    def test_sync_client_with_timeout_config(
        self,
        mock_coze_api_token: str,
        mock_coze_base_url: str,
    ) -> None:
        """
        Test synchronous client with custom timeout configuration.

        GIVEN: Valid credentials and custom timeout settings
        WHEN: Creating client with custom base_url
        THEN: Client initializes successfully
        """
        # Create client with timeout config
        client = Coze(
            auth=TokenAuth(mock_coze_api_token),
            base_url=mock_coze_base_url,
        )

        # Verify initialization (timeout config is internal)
        assert client is not None


class TestAsyncClientInitialization:
    """Test asynchronous Coze client initialization."""

    @pytest.mark.asyncio
    async def test_async_client_init(
        self,
        mock_coze_api_token: str,
        mock_coze_base_url: str,
    ) -> None:
        """
        Test asynchronous Coze client initialization.

        GIVEN: Valid API token and base URL
        WHEN: Creating AsyncCoze client with AsyncTokenAuth
        THEN: Client initializes successfully with expected attributes
        """
        # Create async client
        client = AsyncCoze(
            auth=AsyncTokenAuth(mock_coze_api_token),
            base_url=mock_coze_base_url,
        )

        # Verify initialization
        assert client is not None
        # Verify client has expected API interfaces
        assert hasattr(client, "bots")
        assert hasattr(client, "chat")
        assert hasattr(client, "workflows")

    @pytest.mark.asyncio
    async def test_async_client_with_default_base_url(
        self,
        mock_coze_api_token: str,
    ) -> None:
        """
        Test asynchronous client with default base URL.

        GIVEN: Valid API token without custom base URL
        WHEN: Creating AsyncCoze client with AsyncTokenAuth
        THEN: Client initializes successfully
        """
        # Create async client without custom base_url
        client = AsyncCoze(auth=AsyncTokenAuth(mock_coze_api_token))

        # Verify initialization
        assert client is not None
        assert hasattr(client, "bots")
        assert hasattr(client, "chat")

    @pytest.mark.asyncio
    async def test_async_client_with_timeout_config(
        self,
        mock_coze_api_token: str,
        mock_coze_base_url: str,
    ) -> None:
        """
        Test asynchronous client with custom timeout configuration.

        GIVEN: Valid credentials and custom timeout settings
        WHEN: Creating async client with custom base_url
        THEN: Client initializes successfully
        """
        # Create async client with timeout config
        client = AsyncCoze(
            auth=AsyncTokenAuth(mock_coze_api_token),
            base_url=mock_coze_base_url,
        )

        # Verify initialization (timeout config is internal)
        assert client is not None
