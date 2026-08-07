from pathlib import Path
import shutil
from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session
import uuid

from app.ai.ingest import ingest_document
from app.models.document import Document
from app.models.user import User

UPLOAD_DIR=Path("uploads/documents")
UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True
)

def upload_document(db:Session,user:User,file:UploadFile):

    """
    Upload a PDF, save it locally , ingest it into ChromaDB,
    and store its metadata in the SQL database.
    """

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is required"
        )

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
        )

    #===================================================================
    #Generate unique filename
    #===================================================================

    unique_filename=f"{uuid.uuid4()}_{file.filename}"

    file_path=UPLOAD_DIR/unique_filename

    #===================================================================
    #Save PDF to disk
    #==================================================================

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )

    #=============================================================='
    #create DB record
    #===============================================================

    document=Document(
        user_id=user.id,
        filename=file.filename,
        file_path=str(file_path),
        status="preprocessing"
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    #===================================================================
    #Ingest Document
    #=====================================================================

    try:
        chunk_count=ingest_document(
            str(file_path)
        )

        document.status="indexed"
        db.commit()

    except Exception:

        document.status="failed"

        db.commit()

        raise

    #===============================================
    #response
    #==========================================================

    return{
        "document_id":document.id,
        "filename":document.filename,
        "status":document.status,
        "chunks":chunk_count
    }


#================================================================
#get user documents
#===================================================================
def get_user_documents(
    db:Session,
    user:User
):
    """
    Return all documents uploaded by the current user.
    """

    return(
        db.query(Document)
        .filter(Document.user_id==user.id)
        .order_by(Document.created_at.desc())
        .all()
    )


#==================================================================
#Delete document
#===============================================================

def delete document(db:Session,user:User,document_id:int):

    """
    Delete a document belonging to the current user
    """

    document=(
        db.query(Document)
        .filter(
            Document.id==document_id,
            Document.user_id==user.id,
        )
        .first()
    )


    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )


    #delete local pdf
    file_path=Path(document.file_path)

    if file_path.exists():
        file_path.unlink()

    #delete database record
    db.delete(document)
    db.commit()
    return True


    



