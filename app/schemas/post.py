from pydantic import BaseModel,ConfigDict

class PostCreate(BaseModel):
    title:str
    content:str
    user_id:int


class PostResponse(BaseModel):
    model_config=ConfigDict(from_attributes=True)
    id:int
    title:str
    content:str
    user_id:int


class PostSimpleResponse(BaseModel):
    model_config=ConfigDict(from_attributes=True)
    id:int
    title:str
    content:str