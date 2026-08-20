from io import BytesIO
from unittest.mock import patch, MagicMock
from langchain_core.messages import AIMessage



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

#=================================================================
#RAG Query Authetication 
#===================================================================

def test_rag_query_requires_authentication(client):
    response=client.post(
        "/documents/query",
        json={
            "question":"What is FastAPI?"
        }
    )

    assert response.status_code in [401,403]

#===========================================================
#RAG Query -with documents
#===========================================================

def test_raq_query_with_documents(auth_client):
    fake_documents=[
        MagicMock(
            page_content=(
                "FastAPI is a modern Python web framework "
                "used for building APIs"
            ),
            metadata={
                "document_id":1,
                "source":"test.pdf"
            },
        )
    ]

    fake_vector_store=MagicMock()

    fake_vector_store.similarity_search.return_value=(
        fake_documents
    )

    fake_llm=MagicMock()

    fake_llm.invoke.return_value=AIMessage(
        content="FastAPI is a Python web framework"
    )

    with patch(
        "app.ai.rag.get_vector_store",
        return_value=fake_vector_store,
    ), patch(
        "app.ai.rag.get_llm",
        return_value=fake_llm
    ):
        response=auth_client.post(
            "/documents/query",
            json={
                "question":"What is FastAPI?"
            }
        )

    assert response.status_code ==200

    data=response.json()

    assert "answer" in data
    assert "sources" in data

    assert data["answer"]==(
        "FastAPI is a Python web framework"
    )

    assert isinstance(data["sources"],list)

    fake_vector_store.similarity_search.assert_called_once()

    fake_llm.invoke.assert_called_once()

#==================================================================
#RAG Query- No documents
#===============================================================

def test_rag_query_no_documents(auth_client):
    fake_vector_store=MagicMock()

    fake_vector_store.similarity_search.return_value=[]

    fake_llm=MagicMock()

    with patch(
        "app.ai.rag.get_vector_store",
        return_value=fake_vector_store,
    ), patch(
        "app.ai.rag.get_llm",
        return_value=fake_llm
    ):
        response=auth_client.post(
            "/documents/query",
            json={
                "question": "What information is available?"
            }
        )

    assert response.status_code==200

    data=response.json()

    assert "answer" in data
    assert "sources" in data

    #llm shuld not be called when nothing was retrieved
    fake_llm.invoke.assert_not_called()
