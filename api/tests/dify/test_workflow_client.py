"""
Tests for AsyncWorkflowClient.

This module tests the AsyncWorkflowClient functionality including:
- Workflow execution (run, stop, get results)
- Workflow logs retrieval with filtering
- Specific workflow execution
"""

from dify_client.async_client import AsyncWorkflowClient
from pytest_httpx import HTTPXMock


class TestWorkflowClientInitialization:
    """Test AsyncWorkflowClient initialization."""

    async def test_workflow_client_inherits_from_dify_client(self, mock_api_key: str) -> None:
        """Test that AsyncWorkflowClient inherits from AsyncDifyClient."""
        client = AsyncWorkflowClient(api_key=mock_api_key)

        assert hasattr(client, "api_key")
        assert hasattr(client, "base_url")
        assert client.api_key == mock_api_key


class TestWorkflowClientRun:
    """Test workflow execution."""

    async def test_run_workflow_blocking(
        self,
        httpx_mock: HTTPXMock,
        mock_api_key: str,
        sample_inputs: dict,
        mock_user: str,
    ) -> None:
        """Test running a workflow in blocking mode."""
        httpx_mock.add_response(
            url="https://api.dify.ai/v1/workflows/run",
            method="POST",
            json={"success": True},
            status_code=200,
        )

        client = AsyncWorkflowClient(api_key=mock_api_key)
        response = await client.run(
            inputs=sample_inputs,
            response_mode="blocking",
            user=mock_user,
        )

        # Verify request
        requests = httpx_mock.get_requests()
        assert len(requests) == 1
        request = requests[0]
        assert request.method == "POST"
        assert "/workflows/run" in str(request.url)

        import json

        request_body = json.loads(request.content)
        assert request_body["inputs"] == sample_inputs
        assert request_body["response_mode"] == "blocking"
        assert request_body["user"] == mock_user
        assert response.status_code == 200

    async def test_run_workflow_streaming(
        self,
        httpx_mock: HTTPXMock,
        mock_api_key: str,
        sample_inputs: dict,
    ) -> None:
        """Test running a workflow in streaming mode."""
        httpx_mock.add_response(
            url="https://api.dify.ai/v1/workflows/run",
            method="POST",
            json={"success": True},
            status_code=200,
        )

        client = AsyncWorkflowClient(api_key=mock_api_key)
        response = await client.run(
            inputs=sample_inputs,
            response_mode="streaming",
        )

        # Verify streaming mode
        requests = httpx_mock.get_requests()
        assert len(requests) == 1
        request = requests[0]

        import json

        request_body = json.loads(request.content)
        assert request_body["response_mode"] == "streaming"
        assert response.status_code == 200

    async def test_run_workflow_default_params(
        self,
        httpx_mock: HTTPXMock,
        mock_api_key: str,
        sample_inputs: dict,
    ) -> None:
        """Test running a workflow with default parameters."""
        httpx_mock.add_response(
            url="https://api.dify.ai/v1/workflows/run",
            method="POST",
            json={"success": True},
            status_code=200,
        )

        client = AsyncWorkflowClient(api_key=mock_api_key)
        response = await client.run(inputs=sample_inputs)

        # Verify default values
        requests = httpx_mock.get_requests()
        assert len(requests) == 1
        request = requests[0]

        import json

        request_body = json.loads(request.content)
        assert request_body["response_mode"] == "streaming"
        assert request_body["user"] == "abc-123"
        assert response.status_code == 200


class TestWorkflowClientStop:
    """Test stopping workflow execution."""

    async def test_stop_workflow(
        self,
        httpx_mock: HTTPXMock,
        mock_api_key: str,
        sample_task_id: str,
        mock_user: str,
    ) -> None:
        """Test stopping a running workflow."""
        httpx_mock.add_response(
            url=f"https://api.dify.ai/v1/workflows/tasks/{sample_task_id}/stop",
            method="POST",
            json={"success": True},
            status_code=200,
        )

        client = AsyncWorkflowClient(api_key=mock_api_key)
        response = await client.stop(task_id=sample_task_id, user=mock_user)

        # Verify request
        requests = httpx_mock.get_requests()
        assert len(requests) == 1
        request = requests[0]
        assert request.method == "POST"
        assert f"/workflows/tasks/{sample_task_id}/stop" in str(request.url)

        import json

        request_body = json.loads(request.content)
        assert request_body == {"user": mock_user}
        assert response.status_code == 200


class TestWorkflowClientGetResult:
    """Test getting workflow results."""

    async def test_get_workflow_result(
        self,
        httpx_mock: HTTPXMock,
        mock_api_key: str,
    ) -> None:
        """Test retrieving workflow execution result."""
        workflow_run_id = "run-12345-abc"
        httpx_mock.add_response(
            url=f"https://api.dify.ai/v1/workflows/run/{workflow_run_id}",
            method="GET",
            json={"success": True},
            status_code=200,
        )

        client = AsyncWorkflowClient(api_key=mock_api_key)
        response = await client.get_result(workflow_run_id=workflow_run_id)

        # Verify request
        requests = httpx_mock.get_requests()
        assert len(requests) == 1
        request = requests[0]
        assert request.method == "GET"
        assert f"/workflows/run/{workflow_run_id}" in str(request.url)
        assert response.status_code == 200


class TestWorkflowClientGetLogs:
    """Test getting workflow logs."""

    async def test_get_workflow_logs_default(
        self,
        httpx_mock: HTTPXMock,
        mock_api_key: str,
    ) -> None:
        """Test getting workflow logs with default parameters."""
        httpx_mock.add_response(
            method="GET",
            json={"success": True},
            status_code=200,
        )

        client = AsyncWorkflowClient(api_key=mock_api_key)
        response = await client.get_workflow_logs()

        # Verify request
        requests = httpx_mock.get_requests()
        assert len(requests) == 1
        request = requests[0]
        assert request.method == "GET"
        assert "/workflows/logs" in str(request.url)
        assert "page=1" in str(request.url)
        assert "limit=20" in str(request.url)
        assert response.status_code == 200

    async def test_get_workflow_logs_with_pagination(
        self,
        httpx_mock: HTTPXMock,
        mock_api_key: str,
    ) -> None:
        """Test getting workflow logs with pagination."""
        httpx_mock.add_response(
            method="GET",
            json={"success": True},
            status_code=200,
        )

        client = AsyncWorkflowClient(api_key=mock_api_key)
        response = await client.get_workflow_logs(page=3, limit=50)

        # Verify pagination
        requests = httpx_mock.get_requests()
        assert len(requests) == 1
        request = requests[0]
        assert "page=3" in str(request.url)
        assert "limit=50" in str(request.url)
        assert response.status_code == 200

    async def test_get_workflow_logs_with_keyword(
        self,
        httpx_mock: HTTPXMock,
        mock_api_key: str,
    ) -> None:
        """Test getting workflow logs with keyword filter."""
        httpx_mock.add_response(
            method="GET",
            json={"success": True},
            status_code=200,
        )

        client = AsyncWorkflowClient(api_key=mock_api_key)
        response = await client.get_workflow_logs(keyword="error")

        # Verify keyword filter
        requests = httpx_mock.get_requests()
        assert len(requests) == 1
        request = requests[0]
        assert "keyword=error" in str(request.url)
        assert response.status_code == 200

    async def test_get_workflow_logs_with_status_filter(
        self,
        httpx_mock: HTTPXMock,
        mock_api_key: str,
    ) -> None:
        """Test getting workflow logs with status filter."""
        httpx_mock.add_response(
            method="GET",
            json={"success": True},
            status_code=200,
        )

        client = AsyncWorkflowClient(api_key=mock_api_key)
        response = await client.get_workflow_logs(status="succeeded")

        # Verify status filter
        requests = httpx_mock.get_requests()
        assert len(requests) == 1
        request = requests[0]
        assert "status=succeeded" in str(request.url)
        assert response.status_code == 200

    async def test_get_workflow_logs_with_date_filters(
        self,
        httpx_mock: HTTPXMock,
        mock_api_key: str,
    ) -> None:
        """Test getting workflow logs with date range filters."""
        httpx_mock.add_response(
            method="GET",
            json={"success": True},
            status_code=200,
        )

        client = AsyncWorkflowClient(api_key=mock_api_key)
        response = await client.get_workflow_logs(
            created_at__before="2025-10-09T23:59:59Z",
            created_at__after="2025-10-01T00:00:00Z",
        )

        # Verify date filters
        requests = httpx_mock.get_requests()
        assert len(requests) == 1
        request = requests[0]
        assert "created_at__before" in str(request.url)
        assert "created_at__after" in str(request.url)
        assert response.status_code == 200

    async def test_get_workflow_logs_with_creator_filters(
        self,
        httpx_mock: HTTPXMock,
        mock_api_key: str,
    ) -> None:
        """Test getting workflow logs with creator filters."""
        httpx_mock.add_response(
            method="GET",
            json={"success": True},
            status_code=200,
        )

        client = AsyncWorkflowClient(api_key=mock_api_key)
        response = await client.get_workflow_logs(
            created_by_end_user_session_id="session-123",
            created_by_account="account-456",
        )

        # Verify creator filters
        requests = httpx_mock.get_requests()
        assert len(requests) == 1
        request = requests[0]
        assert "created_by_end_user_session_id=session-123" in str(request.url)
        assert "created_by_account=account-456" in str(request.url)
        assert response.status_code == 200

    async def test_get_workflow_logs_all_filters(
        self,
        httpx_mock: HTTPXMock,
        mock_api_key: str,
    ) -> None:
        """Test getting workflow logs with all filters combined."""
        httpx_mock.add_response(
            method="GET",
            json={"success": True},
            status_code=200,
        )

        client = AsyncWorkflowClient(api_key=mock_api_key)
        response = await client.get_workflow_logs(
            keyword="processing",
            status="failed",
            page=2,
            limit=30,
            created_at__before="2025-10-09T23:59:59Z",
            created_at__after="2025-10-08T00:00:00Z",
            created_by_end_user_session_id="session-789",
            created_by_account="account-101",
        )

        # Verify all filters
        requests = httpx_mock.get_requests()
        assert len(requests) == 1
        request = requests[0]
        url_str = str(request.url)
        assert "keyword=processing" in url_str
        assert "status=failed" in url_str
        assert "page=2" in url_str
        assert "limit=30" in url_str
        assert response.status_code == 200


class TestWorkflowClientRunSpecific:
    """Test running specific workflow by ID."""

    async def test_run_specific_workflow_blocking(
        self,
        httpx_mock: HTTPXMock,
        mock_api_key: str,
        sample_workflow_id: str,
        sample_inputs: dict,
        mock_user: str,
    ) -> None:
        """Test running a specific workflow in blocking mode."""
        httpx_mock.add_response(
            url=f"https://api.dify.ai/v1/workflows/{sample_workflow_id}/run",
            method="POST",
            json={"success": True},
            status_code=200,
        )

        client = AsyncWorkflowClient(api_key=mock_api_key)
        response = await client.run_specific_workflow(
            workflow_id=sample_workflow_id,
            inputs=sample_inputs,
            response_mode="blocking",
            user=mock_user,
        )

        # Verify request
        requests = httpx_mock.get_requests()
        assert len(requests) == 1
        request = requests[0]
        assert request.method == "POST"
        assert f"/workflows/{sample_workflow_id}/run" in str(request.url)

        import json

        request_body = json.loads(request.content)
        assert request_body["inputs"] == sample_inputs
        assert response.status_code == 200

    async def test_run_specific_workflow_streaming(
        self,
        httpx_mock: HTTPXMock,
        mock_api_key: str,
        sample_workflow_id: str,
        sample_inputs: dict,
    ) -> None:
        """Test running a specific workflow in streaming mode."""
        httpx_mock.add_response(
            url=f"https://api.dify.ai/v1/workflows/{sample_workflow_id}/run",
            method="POST",
            json={"success": True},
            status_code=200,
        )

        client = AsyncWorkflowClient(api_key=mock_api_key)
        response = await client.run_specific_workflow(
            workflow_id=sample_workflow_id,
            inputs=sample_inputs,
            response_mode="streaming",
        )

        # Verify streaming is enabled
        requests = httpx_mock.get_requests()
        assert len(requests) == 1
        assert response.status_code == 200

    async def test_run_specific_workflow_default_params(
        self,
        httpx_mock: HTTPXMock,
        mock_api_key: str,
        sample_workflow_id: str,
        sample_inputs: dict,
    ) -> None:
        """Test running a specific workflow with default parameters."""
        httpx_mock.add_response(
            url=f"https://api.dify.ai/v1/workflows/{sample_workflow_id}/run",
            method="POST",
            json={"success": True},
            status_code=200,
        )

        client = AsyncWorkflowClient(api_key=mock_api_key)
        response = await client.run_specific_workflow(
            workflow_id=sample_workflow_id,
            inputs=sample_inputs,
        )

        # Verify defaults
        requests = httpx_mock.get_requests()
        assert len(requests) == 1
        request = requests[0]

        import json

        request_body = json.loads(request.content)
        assert request_body["response_mode"] == "streaming"
        assert request_body["user"] == "abc-123"
        assert response.status_code == 200
