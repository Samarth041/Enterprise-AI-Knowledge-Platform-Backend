from pydantic import BaseModel, EmailStr,Field,ConfigDict
from app.schemas.post import PostSimpleResponse
class UserCreate(BaseModel):
    name:str=Field(
        min_length=2,
        description="USer name must have at least 2 characters"
    )
    email:EmailStr

    age:int=Field(
        ge=18,
        le=100,
        description="Age msut be b/w 18 and 100"
    )

    phone:str|None=None

class UserResponse(BaseModel):
    id:int
    name:str
    email:EmailStr
    age:int
    phone:str|None=None
    posts:list[PostSimpleResponse]= Field(default_factory=list)

    model_config=ConfigDict(from_attributes=True)

