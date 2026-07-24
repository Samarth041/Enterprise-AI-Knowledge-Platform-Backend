from fastapi import APIRouter,status,HTTPException,Depends
from app.schemas.user import UserCreate,UserResponse
from typing import Optional
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.user import User
from sqlalchemy import select
from app.services.user_service import get_users as get_users_service
from app.services.user_service import get_user as get_user_service
from app.services.user_service import create_user as create_user_service
from app.services.user_service import delete_user as delete_user_service
from app.services.user_service import update_user as update_user_service

router=APIRouter(prefix="/users",tags=["Users"])
#fake_db=[]


#routing
#get all users
@router.get("/",response_model=list[UserResponse])
def get_users(db:Session=Depends(get_db)):
    return get_users_service(db)


#get user by id
@router.get("/{user_id}",response_model=UserResponse)
def get_user(user_id:int,db:Session=Depends(get_db)):
    return get_user_service(db,user_id)
    



#create user
@router.post("/",status_code=status.HTTP_201_CREATED,response_model=UserResponse)
def create_user(user:UserCreate,db:Session=Depends(get_db)):
    return create_user_service(db,user)


#delete user
@router.delete("/{user_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id:int,db:Session=Depends(get_db)):
    delete_user_service(db,user_id)

#update user details

@router.put("/{user_id}",response_model=UserResponse)
def update_user(user_id:int,updated_user:UserCreate,db:Session=Depends(get_db)):
    return update_user_service(db,user_id,updated_user)


