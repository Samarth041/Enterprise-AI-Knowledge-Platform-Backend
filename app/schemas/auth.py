from pydantic import BaseModel, EmailStr, Field, ConfigDict

class SignupRequest(BaseModel):
    name:str=Field(
        min_length=2,
    )

    email:EmailStr

    password:str=Field(
        min_length=8,
    )

    age:int=Field(ge=18, le=100)
    phone:str

class LoginRequest(BaseModel):
    email:EmailStr
    password:str

class TokenResponse(BaseModel):
    access_token:str
    token_type:str="bearer"

    