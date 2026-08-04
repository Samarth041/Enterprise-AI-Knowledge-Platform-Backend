from fastapi import APIRouter
from fastapi import UploadFile, File,HTTPException,status
from pathlib import Path
from uuid import uuid4

router=APIRouter(
    prefix="/files",
    tags=["Files"]
)

UPLOAD_DIR=Path("uploads/documents")

UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True
)

ALLOWED_TYPES={
    "application/pdf",
    "text/plain"
}

MAX_FILE_SIZE=5*1024*1024  # 5MB

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):

    #validate MIME type

    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF AND TXT files are allowed"
        )

    #read file
    content=await file.read()

    #validate size
    if len(content)>MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File size exceeds 5 MB."
        )

    #Generate unique filename
    extension=Path(file.filename).suffix

    stored_name=f"{uuid4()}{extension}"

    filepath=UPLOAD_DIR/stored_name

    #save file
    with open (filepath,"wb") as buffer:
        buffer.write(content)

    return{
        "original_filename":file.filename,
        "stored_filename":stored_name,
        "content_type":file.content_type,
        "size":len(content),
        "path":str(filepath)

    }



