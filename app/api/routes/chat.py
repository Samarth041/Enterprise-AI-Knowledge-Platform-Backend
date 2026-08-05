from fastapi import APIRouter, Depends
from app.ai.chat_service import chat
from app.models.user import User
from app.api.dependencies import get_current_user
from app.schemas.chat import ChatRequest,ChatResponse

router=APIRouter(
    prefix="/chat",
    tags=["AI Chat"]
)

@router.post("",response_model=ChatResponse)
def chat_endpoint(request:ChatRequest,current_user:User=Depends(get_current_user)):
    response=chat(request.message)

    return ChatResponse(
        response=response
    )

