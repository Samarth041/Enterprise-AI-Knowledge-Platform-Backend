from pydantic import BaseModel, Field
from datetime import datetime

class ChatRequest(BaseModel):
    session_id: int | None = Field(
        default=None,
        description="Existing chat session ID. Leave empty to create a new session.",
        example=None,
    )
    message:str=Field(
        ...,
        min_length=1,
        max_length=4000
    )


class ChatResponse(BaseModel):
    session_id:int
    response:str

class ChatSessionResponse(BaseModel):
    id:int
    title:str
    created_at:datetime

    model_config={
        "from_attributes":True
    }

class ChatMessageResponse(BaseModel):
    role:str
    content:str
    created_at:datetime

    model_config={
        "from_attributes":True
    }

    
class ChatHistoryResponse(BaseModel):
    id:int
    title:str
    messages:list[ChatMessageResponse]

    model_config={
        "from_attributes":True
    }
    