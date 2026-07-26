from datetime import datetime, timedelta,timezone
from jose import jwt,JWTError
from passlib.context import CryptContext
from app.core.config import settings

pwd_context = CryptContext( #password hashing context
    schemes=["bcrypt"],
    deprecated="auto"
)


#hashing password
def hash_password(password:str)->str:
    return pwd_context.hash(password)

#verify password
def verify_password(plain_password:str,hashed_password:str)->bool:
    return pwd_context.verify(plain_password,hashed_password)