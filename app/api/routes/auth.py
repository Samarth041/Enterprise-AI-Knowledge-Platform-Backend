from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.db.database import get_db
from app.schemas.auth import SignupRequest,LoginRequest,TokenResponse
from app.services.auth_service import signup,login
from app.schemas.user import UserResponse
from app.services.refresh_token_service import refresh_access_token,logout
from app.schemas.auth import RefreshTokenRequest,SignupRequest,LoginRequest,TokenResponse,LogoutRequest

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


@router.post("/refresh",response_model=TokenResponse)
def refresh(request:RefreshTokenRequest,db:Session=Depends(get_db)):
    #refresh access token using refresh token
    return refresh_access_token(db,request.refresh_token)

@router.post("/logout")
def logout_user(request:LogoutRequest,db:Session=Depends(get_db)):
    return logout(db,request.refresh_token)