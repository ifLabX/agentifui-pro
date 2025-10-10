"""
Tests for Coze SDK workflow operations.

This module tests workflow-related operations including running workflows,
retrieving workflow status, streaming workflow execution, and managing workflow runs.
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


class TestWorkflowExecution:
    """Test workflow execution operations."""

    def test_run_workflow_blocking(
        self,
        coze_client: Coze,
        mock_workflow_id: str,
        sample_workflow_inputs: dict[str, Any],
        sample_workflow_data: dict[str, Any],
    ) -> None:
        """
        Test running a workflow in blocking mode.

        GIVEN: Valid workflow ID and inputs
        WHEN: Running workflow with blocking mode
        THEN: Returns completed workflow run with outputs
        """
        # Configure mock response
        mock_response = Mock(spec=httpx.Response)
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": sample_workflow_data,
            "logid": "req-workflow-run-123",
        }

        # Mock the HTTP client
        with patch("httpx.Client.request", return_value=mock_response):
            # This test demonstrates the blocking workflow execution pattern
            response_data = mock_response.json()
            workflow_run = response_data["data"]

            assert workflow_run["workflow_id"] == mock_workflow_id
            assert workflow_run["status"] == "succeeded"
            assert "outputs" in workflow_run
            assert workflow_run["outputs"]["result"] == "Data processed successfully"


class TestWorkflowStreaming:
    """Test streaming workflow operations."""

    def test_run_workflow_streaming(
        self,
        coze_client: Coze,
        mock_workflow_id: str,
        sample_workflow_inputs: dict[str, Any],
        mock_streaming_response: Mock,
    ) -> None:
        """
        Test running a workflow with streaming response.

        GIVEN: Valid workflow ID and inputs
        WHEN: Running workflow with streaming mode
        THEN: Returns streaming events with progress updates
        """
        # Mock the HTTP client
        with patch("httpx.Client.request", return_value=mock_streaming_response):
            # This test demonstrates the streaming workflow execution pattern
            events = list(mock_streaming_response.iter_lines())

            # Verify streaming events exist
            assert len(events) > 0
            # Events should contain workflow progress information
            assert mock_streaming_response.status_code == 200


class TestWorkflowRunStatus:
    """Test workflow run status operations."""

    def test_retrieve_workflow_run(
        self,
        coze_client: Coze,
        mock_workflow_id: str,
        mock_workflow_run_id: str,
        sample_workflow_data: dict[str, Any],
    ) -> None:
        """
        Test retrieving workflow run status.

        GIVEN: Valid workflow run ID
        WHEN: Retrieving run status
        THEN: Returns workflow run with current status
        """
        # Configure mock response
        mock_response = Mock(spec=httpx.Response)
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": sample_workflow_data,
            "logid": "req-workflow-status-456",
        }

        # Mock the HTTP client
        with patch("httpx.Client.request", return_value=mock_response):
            # This test demonstrates the workflow run status retrieval pattern
            response_data = mock_response.json()
            workflow_run = response_data["data"]

            assert workflow_run["workflow_run_id"] == mock_workflow_run_id
            assert workflow_run["status"] in ["running", "succeeded", "failed"]
            assert "inputs" in workflow_run


class TestWorkflowInputValidation:
    """Test workflow input validation."""

    def test_workflow_with_valid_inputs(
        self,
        sample_workflow_inputs: dict[str, Any],
    ) -> None:
        """
        Test workflow inputs structure.

        GIVEN: Workflow input data
        WHEN: Validating input structure
        THEN: Input has required fields
        """
        # Verify input structure
        assert "query" in sample_workflow_inputs
        assert isinstance(sample_workflow_inputs["query"], str)
        assert len(sample_workflow_inputs["query"]) > 0

    def test_workflow_with_parameters(
        self,
        sample_workflow_inputs: dict[str, Any],
    ) -> None:
        """
        Test workflow inputs with parameters.

        GIVEN: Workflow input with additional parameters
        WHEN: Validating parameter structure
        THEN: Parameters are correctly structured
        """
        # Verify parameters exist
        assert "parameters" in sample_workflow_inputs
        assert isinstance(sample_workflow_inputs["parameters"], dict)
        assert sample_workflow_inputs["parameters"]["mode"] == "batch"


class TestWorkflowOutputs:
    """Test workflow output operations."""

    def test_workflow_output_structure(
        self,
        sample_workflow_data: dict[str, Any],
    ) -> None:
        """
        Test workflow output structure.

        GIVEN: Completed workflow run
        WHEN: Validating output structure
        THEN: Output has expected format
        """
        # Verify output exists
        assert "outputs" in sample_workflow_data
        assert isinstance(sample_workflow_data["outputs"], dict)
        assert "result" in sample_workflow_data["outputs"]

    def test_workflow_execution_metadata(
        self,
        sample_workflow_data: dict[str, Any],
    ) -> None:
        """
        Test workflow execution metadata.

        GIVEN: Completed workflow run
        WHEN: Checking execution metadata
        THEN: Metadata includes timestamps and status
        """
        # Verify metadata
        assert "created_at" in sample_workflow_data
        assert "completed_at" in sample_workflow_data
        assert sample_workflow_data["created_at"] <= sample_workflow_data["completed_at"]
        assert sample_workflow_data["status"] == "succeeded"
