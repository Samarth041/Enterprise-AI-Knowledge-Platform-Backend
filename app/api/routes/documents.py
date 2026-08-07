from fastapi import APIRouter, Depends, file, UploadFile
from sqlalchemy.orm import Session
from app.api.dependencies import get_current_user
from app.models.user import User
from app.db.database import get_db
from app.schemas.document import DocumentUploadResponse,DocumentResponse
from app.services.document_servivce import upload_document,get_user_documents,delete_document

router=APIRouter(
    prefix="/documents",
    tags=["Documents"]
)

#======================================================================
#Upload document
#======================================================================

@router.post("/upload",response_model=DocumentUploadResponse,status_code=201)
def upload_document_endpoint(
    file:UploadFile=File(...),
    db:Session=Depends(get_db),
    current_user:User=Depends(get_current_user)
):
    """
    Upload and index a PDF document.
    """

    return upload_document(
        db=db,
        user=current_user,
        file=file
    )

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

@route.delete("/{document_id}")
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