from fastapi import APIRouter, Depends,HTTPException
from app.ai.chat_engine import generate_response
from app.models.user import User
from app.api.dependencies import get_current_user
from app.schemas.chat import ChatRequest,ChatResponse,ChatSessionResponse,ChatHistoryResponse
from sqlalchemy.orm import Session
from datetime import datetime
from app.db.database import get_db
from app.models.user import User
from fastapi.responses import StreamingResponse
from app.services.chat_service import process_chat_stream
from app.services.chat_service import process_chat,get_user_sessions,get_session,delete_session


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

@router.get("/sessions",response_model=list[ChatSessionResponse])
def list_sessions(db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    return get_user_sessions(db,current_user)


@router.get(
    "/session/{session_id}",
    response_model=ChatHistoryResponse
)
def get_chat_history(
    session_id:int,
    db:Session=Depends(get_db),
    current_user:User=Depends(get_current_user)
):
    session=get_session(
        db,
        session_id,
        current_user
    )

    if session is None:
        raise HTTPException(
            status_code=404,
            detail="Session not found"
        )

    return session


@router.delete("/sessions/{session_id}")
def remove_session(
    session_id:int,
    db:Session=Depends(get_db),
    current_user:User=Depends(get_current_user)
):  
    session=get_session(db,session_id,current_user)

    if session is None:
        raise HTTPException(
            status_code=404,
            detail="Session mot found"
        )

    delete_session(db,session)

    return{
        "message":"Conversation deleted successfully"
    }


@router.post("/stream")
def stream_chat(
    request:ChatRequest,
    db:Session=Depends(get_db),
    current_user:User=Depends(get_current_user)
):
    session_id,generator=process_chat_stream(
        db=db,
        user=current_user,
        session_id=request.session_id,
        message=request.message
    )

    return StreamingResponse(
        generator,
        media_type="text/plain",
        headers={
            "X-Session-ID":str(session_id)
        },

    )