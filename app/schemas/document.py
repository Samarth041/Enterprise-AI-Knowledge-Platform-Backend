from datetime import datetime
from pydantic import BaseModel

class DocumentUploadResponse(BaseModel):
    document_id:str
    filename:str
    status:str
    chunks:int

class DocumentResposne(BaseModel):
    id:int
    filename:str
    status:str
    created_at:datetime

    model_config={
        "from_attributes":True
    }