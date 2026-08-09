from fastapi import APIRouter, Depends, File, UploadFile,BackgroundTasks,status
from sqlalchemy.orm import Session
from app.api.dependencies import get_current_user
from app.models.user import User
from app.db.database import get_db
from app.schemas.document import DocumentUploadResponse,DocumentResponse
from app.services.document_service import upload_document,get_user_documents,delete_document,process_document_ingestion
from app.ai.rag import generate_rag_response

from app.schemas.rag import RAGQueryRequest,RAGQueryResponse



router=APIRouter(
    prefix="/documents",
    tags=["Documents"]
)

#======================================================================
#Upload document
#======================================================================

@router.post("/upload",response_model=DocumentUploadResponse,status_code=status.HTTP_202_ACCEPTED)
def upload_document_endpoint(
    background_tasks:BackgroundTasks,
    file:UploadFile=File(...),
    db:Session=Depends(get_db),
    current_user:User=Depends(get_current_user)
):
    """
    Upload and index a PDF document.
    """

    document=upload_document(
        db=db,
        user=current_user,
        file=file
    )

    background_tasks.add_task(
        process_document_ingestion,
        document.id,
        document.file_path,
        current_user.id
    )


    return{
        "document_id":document.id,
        "filename":document.filename,
        "status":document.status,
        "chunks":0
    }

#========================================================
#list User Documents
#===============================================================

@router.get("",response_model=list[DocumentResponse])
def list_documents(
    db:Session=Depends(get_db),
    current_user:User=Depends(get_current_user)
):
    """
    list all documents uploaded by the current user.
    """

    return get_user_documents(
        db=db,
        user=current_user
    )


#===========================================================
#delete document
#===================================================

@router.delete("/{document_id}")
def delete_document_endpoint(
    document_id:int,
    db:Session=Depends(get_db),
    current_user:User=Depends(get_current_user)
):
    """
    Delete a document
    """

    delete_document(
        db=db,
        user=current_user,
        document_id=document_id
    )

    return{
        "message":"Document deleted successfully"
    }


@router.post("/query",response_model=RAGQueryResponse)
def query_documents(
    request:RAGQueryRequest,
    db:Session=Depends(get_db),
    current_user:User=Depends(get_current_user)
):

    """
    Aska question using the current user's documents.
    """

    result=generate_rag_response(
        question=request.question,
        user_id=current_user.id
    )

    return RAGQueryResponse(
        answer=result["answer"],
        sources=result["sources"]
    )