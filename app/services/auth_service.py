from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm
from app.models.user import User
from app.schemas.auth import SignupRequest,LoginRequest,TokenResponse
from app.core.security import hash_password,verify_password,create_access_token


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

    return db_user

#login service

def login(db: Session, form_data: OAuth2PasswordRequestForm):
    db_user = db.scalar(
        select(User).where(User.email == form_data.username)
    )

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # 👇 Add these debug prints here
    print("Password entered:", repr(form_data.password))
    print("Stored hash:", db_user.hashed_password)

    if not verify_password(form_data.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        {"sub": db_user.email}
    )

    return TokenResponse(
        access_token=access_token
    )