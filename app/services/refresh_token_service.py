from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from sqlalchemy import select,update
from app.schemas.auth import TokenResponse
from app.models.refresh_token import RefreshToken
from app.models.user import User
from app.core.security import create_refresh_token, hash_refresh_token,decode_refresh_token,create_access_token
from app.core.config import settings


def create_user_refresh_token(db:Session,user:User)->str:
    #create refresh token
    refresh_token = create_refresh_token({"sub":user.email})
    #hash the refresh tokeen
    token_hash = hash_refresh_token(refresh_token)
    #store the hashed refresh token in the database
    db_token = RefreshToken(
        token_hash=token_hash,
        user_id=user.id,
        expires_at=datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),

    )

    db.add(db_token)
    

    return refresh_token



#refresh access token using refresh token

def refresh_access_token(db:Session,refresh_token:str)->dict:
    #step 1:Decode and validate the JWT
    try:
        payload=decode_refresh_token(refresh_token)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token"
        )


    #step 2:Extract email from payload
    email=payload.get("sub")
    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token payload"
        )

    #step 3:Hash the incoming refresh token
    token_hash=hash_refresh_token(refresh_token)

    #step 4:find the token in database
    db_token=db.scalar(
        select(RefreshToken).where(RefreshToken.token_hash==token_hash)
    )

    if not db_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token not found"
        )

    #step 5:Check if token has been revoked
    if db_token.revoked:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token has been revoked"
        )

    #step 6:Check if token has expired
    if db_token.expires_at < datetime.now():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token has expired"
        )

    #step 7:Load the associated user from the database
    user=db_token.user

    #step 8:Revoke old refresh token

    db_token.revoked=True

    #Step:9:- GEnerate new refresh token
    new_refresh_token=create_user_refresh_token(db=db,user=user)


    #step 10:Generate new access token
    access_token=create_access_token({"sub":user.email})
    #step :11:Commit the changes to the database
    db.commit()

    #step 12:Return the new access and refresh tokens
    return {
        "access_token":access_token,
        "refresh_token":new_refresh_token,
        
    }


#----------------------------------------------------
def logout(db:Session,refresh_token:str):
    try:
        decode_refresh_token(refresh_token)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token"
        )

    token_hash=hash_refresh_token(refresh_token)

    db_token=db.scalar(
        select(RefreshToken).where(RefreshToken.token_hash==token_hash)
    )

    if not db_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token not found"
        )

    db_token.revoked=True
    db.commit() 
    return{
        "message":"Logged out successfully"
    }


#-----------------------------------------------------------------------
def logout_all_devices(db:Session,refresh_token:str):
    #Step1: Validate refresh token
    try:
        payload=decode_refresh_token(refresh_token)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token"
        )

    #step 2:get email
    email=payload.get("sub")

    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

    #find user
    user=db.scalar(
        select(User).where(User.email==email)
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    #step 4:Revoke  every refresh token of this user

    db.execute(
        update(RefreshToken)
        .where(RefreshToken.user_id==user.id)
        .values(revoked=True)
    )

    #step 5:commit

    db.commit()

    return{
        "message":"Logged out from all devices successfully"
    }
    