from io import BytesIO
from unittest.mock import patch


# ============================================================
# Authentication
# ============================================================

def test_document_upload_requires_authentication(client):

    response = client.post(
        "/documents/upload",
        files={
            "file": (
                "test.pdf",
                BytesIO(b"%PDF-1.4 fake pdf"),
                "application/pdf",
            )
        },
    )

    assert response.status_code in [401, 403]


# ============================================================
# Upload PDF
# ============================================================

def test_upload_document(auth_client):

    with patch(
        "app.api.routes.documents.process_document_ingestion"
    ) as mock_ingestion:

        response = auth_client.post(
            "/documents/upload",
            files={
                "file": (
                    "test.pdf",
                    BytesIO(b"%PDF-1.4 fake pdf"),
                    "application/pdf",
                )
            },
        )

    assert response.status_code == 202

    data = response.json()

    assert "document_id" in data
    assert "filename" in data
    assert "status" in data
    assert "chunks" in data

    assert data["filename"] == "test.pdf"
    assert data["status"] == "preprocessing"
    assert data["chunks"] == 0

    mock_ingestion.assert_called_once()


# ============================================================
# Reject non-PDF
# ============================================================

def test_upload_non_pdf_document(auth_client):

    response = auth_client.post(
        "/documents/upload",
        files={
            "file": (
                "test.txt",
                BytesIO(b"this is not a pdf"),
                "text/plain",
            )
        },
    )

    print(response.json())

    assert response.status_code == 400

    data = response.json()

    assert data["message"] == "Only PDF files are allowed."


# ============================================================
# List documents
# ============================================================

def test_list_documents(auth_client):

    with patch(
        "app.api.routes.documents.process_document_ingestion"
    ):

        upload_response = auth_client.post(
            "/documents/upload",
            files={
                "file": (
                    "list_test.pdf",
                    BytesIO(b"%PDF-1.4 fake pdf"),
                    "application/pdf",
                )
            },
        )

    assert upload_response.status_code == 202

    response = auth_client.get("/documents")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) >= 1

    filenames = [
        document["filename"]
        for document in data
    ]

    assert "list_test.pdf" in filenames


# ============================================================
# Delete document
# ============================================================

def test_delete_document(auth_client):

    with patch(
        "app.api.routes.documents.process_document_ingestion"
    ):

        upload_response = auth_client.post(
            "/documents/upload",
            files={
                "file": (
                    "delete_test.pdf",
                    BytesIO(b"%PDF-1.4 fake pdf"),
                    "application/pdf",
                )
            },
        )

    assert upload_response.status_code == 202

    document_id = upload_response.json()["document_id"]

    with patch(
        "app.services.document_service.get_vector_store"
    ) as mock_vector_store:

        mock_store = mock_vector_store.return_value

        delete_response = auth_client.delete(
            f"/documents/{document_id}"
        )

    assert delete_response.status_code == 200

    data = delete_response.json()

    assert data["message"] == "Document deleted successfully"

    mock_store.delete.assert_called_once()


# ============================================================
# Delete nonexistent document
# ============================================================

def test_delete_nonexistent_document(auth_client):

    response = auth_client.delete(
        "/documents/999999"
    )

    assert response.status_code == 404