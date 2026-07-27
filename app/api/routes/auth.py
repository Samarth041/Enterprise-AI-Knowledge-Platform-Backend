from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.auth import SignupRequest,LoginRequest,TokenResponse
from app.services.auth_service import signup,login
from app.schemas.auth import UserResponse


router=APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/signup",response_model=UserResponse,status_code=status.HTTP_201_CREATED)
def signup_user(user:SignupRequest,db:Session=Depends(get_db)):
    return signup(db,user)


@router.post("/login",response_model=TokenResponse)
def login_user(credentials:LoginRequest,db:Session=Depends(get_db)):
    return login(db,credentials)