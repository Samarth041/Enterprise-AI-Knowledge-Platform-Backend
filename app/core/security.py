from datetime import datetime, timedelta,timezone
from jose import jwt,JWTError
from passlib.context import CryptContext
from app.core.config import settings
from fastapi.security import OAuth2PasswordBearer
import hashlib
from uuid import uuid4


ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"

pwd_context = CryptContext( #password hashing context
    schemes=["bcrypt"],
    deprecated="auto"
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")



#hashing password
def hash_password(password:str)->str:
    return pwd_context.hash(password)

#verify password
def verify_password(plain_password:str,hashed_password:str)->bool:
    return pwd_context.verify(plain_password,hashed_password)

def create_access_token(data:dict)->str:
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update(
        {
            "exp":expire,
            "type": ACCESS_TOKEN_TYPE
        }
    )

    encoded_jwt = jwt.encode(to_encode,settings.SECRET_KEY,algorithm=settings.ALGORITHM)

    return encoded_jwt


#refresh token 
def create_refresh_token(data:dict)->str:
    to_encode= data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update(
        {
            "exp":expire,
            "type": REFRESH_TOKEN_TYPE,
            "jti":str(uuid4())
        }
    )

    encoded_jwt = jwt.encode(to_encode,settings.SECRET_KEY,algorithm=settings.ALGORITHM)

    return encoded_jwt


#decode access token
def decode_access_token(token:str)->dict:
    try:
        payload=jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        if payload.get("type") != "access":
            raise ValueError("Invalid token type")


        return payload

    except JWTError:
        raise ValueError("Invalid or expired token")

    
#---------------------------------------------------------
    #decode refresh token
def decode_refresh_token(token:str)->dict:
    try:
        payload=jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        if payload.get("type") != "refresh":
            raise ValueError("Invalid token type")

        return payload

    except JWTError:
        raise ValueError("Invalid or expired token")


#---------------------------------------------------------

#password hashing context
def hash_refresh_token(token:str)->str:
    return hashlib.sha256(token.encode()).hexdigest()

#verify hashed refresh token
def verify_refresh_token(refresh_token:str,stored_hash:str)->bool:
    return hash_refresh_token(refresh_token) == stored_hash

