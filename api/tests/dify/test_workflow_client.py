"""
Tests for WorkflowClient.

This module tests the WorkflowClient functionality including:
- Workflow execution (run, stop, get results)
- Workflow logs retrieval with filtering
- Specific workflow execution
"""

from unittest.mock import Mock

from dify_client import WorkflowClient


class TestWorkflowClientInitialization:
    """Test WorkflowClient initialization."""

    def test_workflow_client_inherits_from_dify_client(
        self, mock_api_key: str
    ) -> None:
        """Test that WorkflowClient inherits from DifyClient."""
        client = WorkflowClient(api_key=mock_api_key)

        assert hasattr(client, "api_key")
        assert hasattr(client, "base_url")
        assert client.api_key == mock_api_key


class TestWorkflowClientRun:
    """Test workflow execution."""

    def test_run_workflow_blocking(
        self,
        mock_api_key: str,
        mock_requests_request: Mock,
        mock_successful_response: Mock,
        sample_inputs: dict,
        mock_user: str,
    ) -> None:
        """Test running a workflow in blocking mode."""
        mock_requests_request.return_value = mock_successful_response

        client = WorkflowClient(api_key=mock_api_key)
        response = client.run(
            inputs=sample_inputs,
            response_mode="blocking",
            user=mock_user,
        )

        # Verify request
        mock_requests_request.assert_called_once()
        call_args, call_kwargs = mock_requests_request.call_args
        assert call_args[0] == "POST"
        assert "/workflows/run" in call_args[1]
        assert call_kwargs["json"]["inputs"] == sample_inputs
        assert call_kwargs["json"]["response_mode"] == "blocking"
        assert call_kwargs["json"]["user"] == mock_user
        assert response == mock_successful_response

    def test_run_workflow_streaming(
        self,
        mock_api_key: str,
        mock_requests_request: Mock,
        mock_streaming_response: Mock,
        sample_inputs: dict,
    ) -> None:
        """Test running a workflow in streaming mode."""
        mock_requests_request.return_value = mock_streaming_response

        client = WorkflowClient(api_key=mock_api_key)
        response = client.run(
            inputs=sample_inputs,
            response_mode="streaming",
        )

        # Verify streaming mode
        call_kwargs = mock_requests_request.call_args[1]
        assert call_kwargs["json"]["response_mode"] == "streaming"
        assert response == mock_streaming_response

    def test_run_workflow_default_params(
        self,
        mock_api_key: str,
        mock_requests_request: Mock,
        mock_successful_response: Mock,
        sample_inputs: dict,
    ) -> None:
        """Test running a workflow with default parameters."""
        mock_requests_request.return_value = mock_successful_response

        client = WorkflowClient(api_key=mock_api_key)
        response = client.run(inputs=sample_inputs)

        # Verify default values
        call_kwargs = mock_requests_request.call_args[1]
        assert call_kwargs["json"]["response_mode"] == "streaming"
        assert call_kwargs["json"]["user"] == "abc-123"
        assert response == mock_successful_response


class TestWorkflowClientStop:
    """Test stopping workflow execution."""

    def test_stop_workflow(
        self,
        mock_api_key: str,
        mock_requests_request: Mock,
        mock_successful_response: Mock,
        sample_task_id: str,
        mock_user: str,
    ) -> None:
        """Test stopping a running workflow."""
        mock_requests_request.return_value = mock_successful_response

        client = WorkflowClient(api_key=mock_api_key)
        response = client.stop(task_id=sample_task_id, user=mock_user)

        # Verify request
        mock_requests_request.assert_called_once()
        call_args, call_kwargs = mock_requests_request.call_args
        assert call_args[0] == "POST"
        assert f"/workflows/tasks/{sample_task_id}/stop" in call_args[1]
        assert call_kwargs["json"] == {"user": mock_user}
        assert response == mock_successful_response


class TestWorkflowClientGetResult:
    """Test getting workflow results."""

    def test_get_workflow_result(
        self,
        mock_api_key: str,
        mock_requests_request: Mock,
        mock_successful_response: Mock,
    ) -> None:
        """Test retrieving workflow execution result."""
        mock_requests_request.return_value = mock_successful_response

        client = WorkflowClient(api_key=mock_api_key)
        workflow_run_id = "run-12345-abc"
        response = client.get_result(workflow_run_id=workflow_run_id)

        # Verify request
        mock_requests_request.assert_called_once()
        call_args = mock_requests_request.call_args[0]
        assert call_args[0] == "GET"
        assert f"/workflows/run/{workflow_run_id}" in call_args[1]
        assert response == mock_successful_response


class TestWorkflowClientGetLogs:
    """Test getting workflow logs."""

    def test_get_workflow_logs_default(
        self,
        mock_api_key: str,
        mock_requests_request: Mock,
        mock_successful_response: Mock,
    ) -> None:
        """Test getting workflow logs with default parameters."""
        mock_requests_request.return_value = mock_successful_response

        client = WorkflowClient(api_key=mock_api_key)
        response = client.get_workflow_logs()

        # Verify request
        mock_requests_request.assert_called_once()
        call_args, call_kwargs = mock_requests_request.call_args
        assert call_args[0] == "GET"
        assert "/workflows/logs" in call_args[1]
        assert call_kwargs["params"]["page"] == 1
        assert call_kwargs["params"]["limit"] == 20
        assert response == mock_successful_response

    def test_get_workflow_logs_with_pagination(
        self,
        mock_api_key: str,
        mock_requests_request: Mock,
        mock_successful_response: Mock,
    ) -> None:
        """Test getting workflow logs with pagination."""
        mock_requests_request.return_value = mock_successful_response

        client = WorkflowClient(api_key=mock_api_key)
        response = client.get_workflow_logs(page=3, limit=50)

        # Verify pagination
        call_kwargs = mock_requests_request.call_args[1]
        assert call_kwargs["params"]["page"] == 3
        assert call_kwargs["params"]["limit"] == 50
        assert response == mock_successful_response

    def test_get_workflow_logs_with_keyword(
        self,
        mock_api_key: str,
        mock_requests_request: Mock,
        mock_successful_response: Mock,
    ) -> None:
        """Test getting workflow logs with keyword filter."""
        mock_requests_request.return_value = mock_successful_response

        client = WorkflowClient(api_key=mock_api_key)
        response = client.get_workflow_logs(keyword="error")

        # Verify keyword filter
        call_kwargs = mock_requests_request.call_args[1]
        assert call_kwargs["params"]["keyword"] == "error"
        assert response == mock_successful_response

    def test_get_workflow_logs_with_status_filter(
        self,
        mock_api_key: str,
        mock_requests_request: Mock,
        mock_successful_response: Mock,
    ) -> None:
        """Test getting workflow logs with status filter."""
        mock_requests_request.return_value = mock_successful_response

        client = WorkflowClient(api_key=mock_api_key)
        response = client.get_workflow_logs(status="succeeded")

        # Verify status filter
        call_kwargs = mock_requests_request.call_args[1]
        assert call_kwargs["params"]["status"] == "succeeded"
        assert response == mock_successful_response

    def test_get_workflow_logs_with_date_filters(
        self,
        mock_api_key: str,
        mock_requests_request: Mock,
        mock_successful_response: Mock,
    ) -> None:
        """Test getting workflow logs with date range filters."""
        mock_requests_request.return_value = mock_successful_response

        client = WorkflowClient(api_key=mock_api_key)
        response = client.get_workflow_logs(
            created_at__before="2025-10-09T23:59:59Z",
            created_at__after="2025-10-01T00:00:00Z",
        )

        # Verify date filters
        call_kwargs = mock_requests_request.call_args[1]
        assert "created_at__before" in call_kwargs["params"]
        assert "created_at__after" in call_kwargs["params"]
        assert response == mock_successful_response

    def test_get_workflow_logs_with_creator_filters(
        self,
        mock_api_key: str,
        mock_requests_request: Mock,
        mock_successful_response: Mock,
    ) -> None:
        """Test getting workflow logs with creator filters."""
        mock_requests_request.return_value = mock_successful_response

        client = WorkflowClient(api_key=mock_api_key)
        response = client.get_workflow_logs(
            created_by_end_user_session_id="session-123",
            created_by_account="account-456",
        )

        # Verify creator filters
        call_kwargs = mock_requests_request.call_args[1]
        assert call_kwargs["params"]["created_by_end_user_session_id"] == "session-123"
        assert call_kwargs["params"]["created_by_account"] == "account-456"
        assert response == mock_successful_response

    def test_get_workflow_logs_all_filters(
        self,
        mock_api_key: str,
        mock_requests_request: Mock,
        mock_successful_response: Mock,
    ) -> None:
        """Test getting workflow logs with all filters combined."""
        mock_requests_request.return_value = mock_successful_response

        client = WorkflowClient(api_key=mock_api_key)
        response = client.get_workflow_logs(
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
        call_kwargs = mock_requests_request.call_args[1]
        params = call_kwargs["params"]
        assert params["keyword"] == "processing"
        assert params["status"] == "failed"
        assert params["page"] == 2
        assert params["limit"] == 30
        assert response == mock_successful_response


class TestWorkflowClientRunSpecific:
    """Test running specific workflow by ID."""

    def test_run_specific_workflow_blocking(
        self,
        mock_api_key: str,
        mock_requests_request: Mock,
        mock_successful_response: Mock,
        sample_workflow_id: str,
        sample_inputs: dict,
        mock_user: str,
    ) -> None:
        """Test running a specific workflow in blocking mode."""
        mock_requests_request.return_value = mock_successful_response

        client = WorkflowClient(api_key=mock_api_key)
        response = client.run_specific_workflow(
            workflow_id=sample_workflow_id,
            inputs=sample_inputs,
            response_mode="blocking",
            user=mock_user,
        )

        # Verify request
        mock_requests_request.assert_called_once()
        call_args, call_kwargs = mock_requests_request.call_args
        assert call_args[0] == "POST"
        assert f"/workflows/{sample_workflow_id}/run" in call_args[1]
        assert call_kwargs["json"]["inputs"] == sample_inputs
        assert call_kwargs["stream"] is False
        assert response == mock_successful_response

    def test_run_specific_workflow_streaming(
        self,
        mock_api_key: str,
        mock_requests_request: Mock,
        mock_streaming_response: Mock,
        sample_workflow_id: str,
        sample_inputs: dict,
    ) -> None:
        """Test running a specific workflow in streaming mode."""
        mock_requests_request.return_value = mock_streaming_response

        client = WorkflowClient(api_key=mock_api_key)
        response = client.run_specific_workflow(
            workflow_id=sample_workflow_id,
            inputs=sample_inputs,
            response_mode="streaming",
        )

        # Verify streaming is enabled
        call_kwargs = mock_requests_request.call_args[1]
        assert call_kwargs["stream"] is True
        assert response == mock_streaming_response

    def test_run_specific_workflow_default_params(
        self,
        mock_api_key: str,
        mock_requests_request: Mock,
        mock_streaming_response: Mock,
        sample_workflow_id: str,
        sample_inputs: dict,
    ) -> None:
        """Test running a specific workflow with default parameters."""
        mock_requests_request.return_value = mock_streaming_response

        client = WorkflowClient(api_key=mock_api_key)
        response = client.run_specific_workflow(
            workflow_id=sample_workflow_id,
            inputs=sample_inputs,
        )

        # Verify defaults
        call_kwargs = mock_requests_request.call_args[1]
        assert call_kwargs["json"]["response_mode"] == "streaming"
        assert call_kwargs["json"]["user"] == "abc-123"
        assert response == mock_streaming_response
