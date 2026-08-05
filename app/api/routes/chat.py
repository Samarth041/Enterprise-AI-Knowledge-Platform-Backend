from fastapi import APIRouter, Depends
from app.ai.chat_engine import generate_response
from app.models.user import User
from app.api.dependencies import get_current_user
from app.schemas.chat import ChatRequest,ChatResponse
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import User
from app.services.chat_service import process_chat


router=APIRouter(
    prefix="/chat",
    tags=["AI Chat"]
)

@router.post("",response_model=ChatResponse)
def chat_endpoint(request:ChatRequest,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    

    session_id,response=process_chat(
        db=db,
        user=current_user,
        session_id=request.session_id,
        message=request.message
    )

    return ChatResponse(
        session_id=session_id,
        response=response
    )

