from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.db.database import get_db
from app.schemas.auth import SignupRequest,LoginRequest,TokenResponse
from app.services.auth_service import signup,login
from app.schemas.user import UserResponse


router=APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/signup",response_model=UserResponse,status_code=status.HTTP_201_CREATED)
def signup_user(user:SignupRequest,db:Session=Depends(get_db)):
    return signup(db,user)


@router.post("/login",response_model=TokenResponse)
def login_user(form_data: OAuth2PasswordRequestForm = Depends(),db:Session=Depends(get_db)):
    return login(db,form_data)