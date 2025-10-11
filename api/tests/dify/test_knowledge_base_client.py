"""
Tests for AsyncKnowledgeBaseClient.

This module tests the comprehensive AsyncKnowledgeBaseClient functionality including:
- Dataset management (create, list, delete)
- Document operations (create, update, delete, list)
- Segment management (add, query, update, delete)
- Advanced features (hit testing, metadata, tags, RAG pipeline)
"""

import json
import re
from unittest.mock import mock_open, patch

import pytest
from dify_client.async_client import AsyncKnowledgeBaseClient
from pytest_httpx import HTTPXMock


class TestKnowledgeBaseClientInitialization:
    """Test AsyncKnowledgeBaseClient initialization."""

    async def test_client_initialization_with_dataset_id(self, mock_api_key: str, sample_dataset_id: str) -> None:
        """Test client initialization with dataset ID."""
        client = AsyncKnowledgeBaseClient(api_key=mock_api_key, dataset_id=sample_dataset_id)

        assert client.api_key == mock_api_key
        assert client.dataset_id == sample_dataset_id
        assert client.base_url == "https://api.dify.ai/v1"

    async def test_client_initialization_without_dataset_id(self, mock_api_key: str) -> None:
        """Test client initialization without dataset ID."""
        client = AsyncKnowledgeBaseClient(api_key=mock_api_key)

        assert client.api_key == mock_api_key
        assert client.dataset_id is None

    async def test_client_initialization_with_custom_base_url(self, mock_api_key: str, mock_base_url: str) -> None:
        """Test client initialization with custom base URL."""
        client = AsyncKnowledgeBaseClient(api_key=mock_api_key, base_url=mock_base_url)

        assert client.base_url == mock_base_url

    async def test_get_dataset_id_raises_when_not_set(self, mock_api_key: str) -> None:
        """Test that _get_dataset_id raises error when dataset_id is None."""
        client = AsyncKnowledgeBaseClient(api_key=mock_api_key)

        with pytest.raises(ValueError) as exc_info:
            client._get_dataset_id()

        assert "dataset_id is not set" in str(exc_info.value)


class TestKnowledgeBaseClientDatasetManagement:
    """Test dataset management operations."""

    async def test_create_dataset(
        self,
        httpx_mock: HTTPXMock,
        mock_api_key: str,
    ) -> None:
        """Test creating a new dataset."""
        httpx_mock.add_response(
            url="https://api.dify.ai/v1/datasets",
            method="POST",
            json={"id": "dataset-123", "name": "Test Dataset"},
            status_code=200,
        )

        client = AsyncKnowledgeBaseClient(api_key=mock_api_key)
        dataset_name = "Test Dataset"
        response = await client.create_dataset(name=dataset_name)

        # Verify request
        requests = httpx_mock.get_requests()
        assert len(requests) == 1
        assert requests[0].method == "POST"
        assert str(requests[0].url) == "https://api.dify.ai/v1/datasets"
        request_json = json.loads(requests[0].content)
        assert request_json["name"] == dataset_name
        assert response.status_code == 200

    async def test_list_datasets_default(
        self,
        httpx_mock: HTTPXMock,
        mock_api_key: str,
    ) -> None:
        """Test listing datasets with default parameters."""
        httpx_mock.add_response(
            url="https://api.dify.ai/v1/datasets?page=1&limit=20",
            method="GET",
            json={"data": []},
            status_code=200,
        )

        client = AsyncKnowledgeBaseClient(api_key=mock_api_key)
        response = await client.list_datasets()

        # Verify request
        requests = httpx_mock.get_requests()
        assert len(requests) == 1
        assert requests[0].method == "GET"
        assert "datasets?page=1&limit=20" in str(requests[0].url)
        assert response.status_code == 200

    async def test_list_datasets_with_pagination(
        self,
        httpx_mock: HTTPXMock,
        mock_api_key: str,
    ) -> None:
        """Test listing datasets with custom pagination."""
        httpx_mock.add_response(
            url="https://api.dify.ai/v1/datasets?page=3&limit=50",
            method="GET",
            json={"data": []},
            status_code=200,
        )

        client = AsyncKnowledgeBaseClient(api_key=mock_api_key)
        response = await client.list_datasets(page=3, page_size=50)

        # Verify pagination
        requests = httpx_mock.get_requests()
        assert len(requests) == 1
        assert "datasets?page=3&limit=50" in str(requests[0].url)
        assert response.status_code == 200

    async def test_delete_dataset(
        self,
        httpx_mock: HTTPXMock,
        mock_api_key: str,
        sample_dataset_id: str,
    ) -> None:
        """Test deleting a dataset."""
        httpx_mock.add_response(
            url=f"https://api.dify.ai/v1/datasets/{sample_dataset_id}",
            method="DELETE",
            json={"result": "success"},
            status_code=200,
        )

        client = AsyncKnowledgeBaseClient(api_key=mock_api_key, dataset_id=sample_dataset_id)
        response = await client.delete_dataset()

        # Verify request
        requests = httpx_mock.get_requests()
        assert len(requests) == 1
        assert requests[0].method == "DELETE"
        assert f"/datasets/{sample_dataset_id}" in str(requests[0].url)
        assert response.status_code == 200


class TestKnowledgeBaseClientDocumentByText:
    """Test document operations using text."""

    async def test_create_document_by_text_minimal(
        self,
        httpx_mock: HTTPXMock,
        mock_api_key: str,
        sample_dataset_id: str,
    ) -> None:
        """Test creating a document with minimal parameters."""
        httpx_mock.add_response(
            url=f"https://api.dify.ai/v1/datasets/{sample_dataset_id}/document/create_by_text",
            method="POST",
            json={"document": {"id": "doc-123"}},
            status_code=200,
        )

        client = AsyncKnowledgeBaseClient(api_key=mock_api_key, dataset_id=sample_dataset_id)
        doc_name = "Test Document"
        doc_text = "This is test content"
        response = await client.create_document_by_text(name=doc_name, text=doc_text)

        # Verify request
        requests = httpx_mock.get_requests()
        assert len(requests) == 1
        assert requests[0].method == "POST"
        assert f"/datasets/{sample_dataset_id}/document/create_by_text" in str(requests[0].url)
        request_json = json.loads(requests[0].content)
        assert request_json["name"] == doc_name
        assert request_json["text"] == doc_text
        assert request_json["indexing_technique"] == "high_quality"
        assert response.status_code == 200

    async def test_create_document_by_text_with_extra_params(
        self,
        httpx_mock: HTTPXMock,
        mock_api_key: str,
        sample_dataset_id: str,
        sample_process_rule: dict,
    ) -> None:
        """Test creating a document with extra parameters."""
        httpx_mock.add_response(
            url=f"https://api.dify.ai/v1/datasets/{sample_dataset_id}/document/create_by_text",
            method="POST",
            json={"document": {"id": "doc-123"}},
            status_code=200,
        )

        client = AsyncKnowledgeBaseClient(api_key=mock_api_key, dataset_id=sample_dataset_id)
        extra_params = {
            "indexing_technique": "economy",
            "process_rule": sample_process_rule,
        }
        response = await client.create_document_by_text(name="Doc", text="Content", extra_params=extra_params)

        # Verify extra params are merged
        requests = httpx_mock.get_requests()
        request_json = json.loads(requests[0].content)
        assert request_json["indexing_technique"] == "economy"
        assert request_json["process_rule"] == sample_process_rule
        assert response.status_code == 200

    async def test_update_document_by_text(
        self,
        httpx_mock: HTTPXMock,
        mock_api_key: str,
        sample_dataset_id: str,
        sample_document_id: str,
    ) -> None:
        """Test updating a document by text."""
        httpx_mock.add_response(
            url=f"https://api.dify.ai/v1/datasets/{sample_dataset_id}/documents/{sample_document_id}/update_by_text",
            method="POST",
            json={"document": {"id": sample_document_id}},
            status_code=200,
        )

        client = AsyncKnowledgeBaseClient(api_key=mock_api_key, dataset_id=sample_dataset_id)
        new_name = "Updated Document"
        new_text = "Updated content"
        response = await client.update_document_by_text(document_id=sample_document_id, name=new_name, text=new_text)

        # Verify request
        requests = httpx_mock.get_requests()
        assert len(requests) == 1
        assert requests[0].method == "POST"
        assert f"/datasets/{sample_dataset_id}/documents/{sample_document_id}/update_by_text" in str(requests[0].url)
        request_json = json.loads(requests[0].content)
        assert request_json["name"] == new_name
        assert request_json["text"] == new_text
        assert response.status_code == 200


class TestKnowledgeBaseClientDocumentByFile:
    """Test document operations using files."""

    @patch("builtins.open", new_callable=mock_open, read_data=b"file content")
    async def test_create_document_by_file_minimal(
        self,
        mock_file,
        httpx_mock: HTTPXMock,
        mock_api_key: str,
        sample_dataset_id: str,
    ) -> None:
        """Test creating a document from file with minimal parameters."""
        httpx_mock.add_response(
            url=f"https://api.dify.ai/v1/datasets/{sample_dataset_id}/document/create_by_file",
            method="POST",
            json={"document": {"id": "doc-123"}},
            status_code=200,
        )

        client = AsyncKnowledgeBaseClient(api_key=mock_api_key, dataset_id=sample_dataset_id)
        file_path = "/tmp/test.txt"
        response = await client.create_document_by_file(file_path=file_path)

        # Verify file was opened
        mock_file.assert_called_once_with(file_path, "rb")

        # Verify request
        requests = httpx_mock.get_requests()
        assert len(requests) == 1
        assert requests[0].method == "POST"
        assert f"/datasets/{sample_dataset_id}/document/create_by_file" in str(requests[0].url)
        assert response.status_code == 200

    @patch("builtins.open", new_callable=mock_open, read_data=b"file content")
    async def test_create_document_by_file_with_original_document_id(
        self,
        mock_file,
        httpx_mock: HTTPXMock,
        mock_api_key: str,
        sample_dataset_id: str,
    ) -> None:
        """Test creating a document from file with original document ID."""
        httpx_mock.add_response(
            url=f"https://api.dify.ai/v1/datasets/{sample_dataset_id}/document/create_by_file",
            method="POST",
            json={"document": {"id": "doc-123"}},
            status_code=200,
        )

        client = AsyncKnowledgeBaseClient(api_key=mock_api_key, dataset_id=sample_dataset_id)
        original_doc_id = "doc-original-123"
        response = await client.create_document_by_file(file_path="/tmp/test.txt", original_document_id=original_doc_id)

        # Verify request
        requests = httpx_mock.get_requests()
        assert len(requests) == 1
        assert response.status_code == 200

    @patch("builtins.open", new_callable=mock_open, read_data=b"file content")
    async def test_update_document_by_file(
        self,
        mock_file,
        httpx_mock: HTTPXMock,
        mock_api_key: str,
        sample_dataset_id: str,
        sample_document_id: str,
    ) -> None:
        """Test updating a document by file."""
        httpx_mock.add_response(
            url=f"https://api.dify.ai/v1/datasets/{sample_dataset_id}/documents/{sample_document_id}/update_by_file",
            method="POST",
            json={"document": {"id": sample_document_id}},
            status_code=200,
        )

        client = AsyncKnowledgeBaseClient(api_key=mock_api_key, dataset_id=sample_dataset_id)
        file_path = "/tmp/updated.txt"
        response = await client.update_document_by_file(document_id=sample_document_id, file_path=file_path)

        # Verify file was opened
        mock_file.assert_called_once_with(file_path, "rb")

        # Verify request
        requests = httpx_mock.get_requests()
        assert len(requests) == 1
        assert requests[0].method == "POST"
        assert f"/datasets/{sample_dataset_id}/documents/{sample_document_id}/update_by_file" in str(requests[0].url)
        assert response.status_code == 200


class TestKnowledgeBaseClientDocumentOperations:
    """Test general document operations."""

    async def test_list_documents_default(
        self,
        httpx_mock: HTTPXMock,
        mock_api_key: str,
        sample_dataset_id: str) -> None:
        """Test listing documents with default parameters."""
        httpx_mock.add_response(
            url=re.compile(rf"https://api\.dify\.ai/v1/datasets/{re.escape(sample_dataset_id)}/documents.*"),
            method="GET",
            json={"data": []},
            status_code=200,
        )

        client = AsyncKnowledgeBaseClient(api_key=mock_api_key, dataset_id=sample_dataset_id)
        response = await client.list_documents()

        # Verify request
        requests = httpx_mock.get_requests()
        assert len(requests) == 1
        assert requests[0].method == "GET"
        assert response.status_code == 200

    async def test_list_documents_with_pagination(
        self,
        httpx_mock: HTTPXMock,
        mock_api_key: str,
        sample_dataset_id: str) -> None:
        """Test listing documents with pagination."""
        httpx_mock.add_response(
            url=re.compile(rf"https://api\.dify\.ai/v1/datasets/{re.escape(sample_dataset_id)}/documents.*"),
            method="GET",
            json={"data": []},
            status_code=200,
        )

        client = AsyncKnowledgeBaseClient(api_key=mock_api_key, dataset_id=sample_dataset_id)
        response = await client.list_documents(page=2, page_size=30)

        # Verify pagination
        requests = httpx_mock.get_requests()
        assert len(requests) == 1
        assert requests[0].method == "GET"
        assert "page=2" in str(requests[0].url)
        assert "limit=30" in str(requests[0].url)
        assert response.status_code == 200

    async def test_list_documents_with_keyword(
        self,
        httpx_mock: HTTPXMock,
        mock_api_key: str,
        sample_dataset_id: str) -> None:
        """Test listing documents with keyword filter."""
        httpx_mock.add_response(
            url=re.compile(rf"https://api\.dify\.ai/v1/datasets/{re.escape(sample_dataset_id)}/documents.*"),
            method="GET",
            json={"data": []},
            status_code=200,
        )

        client = AsyncKnowledgeBaseClient(api_key=mock_api_key, dataset_id=sample_dataset_id)
        response = await client.list_documents(keyword="important")

        # Verify keyword filter
        requests = httpx_mock.get_requests()
        assert len(requests) == 1
        assert requests[0].method == "GET"
        assert "keyword=important" in str(requests[0].url)
        assert response.status_code == 200

    async def test_delete_document(
        self,
        httpx_mock: HTTPXMock,
        mock_api_key: str,
        sample_dataset_id: str,
        sample_document_id: str) -> None:
        """Test deleting a document."""
        httpx_mock.add_response(
            url=f"https://api.dify.ai/v1/datasets/{sample_dataset_id}/documents/{sample_document_id}",
            method="DELETE",
            json={"result": "success"},
            status_code=200,
        )

        client = AsyncKnowledgeBaseClient(api_key=mock_api_key, dataset_id=sample_dataset_id)
        response = await client.delete_document(document_id=sample_document_id)

        # Verify request
        requests = httpx_mock.get_requests()
        assert len(requests) == 1
        assert requests[0].method == "DELETE"
        assert response.status_code == 200

    async def test_batch_indexing_status(
        self,
        httpx_mock: HTTPXMock,
        mock_api_key: str,
        sample_dataset_id: str) -> None:
        """Test getting batch indexing status."""
        batch_id = "batch-12345"
        httpx_mock.add_response(
            url=f"https://api.dify.ai/v1/datasets/{sample_dataset_id}/documents/{batch_id}/indexing-status",
            method="GET",
            json={"status": "processing"},
            status_code=200,
        )

        client = AsyncKnowledgeBaseClient(api_key=mock_api_key, dataset_id=sample_dataset_id)
        response = await client.batch_indexing_status(batch_id=batch_id)

        # Verify request
        requests = httpx_mock.get_requests()
        assert len(requests) == 1
        assert requests[0].method == "GET"
        assert response.status_code == 200


class TestKnowledgeBaseClientSegmentOperations:
    """Test segment management operations."""

    async def test_add_segments(
        self,
        httpx_mock: HTTPXMock,
        mock_api_key: str,
        sample_dataset_id: str,
        sample_document_id: str,
        sample_segment_data: dict) -> None:
        """Test adding segments to a document."""
        httpx_mock.add_response(
            url=f"https://api.dify.ai/v1/datasets/{sample_dataset_id}/documents/{sample_document_id}/segments",
            method="POST",
            json={"data": [{"id": "seg-123"}]},
            status_code=200,
        )

        client = AsyncKnowledgeBaseClient(api_key=mock_api_key, dataset_id=sample_dataset_id)
        segments = [sample_segment_data]
        response = await client.add_segments(document_id=sample_document_id, segments=segments)

        # Verify request
        requests = httpx_mock.get_requests()
        assert len(requests) == 1
        assert requests[0].method == "POST"
        assert response.status_code == 200

    async def test_query_segments_default(
        self,
        httpx_mock: HTTPXMock,
        mock_api_key: str,
        sample_dataset_id: str,
        sample_document_id: str) -> None:
        """Test querying segments with default parameters."""
        httpx_mock.add_response(
            url=re.compile(rf"https://api\.dify\.ai/v1/datasets/{re.escape(sample_dataset_id)}/documents/{re.escape(sample_document_id)}/segments.*"),
            method="GET",
            json={"data": []},
            status_code=200,
        )

        client = AsyncKnowledgeBaseClient(api_key=mock_api_key, dataset_id=sample_dataset_id)
        response = await client.query_segments(document_id=sample_document_id)

        # Verify request
        requests = httpx_mock.get_requests()
        assert len(requests) == 1
        assert requests[0].method == "GET"
        assert response.status_code == 200

    async def test_query_segments_with_filters(
        self,
        httpx_mock: HTTPXMock,
        mock_api_key: str,
        sample_dataset_id: str,
        sample_document_id: str) -> None:
        """Test querying segments with keyword and status filters."""
        httpx_mock.add_response(
            url=re.compile(rf"https://api\.dify\.ai/v1/datasets/{re.escape(sample_dataset_id)}/documents/{re.escape(sample_document_id)}/segments.*"),
            method="GET",
            json={"data": []},
            status_code=200,
        )

        client = AsyncKnowledgeBaseClient(api_key=mock_api_key, dataset_id=sample_dataset_id)
        response = await client.query_segments(document_id=sample_document_id, keyword="test", status="completed")

        # Verify filters
        requests = httpx_mock.get_requests()
        assert len(requests) == 1
        assert requests[0].method == "GET"
        assert "keyword=test" in str(requests[0].url)
        assert "status=completed" in str(requests[0].url)
        assert response.status_code == 200

    async def test_update_document_segment(
        self,
        httpx_mock: HTTPXMock,
        mock_api_key: str,
        sample_dataset_id: str,
        sample_document_id: str) -> None:
        """Test updating a document segment."""
        segment_id = "seg-123"
        httpx_mock.add_response(
            url=f"https://api.dify.ai/v1/datasets/{sample_dataset_id}/documents/{sample_document_id}/segments/{segment_id}",
            method="POST",
            json={"segment": {"id": segment_id}},
            status_code=200,
        )

        client = AsyncKnowledgeBaseClient(api_key=mock_api_key, dataset_id=sample_dataset_id)
        segment_data = {
            "content": "Updated content",
            "enabled": True,
        }
        response = await client.update_document_segment(
            document_id=sample_document_id,
            segment_id=segment_id,
            segment_data=segment_data,
        )

        # Verify request
        requests = httpx_mock.get_requests()
        assert len(requests) == 1
        assert requests[0].method == "POST"
        assert response.status_code == 200

    async def test_delete_document_segment(
        self,
        httpx_mock: HTTPXMock,
        mock_api_key: str,
        sample_dataset_id: str,
        sample_document_id: str) -> None:
        """Test deleting a document segment."""
        segment_id = "seg-456"
        httpx_mock.add_response(
            url=f"https://api.dify.ai/v1/datasets/{sample_dataset_id}/documents/{sample_document_id}/segments/{segment_id}",
            method="DELETE",
            json={"result": "success"},
            status_code=200,
        )

        client = AsyncKnowledgeBaseClient(api_key=mock_api_key, dataset_id=sample_dataset_id)
        response = await client.delete_document_segment(document_id=sample_document_id, segment_id=segment_id)

        # Verify request
        requests = httpx_mock.get_requests()
        assert len(requests) == 1
        assert requests[0].method == "DELETE"
        assert response.status_code == 200


class TestKnowledgeBaseClientAdvancedFeatures:
    """Test advanced knowledge base features."""

    async def test_hit_testing_minimal(
        self,
        httpx_mock: HTTPXMock,
        mock_api_key: str,
        sample_dataset_id: str) -> None:
        """Test hit testing with minimal parameters."""
        httpx_mock.add_response(
            url=f"https://api.dify.ai/v1/datasets/{sample_dataset_id}/hit-testing",
            method="POST",
            json={"records": []},
            status_code=200,
        )

        client = AsyncKnowledgeBaseClient(api_key=mock_api_key, dataset_id=sample_dataset_id)
        query = "What is AI?"
        response = await client.hit_testing(query=query)

        # Verify request
        requests = httpx_mock.get_requests()
        assert len(requests) == 1
        assert requests[0].method == "POST"
        assert response.status_code == 200

    async def test_hit_testing_with_retrieval_model(
        self,
        httpx_mock: HTTPXMock,
        mock_api_key: str,
        sample_dataset_id: str,
        sample_retrieval_model: dict) -> None:
        """Test hit testing with retrieval model configuration."""
        httpx_mock.add_response(
            url=f"https://api.dify.ai/v1/datasets/{sample_dataset_id}/hit-testing",
            method="POST",
            json={"records": []},
            status_code=200,
        )

        client = AsyncKnowledgeBaseClient(api_key=mock_api_key, dataset_id=sample_dataset_id)
        response = await client.hit_testing(query="test", retrieval_model=sample_retrieval_model)

        # Verify retrieval model is included
        requests = httpx_mock.get_requests()
        assert len(requests) == 1
        assert requests[0].method == "POST"
        request_json = json.loads(requests[0].content)
        assert "retrieval_model" in request_json
        assert response.status_code == 200


class TestKnowledgeBaseClientMetadataAPIs:
    """Test metadata management APIs."""

    async def test_get_dataset_metadata(
        self,
        httpx_mock: HTTPXMock,
        mock_api_key: str,
        sample_dataset_id: str) -> None:
        """Test getting dataset metadata."""
        httpx_mock.add_response(
            url=f"https://api.dify.ai/v1/datasets/{sample_dataset_id}/metadata",
            method="GET",
            json={"metadata": []},
            status_code=200,
        )

        client = AsyncKnowledgeBaseClient(api_key=mock_api_key, dataset_id=sample_dataset_id)
        response = await client.get_dataset_metadata()

        # Verify request
        requests = httpx_mock.get_requests()
        assert len(requests) == 1
        assert requests[0].method == "GET"
        assert response.status_code == 200

    async def test_create_dataset_metadata(
        self,
        httpx_mock: HTTPXMock,
        mock_api_key: str,
        sample_dataset_id: str,
        sample_metadata: dict) -> None:
        """Test creating dataset metadata."""
        httpx_mock.add_response(
            url=f"https://api.dify.ai/v1/datasets/{sample_dataset_id}/metadata",
            method="POST",
            json={"id": "meta-123"},
            status_code=200,
        )

        client = AsyncKnowledgeBaseClient(api_key=mock_api_key, dataset_id=sample_dataset_id)
        response = await client.create_dataset_metadata(metadata_data=sample_metadata)

        # Verify request
        requests = httpx_mock.get_requests()
        assert len(requests) == 1
        assert requests[0].method == "POST"
        assert response.status_code == 200

    async def test_update_dataset_metadata(
        self,
        httpx_mock: HTTPXMock,
        mock_api_key: str,
        sample_dataset_id: str,
        sample_metadata: dict) -> None:
        """Test updating dataset metadata."""
        metadata_id = "meta-123"
        httpx_mock.add_response(
            url=f"https://api.dify.ai/v1/datasets/{sample_dataset_id}/metadata/{metadata_id}",
            method="PATCH",
            json={"id": metadata_id},
            status_code=200,
        )

        client = AsyncKnowledgeBaseClient(api_key=mock_api_key, dataset_id=sample_dataset_id)
        response = await client.update_dataset_metadata(metadata_id=metadata_id, metadata_data=sample_metadata)

        # Verify request
        requests = httpx_mock.get_requests()
        assert len(requests) == 1
        assert requests[0].method == "PATCH"
        assert response.status_code == 200

    async def test_get_built_in_metadata(
        self,
        httpx_mock: HTTPXMock,
        mock_api_key: str,
        sample_dataset_id: str) -> None:
        """Test getting built-in metadata."""
        httpx_mock.add_response(
            url=f"https://api.dify.ai/v1/datasets/{sample_dataset_id}/metadata/built-in",
            method="GET",
            json={"metadata": []},
            status_code=200,
        )

        client = AsyncKnowledgeBaseClient(api_key=mock_api_key, dataset_id=sample_dataset_id)
        response = await client.get_built_in_metadata()

        # Verify request
        requests = httpx_mock.get_requests()
        assert len(requests) == 1
        assert requests[0].method == "GET"
        assert response.status_code == 200

    async def test_manage_built_in_metadata(
        self,
        httpx_mock: HTTPXMock,
        mock_api_key: str,
        sample_dataset_id: str) -> None:
        """Test managing built-in metadata."""
        httpx_mock.add_response(
            url=f"https://api.dify.ai/v1/datasets/{sample_dataset_id}/metadata/built-in/enable",
            method="POST",
            json={"result": "success"},
            status_code=200,
        )

        client = AsyncKnowledgeBaseClient(api_key=mock_api_key, dataset_id=sample_dataset_id)
        action = "enable"
        metadata_data = {"field": "value"}
        response = await client.manage_built_in_metadata(action=action, metadata_data=metadata_data)

        # Verify request
        requests = httpx_mock.get_requests()
        assert len(requests) == 1
        assert requests[0].method == "POST"
        assert response.status_code == 200

    async def test_update_documents_metadata(
        self,
        httpx_mock: HTTPXMock,
        mock_api_key: str,
        sample_dataset_id: str) -> None:
        """Test updating metadata for multiple documents."""
        httpx_mock.add_response(
            url=f"https://api.dify.ai/v1/datasets/{sample_dataset_id}/documents/metadata",
            method="POST",
            json={"result": "success"},
            status_code=200,
        )

        client = AsyncKnowledgeBaseClient(api_key=mock_api_key, dataset_id=sample_dataset_id)
        operation_data = [
            {"document_id": "doc-1", "metadata": {"key": "value1"}},
            {"document_id": "doc-2", "metadata": {"key": "value2"}},
        ]
        response = await client.update_documents_metadata(operation_data=operation_data)

        # Verify request
        requests = httpx_mock.get_requests()
        assert len(requests) == 1
        assert requests[0].method == "POST"
        assert response.status_code == 200


class TestKnowledgeBaseClientTagsAPIs:
    """Test dataset tags management APIs."""

    async def test_list_dataset_tags(
        self,
        httpx_mock: HTTPXMock,
        mock_api_key: str) -> None:
        """Test listing all dataset tags."""
        httpx_mock.add_response(
            url="https://api.dify.ai/v1/datasets/tags",
            method="GET",
            json={"tags": []},
            status_code=200,
        )

        client = AsyncKnowledgeBaseClient(api_key=mock_api_key)
        response = await client.list_dataset_tags()

        # Verify request
        requests = httpx_mock.get_requests()
        assert len(requests) == 1
        assert requests[0].method == "GET"
        assert response.status_code == 200

    async def test_bind_dataset_tags(
        self,
        httpx_mock: HTTPXMock,
        mock_api_key: str,
        sample_dataset_id: str) -> None:
        """Test binding tags to dataset."""
        httpx_mock.add_response(
            url="https://api.dify.ai/v1/datasets/tags/binding",
            method="POST",
            json={"result": "success"},
            status_code=200,
        )

        client = AsyncKnowledgeBaseClient(api_key=mock_api_key, dataset_id=sample_dataset_id)
        tag_ids = ["tag-1", "tag-2", "tag-3"]
        response = await client.bind_dataset_tags(tag_ids=tag_ids)

        # Verify request
        requests = httpx_mock.get_requests()
        assert len(requests) == 1
        assert requests[0].method == "POST"
        assert response.status_code == 200

    async def test_unbind_dataset_tag(
        self,
        httpx_mock: HTTPXMock,
        mock_api_key: str,
        sample_dataset_id: str) -> None:
        """Test unbinding a single tag from dataset."""
        tag_id = "tag-to-remove"
        httpx_mock.add_response(
            url="https://api.dify.ai/v1/datasets/tags/unbinding",
            method="POST",
            json={"result": "success"},
            status_code=200,
        )

        client = AsyncKnowledgeBaseClient(api_key=mock_api_key, dataset_id=sample_dataset_id)
        response = await client.unbind_dataset_tag(tag_id=tag_id)

        # Verify request
        requests = httpx_mock.get_requests()
        assert len(requests) == 1
        assert requests[0].method == "POST"
        assert response.status_code == 200

    async def test_get_dataset_tags(
        self,
        httpx_mock: HTTPXMock,
        mock_api_key: str,
        sample_dataset_id: str) -> None:
        """Test getting tags for current dataset."""
        httpx_mock.add_response(
            url=f"https://api.dify.ai/v1/datasets/{sample_dataset_id}/tags",
            method="GET",
            json={"tags": []},
            status_code=200,
        )

        client = AsyncKnowledgeBaseClient(api_key=mock_api_key, dataset_id=sample_dataset_id)
        response = await client.get_dataset_tags()

        # Verify request
        requests = httpx_mock.get_requests()
        assert len(requests) == 1
        assert requests[0].method == "GET"
        assert response.status_code == 200


class TestKnowledgeBaseClientRAGPipelineAPIs:
    """Test RAG pipeline APIs."""

    async def test_get_datasource_plugins(
        self,
        httpx_mock: HTTPXMock,
        mock_api_key: str,
        sample_dataset_id: str) -> None:
        """Test getting datasource plugins."""
        httpx_mock.add_response(
            url=re.compile(rf"https://api\.dify\.ai/v1/datasets/{re.escape(sample_dataset_id)}/pipeline/datasource-plugins.*"),
            method="GET",
            json={"plugins": []},
            status_code=200,
        )

        client = AsyncKnowledgeBaseClient(api_key=mock_api_key, dataset_id=sample_dataset_id)
        response = await client.get_datasource_plugins(is_published=True)

        # Verify request
        requests = httpx_mock.get_requests()
        assert len(requests) == 1
        assert requests[0].method == "GET"
        assert "is_published" in str(requests[0].url)
        assert response.status_code == 200

    async def test_run_datasource_node(
        self,
        httpx_mock: HTTPXMock,
        mock_api_key: str,
        sample_dataset_id: str) -> None:
        """Test running a datasource node."""
        node_id = "node-123"
        httpx_mock.add_response(
            url=f"https://api.dify.ai/v1/datasets/{sample_dataset_id}/pipeline/datasource/nodes/{node_id}/run",
            method="POST",
            json={"result": "success"},
            status_code=200,
        )

        client = AsyncKnowledgeBaseClient(api_key=mock_api_key, dataset_id=sample_dataset_id)
        inputs = {"query": "test"}
        datasource_type = "external"
        response = await client.run_datasource_node(node_id=node_id, inputs=inputs, datasource_type=datasource_type)

        # Verify request
        requests = httpx_mock.get_requests()
        assert len(requests) == 1
        assert requests[0].method == "POST"
        assert response.status_code == 200

    async def test_run_rag_pipeline_blocking(
        self,
        httpx_mock: HTTPXMock,
        mock_api_key: str,
        sample_dataset_id: str,
        sample_rag_pipeline_data: dict) -> None:
        """Test running RAG pipeline in blocking mode."""
        httpx_mock.add_response(
            url=f"https://api.dify.ai/v1/datasets/{sample_dataset_id}/pipeline/run",
            method="POST",
            json={"result": "success"},
            status_code=200,
        )

        client = AsyncKnowledgeBaseClient(api_key=mock_api_key, dataset_id=sample_dataset_id)
        response = await client.run_rag_pipeline(
            inputs=sample_rag_pipeline_data["inputs"],
            datasource_type=sample_rag_pipeline_data["datasource_type"],
            datasource_info_list=sample_rag_pipeline_data["datasource_info_list"],
            start_node_id=sample_rag_pipeline_data["start_node_id"],
            response_mode="blocking",
        )

        # Verify request
        requests = httpx_mock.get_requests()
        assert len(requests) == 1
        assert requests[0].method == "POST"
        assert response.status_code == 200

    async def test_run_rag_pipeline_streaming(
        self,
        httpx_mock: HTTPXMock,
        mock_api_key: str,
        sample_dataset_id: str,
        sample_rag_pipeline_data: dict) -> None:
        """Test running RAG pipeline in streaming mode."""
        httpx_mock.add_response(
            url=f"https://api.dify.ai/v1/datasets/{sample_dataset_id}/pipeline/run",
            method="POST",
            json={"result": "success"},
            status_code=200,
        )

        client = AsyncKnowledgeBaseClient(api_key=mock_api_key, dataset_id=sample_dataset_id)
        response = await client.run_rag_pipeline(
            inputs=sample_rag_pipeline_data["inputs"],
            datasource_type=sample_rag_pipeline_data["datasource_type"],
            datasource_info_list=sample_rag_pipeline_data["datasource_info_list"],
            start_node_id=sample_rag_pipeline_data["start_node_id"],
            response_mode="streaming",
        )

        # Verify streaming
        requests = httpx_mock.get_requests()
        assert len(requests) == 1
        assert requests[0].method == "POST"
        assert response.status_code == 200

    @patch("builtins.open", new_callable=mock_open, read_data=b"file content")
    async def test_upload_pipeline_file(
        self,
        mock_file,
        httpx_mock: HTTPXMock,
        mock_api_key: str) -> None:
        """Test uploading file for RAG pipeline."""
        httpx_mock.add_response(
            url="https://api.dify.ai/v1/datasets/pipeline/file-upload",
            method="POST",
            json={"id": "file-123"},
            status_code=200,
        )

        client = AsyncKnowledgeBaseClient(api_key=mock_api_key)
        file_path = "/tmp/pipeline_file.txt"
        response = await client.upload_pipeline_file(file_path=file_path)

        # Verify file was opened
        mock_file.assert_called_once_with(file_path, "rb")

        # Verify request
        requests = httpx_mock.get_requests()
        assert len(requests) == 1
        assert requests[0].method == "POST"
        assert response.status_code == 200
