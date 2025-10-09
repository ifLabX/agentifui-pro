"""
Tests for KnowledgeBaseClient.

This module tests the comprehensive KnowledgeBaseClient functionality including:
- Dataset management (create, list, delete)
- Document operations (create, update, delete, list)
- Segment management (add, query, update, delete)
- Advanced features (hit testing, metadata, tags, RAG pipeline)
"""

import json
from unittest.mock import Mock, mock_open, patch

import pytest
from dify_client import KnowledgeBaseClient


class TestKnowledgeBaseClientInitialization:
    """Test KnowledgeBaseClient initialization."""

    def test_client_initialization_with_dataset_id(
        self, mock_api_key: str, sample_dataset_id: str
    ) -> None:
        """Test client initialization with dataset ID."""
        client = KnowledgeBaseClient(
            api_key=mock_api_key, dataset_id=sample_dataset_id
        )

        assert client.api_key == mock_api_key
        assert client.dataset_id == sample_dataset_id
        assert client.base_url == "https://api.dify.ai/v1"

    def test_client_initialization_without_dataset_id(self, mock_api_key: str) -> None:
        """Test client initialization without dataset ID."""
        client = KnowledgeBaseClient(api_key=mock_api_key)

        assert client.api_key == mock_api_key
        assert client.dataset_id is None

    def test_client_initialization_with_custom_base_url(
        self, mock_api_key: str, mock_base_url: str
    ) -> None:
        """Test client initialization with custom base URL."""
        client = KnowledgeBaseClient(api_key=mock_api_key, base_url=mock_base_url)

        assert client.base_url == mock_base_url

    def test_get_dataset_id_raises_when_not_set(self, mock_api_key: str) -> None:
        """Test that _get_dataset_id raises error when dataset_id is None."""
        client = KnowledgeBaseClient(api_key=mock_api_key)

        with pytest.raises(ValueError) as exc_info:
            client._get_dataset_id()

        assert "dataset_id is not set" in str(exc_info.value)


class TestKnowledgeBaseClientDatasetManagement:
    """Test dataset management operations."""

    def test_create_dataset(
        self,
        mock_api_key: str,
        mock_requests_request: Mock,
        mock_successful_response: Mock,
    ) -> None:
        """Test creating a new dataset."""
        mock_requests_request.return_value = mock_successful_response

        client = KnowledgeBaseClient(api_key=mock_api_key)
        dataset_name = "Test Dataset"
        response = client.create_dataset(name=dataset_name)

        # Verify request
        mock_requests_request.assert_called_once()
        call_args, call_kwargs = mock_requests_request.call_args
        assert call_args[0] == "POST"
        assert "/datasets" in call_args[1]
        assert call_kwargs["json"]["name"] == dataset_name
        assert response == mock_successful_response

    def test_list_datasets_default(
        self,
        mock_api_key: str,
        mock_requests_request: Mock,
        mock_successful_response: Mock,
    ) -> None:
        """Test listing datasets with default parameters."""
        mock_requests_request.return_value = mock_successful_response

        client = KnowledgeBaseClient(api_key=mock_api_key)
        response = client.list_datasets()

        # Verify request
        call_args = mock_requests_request.call_args[0]
        assert call_args[0] == "GET"
        assert "/datasets?page=1&limit=20" in call_args[1]
        assert response == mock_successful_response

    def test_list_datasets_with_pagination(
        self,
        mock_api_key: str,
        mock_requests_request: Mock,
        mock_successful_response: Mock,
    ) -> None:
        """Test listing datasets with custom pagination."""
        mock_requests_request.return_value = mock_successful_response

        client = KnowledgeBaseClient(api_key=mock_api_key)
        response = client.list_datasets(page=3, page_size=50)

        # Verify pagination
        call_args = mock_requests_request.call_args[0]
        assert "/datasets?page=3&limit=50" in call_args[1]
        assert response == mock_successful_response

    def test_delete_dataset(
        self,
        mock_api_key: str,
        mock_requests_request: Mock,
        mock_successful_response: Mock,
        sample_dataset_id: str,
    ) -> None:
        """Test deleting a dataset."""
        mock_requests_request.return_value = mock_successful_response

        client = KnowledgeBaseClient(
            api_key=mock_api_key, dataset_id=sample_dataset_id
        )
        response = client.delete_dataset()

        # Verify request
        mock_requests_request.assert_called_once()
        call_args = mock_requests_request.call_args[0]
        assert call_args[0] == "DELETE"
        assert f"/datasets/{sample_dataset_id}" in call_args[1]
        assert response == mock_successful_response


class TestKnowledgeBaseClientDocumentByText:
    """Test document operations using text."""

    def test_create_document_by_text_minimal(
        self,
        mock_api_key: str,
        mock_requests_request: Mock,
        mock_successful_response: Mock,
        sample_dataset_id: str,
    ) -> None:
        """Test creating a document with minimal parameters."""
        mock_requests_request.return_value = mock_successful_response

        client = KnowledgeBaseClient(
            api_key=mock_api_key, dataset_id=sample_dataset_id
        )
        doc_name = "Test Document"
        doc_text = "This is test content"
        response = client.create_document_by_text(name=doc_name, text=doc_text)

        # Verify request
        mock_requests_request.assert_called_once()
        call_args, call_kwargs = mock_requests_request.call_args
        assert call_args[0] == "POST"
        assert f"/datasets/{sample_dataset_id}/document/create_by_text" in call_args[1]
        assert call_kwargs["json"]["name"] == doc_name
        assert call_kwargs["json"]["text"] == doc_text
        assert call_kwargs["json"]["indexing_technique"] == "high_quality"
        assert response == mock_successful_response

    def test_create_document_by_text_with_extra_params(
        self,
        mock_api_key: str,
        mock_requests_request: Mock,
        mock_successful_response: Mock,
        sample_dataset_id: str,
        sample_process_rule: dict,
    ) -> None:
        """Test creating a document with extra parameters."""
        mock_requests_request.return_value = mock_successful_response

        client = KnowledgeBaseClient(
            api_key=mock_api_key, dataset_id=sample_dataset_id
        )
        extra_params = {
            "indexing_technique": "economy",
            "process_rule": sample_process_rule,
        }
        response = client.create_document_by_text(
            name="Doc", text="Content", extra_params=extra_params
        )

        # Verify extra params are merged
        call_kwargs = mock_requests_request.call_args[1]
        assert call_kwargs["json"]["indexing_technique"] == "economy"
        assert call_kwargs["json"]["process_rule"] == sample_process_rule
        assert response == mock_successful_response

    def test_update_document_by_text(
        self,
        mock_api_key: str,
        mock_requests_request: Mock,
        mock_successful_response: Mock,
        sample_dataset_id: str,
        sample_document_id: str,
    ) -> None:
        """Test updating a document by text."""
        mock_requests_request.return_value = mock_successful_response

        client = KnowledgeBaseClient(
            api_key=mock_api_key, dataset_id=sample_dataset_id
        )
        new_name = "Updated Document"
        new_text = "Updated content"
        response = client.update_document_by_text(
            document_id=sample_document_id, name=new_name, text=new_text
        )

        # Verify request
        mock_requests_request.assert_called_once()
        call_args, call_kwargs = mock_requests_request.call_args
        assert call_args[0] == "POST"
        assert (
            f"/datasets/{sample_dataset_id}/documents/{sample_document_id}/update_by_text"
            in call_args[1]
        )
        assert call_kwargs["json"]["name"] == new_name
        assert call_kwargs["json"]["text"] == new_text
        assert response == mock_successful_response


class TestKnowledgeBaseClientDocumentByFile:
    """Test document operations using files."""

    @patch("builtins.open", new_callable=mock_open, read_data=b"file content")
    def test_create_document_by_file_minimal(
        self,
        mock_file: Mock,
        mock_api_key: str,
        mock_requests_request: Mock,
        mock_successful_response: Mock,
        sample_dataset_id: str,
    ) -> None:
        """Test creating a document from file with minimal parameters."""
        mock_requests_request.return_value = mock_successful_response

        client = KnowledgeBaseClient(
            api_key=mock_api_key, dataset_id=sample_dataset_id
        )
        file_path = "/tmp/test.txt"
        response = client.create_document_by_file(file_path=file_path)

        # Verify file was opened
        mock_file.assert_called_once_with(file_path, "rb")

        # Verify request
        mock_requests_request.assert_called_once()
        call_args, call_kwargs = mock_requests_request.call_args
        assert call_args[0] == "POST"
        assert f"/datasets/{sample_dataset_id}/document/create_by_file" in call_args[1]
        assert "data" in call_kwargs["data"]
        assert response == mock_successful_response

    @patch("builtins.open", new_callable=mock_open, read_data=b"file content")
    def test_create_document_by_file_with_original_document_id(
        self,
        mock_file: Mock,
        mock_api_key: str,
        mock_requests_request: Mock,
        mock_successful_response: Mock,
        sample_dataset_id: str,
    ) -> None:
        """Test creating a document from file with original document ID."""
        mock_requests_request.return_value = mock_successful_response

        client = KnowledgeBaseClient(
            api_key=mock_api_key, dataset_id=sample_dataset_id
        )
        original_doc_id = "doc-original-123"
        response = client.create_document_by_file(
            file_path="/tmp/test.txt", original_document_id=original_doc_id
        )

        # Verify original_document_id is included
        call_kwargs = mock_requests_request.call_args[1]
        data_json = json.loads(call_kwargs["data"]["data"])
        assert data_json["original_document_id"] == original_doc_id
        assert response == mock_successful_response

    @patch("builtins.open", new_callable=mock_open, read_data=b"file content")
    def test_update_document_by_file(
        self,
        mock_file: Mock,
        mock_api_key: str,
        mock_requests_request: Mock,
        mock_successful_response: Mock,
        sample_dataset_id: str,
        sample_document_id: str,
    ) -> None:
        """Test updating a document by file."""
        mock_requests_request.return_value = mock_successful_response

        client = KnowledgeBaseClient(
            api_key=mock_api_key, dataset_id=sample_dataset_id
        )
        file_path = "/tmp/updated.txt"
        response = client.update_document_by_file(
            document_id=sample_document_id, file_path=file_path
        )

        # Verify file was opened
        mock_file.assert_called_once_with(file_path, "rb")

        # Verify request
        call_args = mock_requests_request.call_args[0]
        assert call_args[0] == "POST"
        assert (
            f"/datasets/{sample_dataset_id}/documents/{sample_document_id}/update_by_file"
            in call_args[1]
        )
        assert response == mock_successful_response


class TestKnowledgeBaseClientDocumentOperations:
    """Test general document operations."""

    def test_list_documents_default(
        self,
        mock_api_key: str,
        mock_requests_request: Mock,
        mock_successful_response: Mock,
        sample_dataset_id: str,
    ) -> None:
        """Test listing documents with default parameters."""
        mock_requests_request.return_value = mock_successful_response

        client = KnowledgeBaseClient(
            api_key=mock_api_key, dataset_id=sample_dataset_id
        )
        response = client.list_documents()

        # Verify request
        mock_requests_request.assert_called_once()
        call_args, call_kwargs = mock_requests_request.call_args
        assert call_args[0] == "GET"
        assert f"/datasets/{sample_dataset_id}/documents" in call_args[1]
        assert call_kwargs["params"] == {}
        assert response == mock_successful_response

    def test_list_documents_with_pagination(
        self,
        mock_api_key: str,
        mock_requests_request: Mock,
        mock_successful_response: Mock,
        sample_dataset_id: str,
    ) -> None:
        """Test listing documents with pagination."""
        mock_requests_request.return_value = mock_successful_response

        client = KnowledgeBaseClient(
            api_key=mock_api_key, dataset_id=sample_dataset_id
        )
        response = client.list_documents(page=2, page_size=30)

        # Verify pagination
        call_kwargs = mock_requests_request.call_args[1]
        assert call_kwargs["params"]["page"] == 2
        assert call_kwargs["params"]["limit"] == 30
        assert response == mock_successful_response

    def test_list_documents_with_keyword(
        self,
        mock_api_key: str,
        mock_requests_request: Mock,
        mock_successful_response: Mock,
        sample_dataset_id: str,
    ) -> None:
        """Test listing documents with keyword filter."""
        mock_requests_request.return_value = mock_successful_response

        client = KnowledgeBaseClient(
            api_key=mock_api_key, dataset_id=sample_dataset_id
        )
        response = client.list_documents(keyword="important")

        # Verify keyword filter
        call_kwargs = mock_requests_request.call_args[1]
        assert call_kwargs["params"]["keyword"] == "important"
        assert response == mock_successful_response

    def test_delete_document(
        self,
        mock_api_key: str,
        mock_requests_request: Mock,
        mock_successful_response: Mock,
        sample_dataset_id: str,
        sample_document_id: str,
    ) -> None:
        """Test deleting a document."""
        mock_requests_request.return_value = mock_successful_response

        client = KnowledgeBaseClient(
            api_key=mock_api_key, dataset_id=sample_dataset_id
        )
        response = client.delete_document(document_id=sample_document_id)

        # Verify request
        mock_requests_request.assert_called_once()
        call_args = mock_requests_request.call_args[0]
        assert call_args[0] == "DELETE"
        assert (
            f"/datasets/{sample_dataset_id}/documents/{sample_document_id}"
            in call_args[1]
        )
        assert response == mock_successful_response

    def test_batch_indexing_status(
        self,
        mock_api_key: str,
        mock_requests_request: Mock,
        mock_successful_response: Mock,
        sample_dataset_id: str,
    ) -> None:
        """Test getting batch indexing status."""
        mock_requests_request.return_value = mock_successful_response

        client = KnowledgeBaseClient(
            api_key=mock_api_key, dataset_id=sample_dataset_id
        )
        batch_id = "batch-12345"
        response = client.batch_indexing_status(batch_id=batch_id)

        # Verify request
        call_args = mock_requests_request.call_args[0]
        assert call_args[0] == "GET"
        assert f"/datasets/{sample_dataset_id}/documents/{batch_id}/indexing-status" in call_args[1]
        assert response == mock_successful_response


class TestKnowledgeBaseClientSegmentOperations:
    """Test segment management operations."""

    def test_add_segments(
        self,
        mock_api_key: str,
        mock_requests_request: Mock,
        mock_successful_response: Mock,
        sample_dataset_id: str,
        sample_document_id: str,
        sample_segment_data: dict,
    ) -> None:
        """Test adding segments to a document."""
        mock_requests_request.return_value = mock_successful_response

        client = KnowledgeBaseClient(
            api_key=mock_api_key, dataset_id=sample_dataset_id
        )
        segments = [sample_segment_data]
        response = client.add_segments(
            document_id=sample_document_id, segments=segments
        )

        # Verify request
        mock_requests_request.assert_called_once()
        call_args, call_kwargs = mock_requests_request.call_args
        assert call_args[0] == "POST"
        assert (
            f"/datasets/{sample_dataset_id}/documents/{sample_document_id}/segments"
            in call_args[1]
        )
        assert call_kwargs["json"]["segments"] == segments
        assert response == mock_successful_response

    def test_query_segments_default(
        self,
        mock_api_key: str,
        mock_requests_request: Mock,
        mock_successful_response: Mock,
        sample_dataset_id: str,
        sample_document_id: str,
    ) -> None:
        """Test querying segments with default parameters."""
        mock_requests_request.return_value = mock_successful_response

        client = KnowledgeBaseClient(
            api_key=mock_api_key, dataset_id=sample_dataset_id
        )
        response = client.query_segments(document_id=sample_document_id)

        # Verify request
        call_args, call_kwargs = mock_requests_request.call_args
        assert call_args[0] == "GET"
        assert (
            f"/datasets/{sample_dataset_id}/documents/{sample_document_id}/segments"
            in call_args[1]
        )
        assert call_kwargs["params"] == {}
        assert response == mock_successful_response

    def test_query_segments_with_filters(
        self,
        mock_api_key: str,
        mock_requests_request: Mock,
        mock_successful_response: Mock,
        sample_dataset_id: str,
        sample_document_id: str,
    ) -> None:
        """Test querying segments with keyword and status filters."""
        mock_requests_request.return_value = mock_successful_response

        client = KnowledgeBaseClient(
            api_key=mock_api_key, dataset_id=sample_dataset_id
        )
        response = client.query_segments(
            document_id=sample_document_id, keyword="test", status="completed"
        )

        # Verify filters
        call_kwargs = mock_requests_request.call_args[1]
        assert call_kwargs["params"]["keyword"] == "test"
        assert call_kwargs["params"]["status"] == "completed"
        assert response == mock_successful_response

    def test_update_document_segment(
        self,
        mock_api_key: str,
        mock_requests_request: Mock,
        mock_successful_response: Mock,
        sample_dataset_id: str,
        sample_document_id: str,
    ) -> None:
        """Test updating a document segment."""
        mock_requests_request.return_value = mock_successful_response

        client = KnowledgeBaseClient(
            api_key=mock_api_key, dataset_id=sample_dataset_id
        )
        segment_id = "seg-123"
        segment_data = {
            "content": "Updated content",
            "enabled": True,
        }
        response = client.update_document_segment(
            document_id=sample_document_id,
            segment_id=segment_id,
            segment_data=segment_data,
        )

        # Verify request
        call_args, call_kwargs = mock_requests_request.call_args
        assert call_args[0] == "POST"
        assert (
            f"/datasets/{sample_dataset_id}/documents/{sample_document_id}/segments/{segment_id}"
            in call_args[1]
        )
        assert call_kwargs["json"]["segment"] == segment_data
        assert response == mock_successful_response

    def test_delete_document_segment(
        self,
        mock_api_key: str,
        mock_requests_request: Mock,
        mock_successful_response: Mock,
        sample_dataset_id: str,
        sample_document_id: str,
    ) -> None:
        """Test deleting a document segment."""
        mock_requests_request.return_value = mock_successful_response

        client = KnowledgeBaseClient(
            api_key=mock_api_key, dataset_id=sample_dataset_id
        )
        segment_id = "seg-456"
        response = client.delete_document_segment(
            document_id=sample_document_id, segment_id=segment_id
        )

        # Verify request
        call_args = mock_requests_request.call_args[0]
        assert call_args[0] == "DELETE"
        assert (
            f"/datasets/{sample_dataset_id}/documents/{sample_document_id}/segments/{segment_id}"
            in call_args[1]
        )
        assert response == mock_successful_response


class TestKnowledgeBaseClientAdvancedFeatures:
    """Test advanced knowledge base features."""

    def test_hit_testing_minimal(
        self,
        mock_api_key: str,
        mock_requests_request: Mock,
        mock_successful_response: Mock,
        sample_dataset_id: str,
    ) -> None:
        """Test hit testing with minimal parameters."""
        mock_requests_request.return_value = mock_successful_response

        client = KnowledgeBaseClient(
            api_key=mock_api_key, dataset_id=sample_dataset_id
        )
        query = "What is AI?"
        response = client.hit_testing(query=query)

        # Verify request
        call_args, call_kwargs = mock_requests_request.call_args
        assert call_args[0] == "POST"
        assert f"/datasets/{sample_dataset_id}/hit-testing" in call_args[1]
        assert call_kwargs["json"]["query"] == query
        assert response == mock_successful_response

    def test_hit_testing_with_retrieval_model(
        self,
        mock_api_key: str,
        mock_requests_request: Mock,
        mock_successful_response: Mock,
        sample_dataset_id: str,
        sample_retrieval_model: dict,
    ) -> None:
        """Test hit testing with retrieval model configuration."""
        mock_requests_request.return_value = mock_successful_response

        client = KnowledgeBaseClient(
            api_key=mock_api_key, dataset_id=sample_dataset_id
        )
        response = client.hit_testing(
            query="test", retrieval_model=sample_retrieval_model
        )

        # Verify retrieval model is included
        call_kwargs = mock_requests_request.call_args[1]
        assert call_kwargs["json"]["retrieval_model"] == sample_retrieval_model
        assert response == mock_successful_response


class TestKnowledgeBaseClientMetadataAPIs:
    """Test metadata management APIs."""

    def test_get_dataset_metadata(
        self,
        mock_api_key: str,
        mock_requests_request: Mock,
        mock_successful_response: Mock,
        sample_dataset_id: str,
    ) -> None:
        """Test getting dataset metadata."""
        mock_requests_request.return_value = mock_successful_response

        client = KnowledgeBaseClient(
            api_key=mock_api_key, dataset_id=sample_dataset_id
        )
        response = client.get_dataset_metadata()

        # Verify request
        call_args = mock_requests_request.call_args[0]
        assert call_args[0] == "GET"
        assert f"/datasets/{sample_dataset_id}/metadata" in call_args[1]
        assert response == mock_successful_response

    def test_create_dataset_metadata(
        self,
        mock_api_key: str,
        mock_requests_request: Mock,
        mock_successful_response: Mock,
        sample_dataset_id: str,
        sample_metadata: dict,
    ) -> None:
        """Test creating dataset metadata."""
        mock_requests_request.return_value = mock_successful_response

        client = KnowledgeBaseClient(
            api_key=mock_api_key, dataset_id=sample_dataset_id
        )
        response = client.create_dataset_metadata(metadata_data=sample_metadata)

        # Verify request
        call_args, call_kwargs = mock_requests_request.call_args
        assert call_args[0] == "POST"
        assert f"/datasets/{sample_dataset_id}/metadata" in call_args[1]
        assert call_kwargs["json"] == sample_metadata
        assert response == mock_successful_response

    def test_update_dataset_metadata(
        self,
        mock_api_key: str,
        mock_requests_request: Mock,
        mock_successful_response: Mock,
        sample_dataset_id: str,
        sample_metadata: dict,
    ) -> None:
        """Test updating dataset metadata."""
        mock_requests_request.return_value = mock_successful_response

        client = KnowledgeBaseClient(
            api_key=mock_api_key, dataset_id=sample_dataset_id
        )
        metadata_id = "meta-123"
        response = client.update_dataset_metadata(
            metadata_id=metadata_id, metadata_data=sample_metadata
        )

        # Verify request
        call_args, call_kwargs = mock_requests_request.call_args
        assert call_args[0] == "PATCH"
        assert f"/datasets/{sample_dataset_id}/metadata/{metadata_id}" in call_args[1]
        assert call_kwargs["json"] == sample_metadata
        assert response == mock_successful_response

    def test_get_built_in_metadata(
        self,
        mock_api_key: str,
        mock_requests_request: Mock,
        mock_successful_response: Mock,
        sample_dataset_id: str,
    ) -> None:
        """Test getting built-in metadata."""
        mock_requests_request.return_value = mock_successful_response

        client = KnowledgeBaseClient(
            api_key=mock_api_key, dataset_id=sample_dataset_id
        )
        response = client.get_built_in_metadata()

        # Verify request
        call_args = mock_requests_request.call_args[0]
        assert call_args[0] == "GET"
        assert f"/datasets/{sample_dataset_id}/metadata/built-in" in call_args[1]
        assert response == mock_successful_response

    def test_manage_built_in_metadata(
        self,
        mock_api_key: str,
        mock_requests_request: Mock,
        mock_successful_response: Mock,
        sample_dataset_id: str,
    ) -> None:
        """Test managing built-in metadata."""
        mock_requests_request.return_value = mock_successful_response

        client = KnowledgeBaseClient(
            api_key=mock_api_key, dataset_id=sample_dataset_id
        )
        action = "enable"
        metadata_data = {"field": "value"}
        response = client.manage_built_in_metadata(
            action=action, metadata_data=metadata_data
        )

        # Verify request
        call_args, call_kwargs = mock_requests_request.call_args
        assert call_args[0] == "POST"
        assert (
            f"/datasets/{sample_dataset_id}/metadata/built-in/{action}" in call_args[1]
        )
        assert call_kwargs["json"] == metadata_data
        assert response == mock_successful_response

    def test_update_documents_metadata(
        self,
        mock_api_key: str,
        mock_requests_request: Mock,
        mock_successful_response: Mock,
        sample_dataset_id: str,
    ) -> None:
        """Test updating metadata for multiple documents."""
        mock_requests_request.return_value = mock_successful_response

        client = KnowledgeBaseClient(
            api_key=mock_api_key, dataset_id=sample_dataset_id
        )
        operation_data = [
            {"document_id": "doc-1", "metadata": {"key": "value1"}},
            {"document_id": "doc-2", "metadata": {"key": "value2"}},
        ]
        response = client.update_documents_metadata(operation_data=operation_data)

        # Verify request
        call_args, call_kwargs = mock_requests_request.call_args
        assert call_args[0] == "POST"
        assert f"/datasets/{sample_dataset_id}/documents/metadata" in call_args[1]
        assert call_kwargs["json"]["operation_data"] == operation_data
        assert response == mock_successful_response


class TestKnowledgeBaseClientTagsAPIs:
    """Test dataset tags management APIs."""

    def test_list_dataset_tags(
        self,
        mock_api_key: str,
        mock_requests_request: Mock,
        mock_successful_response: Mock,
    ) -> None:
        """Test listing all dataset tags."""
        mock_requests_request.return_value = mock_successful_response

        client = KnowledgeBaseClient(api_key=mock_api_key)
        response = client.list_dataset_tags()

        # Verify request
        call_args = mock_requests_request.call_args[0]
        assert call_args[0] == "GET"
        assert "/datasets/tags" in call_args[1]
        assert response == mock_successful_response

    def test_bind_dataset_tags(
        self,
        mock_api_key: str,
        mock_requests_request: Mock,
        mock_successful_response: Mock,
        sample_dataset_id: str,
    ) -> None:
        """Test binding tags to dataset."""
        mock_requests_request.return_value = mock_successful_response

        client = KnowledgeBaseClient(
            api_key=mock_api_key, dataset_id=sample_dataset_id
        )
        tag_ids = ["tag-1", "tag-2", "tag-3"]
        response = client.bind_dataset_tags(tag_ids=tag_ids)

        # Verify request
        call_args, call_kwargs = mock_requests_request.call_args
        assert call_args[0] == "POST"
        assert "/datasets/tags/binding" in call_args[1]
        assert call_kwargs["json"]["tag_ids"] == tag_ids
        assert call_kwargs["json"]["target_id"] == sample_dataset_id
        assert response == mock_successful_response

    def test_unbind_dataset_tag(
        self,
        mock_api_key: str,
        mock_requests_request: Mock,
        mock_successful_response: Mock,
        sample_dataset_id: str,
    ) -> None:
        """Test unbinding a single tag from dataset."""
        mock_requests_request.return_value = mock_successful_response

        client = KnowledgeBaseClient(
            api_key=mock_api_key, dataset_id=sample_dataset_id
        )
        tag_id = "tag-to-remove"
        response = client.unbind_dataset_tag(tag_id=tag_id)

        # Verify request
        call_args, call_kwargs = mock_requests_request.call_args
        assert call_args[0] == "POST"
        assert "/datasets/tags/unbinding" in call_args[1]
        assert call_kwargs["json"]["tag_id"] == tag_id
        assert call_kwargs["json"]["target_id"] == sample_dataset_id
        assert response == mock_successful_response

    def test_get_dataset_tags(
        self,
        mock_api_key: str,
        mock_requests_request: Mock,
        mock_successful_response: Mock,
        sample_dataset_id: str,
    ) -> None:
        """Test getting tags for current dataset."""
        mock_requests_request.return_value = mock_successful_response

        client = KnowledgeBaseClient(
            api_key=mock_api_key, dataset_id=sample_dataset_id
        )
        response = client.get_dataset_tags()

        # Verify request
        call_args = mock_requests_request.call_args[0]
        assert call_args[0] == "GET"
        assert f"/datasets/{sample_dataset_id}/tags" in call_args[1]
        assert response == mock_successful_response


class TestKnowledgeBaseClientRAGPipelineAPIs:
    """Test RAG pipeline APIs."""

    def test_get_datasource_plugins(
        self,
        mock_api_key: str,
        mock_requests_request: Mock,
        mock_successful_response: Mock,
        sample_dataset_id: str,
    ) -> None:
        """Test getting datasource plugins."""
        mock_requests_request.return_value = mock_successful_response

        client = KnowledgeBaseClient(
            api_key=mock_api_key, dataset_id=sample_dataset_id
        )
        response = client.get_datasource_plugins(is_published=True)

        # Verify request
        call_args, call_kwargs = mock_requests_request.call_args
        assert call_args[0] == "GET"
        assert (
            f"/datasets/{sample_dataset_id}/pipeline/datasource-plugins"
            in call_args[1]
        )
        assert call_kwargs["params"]["is_published"] is True
        assert response == mock_successful_response

    def test_run_datasource_node(
        self,
        mock_api_key: str,
        mock_requests_request: Mock,
        mock_streaming_response: Mock,
        sample_dataset_id: str,
    ) -> None:
        """Test running a datasource node."""
        mock_requests_request.return_value = mock_streaming_response

        client = KnowledgeBaseClient(
            api_key=mock_api_key, dataset_id=sample_dataset_id
        )
        node_id = "node-123"
        inputs = {"query": "test"}
        datasource_type = "external"
        response = client.run_datasource_node(
            node_id=node_id, inputs=inputs, datasource_type=datasource_type
        )

        # Verify request
        call_args, call_kwargs = mock_requests_request.call_args
        assert call_args[0] == "POST"
        assert (
            f"/datasets/{sample_dataset_id}/pipeline/datasource/nodes/{node_id}/run"
            in call_args[1]
        )
        assert call_kwargs["json"]["inputs"] == inputs
        assert call_kwargs["json"]["datasource_type"] == datasource_type
        assert call_kwargs["stream"] is True
        assert response == mock_streaming_response

    def test_run_rag_pipeline_blocking(
        self,
        mock_api_key: str,
        mock_requests_request: Mock,
        mock_successful_response: Mock,
        sample_dataset_id: str,
        sample_rag_pipeline_data: dict,
    ) -> None:
        """Test running RAG pipeline in blocking mode."""
        mock_requests_request.return_value = mock_successful_response

        client = KnowledgeBaseClient(
            api_key=mock_api_key, dataset_id=sample_dataset_id
        )
        response = client.run_rag_pipeline(
            inputs=sample_rag_pipeline_data["inputs"],
            datasource_type=sample_rag_pipeline_data["datasource_type"],
            datasource_info_list=sample_rag_pipeline_data["datasource_info_list"],
            start_node_id=sample_rag_pipeline_data["start_node_id"],
            response_mode="blocking",
        )

        # Verify request
        call_args, call_kwargs = mock_requests_request.call_args
        assert call_args[0] == "POST"
        assert f"/datasets/{sample_dataset_id}/pipeline/run" in call_args[1]
        assert call_kwargs["json"]["response_mode"] == "blocking"
        assert call_kwargs["stream"] is False
        assert response == mock_successful_response

    def test_run_rag_pipeline_streaming(
        self,
        mock_api_key: str,
        mock_requests_request: Mock,
        mock_streaming_response: Mock,
        sample_dataset_id: str,
        sample_rag_pipeline_data: dict,
    ) -> None:
        """Test running RAG pipeline in streaming mode."""
        mock_requests_request.return_value = mock_streaming_response

        client = KnowledgeBaseClient(
            api_key=mock_api_key, dataset_id=sample_dataset_id
        )
        response = client.run_rag_pipeline(
            inputs=sample_rag_pipeline_data["inputs"],
            datasource_type=sample_rag_pipeline_data["datasource_type"],
            datasource_info_list=sample_rag_pipeline_data["datasource_info_list"],
            start_node_id=sample_rag_pipeline_data["start_node_id"],
            response_mode="streaming",
        )

        # Verify streaming
        call_kwargs = mock_requests_request.call_args[1]
        assert call_kwargs["stream"] is True
        assert response == mock_streaming_response

    @patch("builtins.open", new_callable=mock_open, read_data=b"file content")
    def test_upload_pipeline_file(
        self,
        mock_file: Mock,
        mock_api_key: str,
        mock_requests_request: Mock,
        mock_successful_response: Mock,
    ) -> None:
        """Test uploading file for RAG pipeline."""
        mock_requests_request.return_value = mock_successful_response

        client = KnowledgeBaseClient(api_key=mock_api_key)
        file_path = "/tmp/pipeline_file.txt"
        response = client.upload_pipeline_file(file_path=file_path)

        # Verify file was opened
        mock_file.assert_called_once_with(file_path, "rb")

        # Verify request
        call_args = mock_requests_request.call_args[0]
        assert call_args[0] == "POST"
        assert "/datasets/pipeline/file-upload" in call_args[1]
        assert response == mock_successful_response
