from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm
from app.models.user import User
from app.schemas.auth import SignupRequest,LoginRequest,TokenResponse
from app.core.security import hash_password,verify_password,create_access_token
from app.core.logging import logger
from app.services.refresh_token_service import create_user_refresh_token

#signup service
def signup(db:Session,request:SignupRequest):
    #check if user already exists
    existing_user=db.scalar(
        select(User).where(User.email==request.email)
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )

    #create new user
    hashed_password=hash_password(request.password)
    db_user=User(
        name=request.name,
        email=request.email,
        age=request.age,
        phone=request.phone,
        hashed_password=hashed_password
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    logger.info(f"New user registered: {db_user.email}")
    return db_user

#login service

def login(db: Session, form_data: OAuth2PasswordRequestForm):
    db_user = db.scalar(
        select(User).where(User.email == form_data.username)
    )

    if not db_user:

        logger.warning(
            f"Login failed. User not found: {form_data.username}"
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    

    if not verify_password(form_data.password, db_user.hashed_password):

        logger.warning(
            f"Invalid password for {db_user.email}"
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        {"sub": db_user.email}
    )

    refresh_token = create_user_refresh_token(
        db,
        db_user
    )

    db.commit()

    logger.info(
        f"User logged in successfully :{db_user.email}"
    )

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
    )