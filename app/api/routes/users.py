from fastapi import APIRouter,status,HTTPException,Depends
from app.schemas.user import UserCreate,UserResponse
from typing import Optional
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.user import User
from sqlalchemy import select

router=APIRouter(prefix="/users",tags=["Users"])
fake_db=[]


#routing
@router.get("/",response_model=list[UserResponse])
def get_users(min_age:Optional[int]=None):
    if min_age is None:
        return fake_db

    filtered_users=[]

    for user in fake_db:
        if user["age"]>=min_age:
            filtered_users.append(user)

    return filtered_users

@router.get("/{user_id}",response_model=UserResponse)
def get_user(user_id:int):
    for user in fake_db:
        if user["id"]==user_id:
            return user

    raise HTTP_201_CREATED(
        status_code=status.HTTTP_404_NOT_FOUND,
        detail="User not found"
    )
    




@router.post("/",status_code=status.HTTP_201_CREATED,response_model=UserResponse)
def create_user(user:UserCreate,db:Session=Depends(get_db)):
    db_user=User(
        name=user.name,
        email=user.email,
        age=user.age
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# @router.post("/",status_code=status.HTTP_201_CREATED)
# def create_user(user:UserCreate):
#     return{
#         "message":"User created successfully",
#         "user":user
#     }

#delete user

@router.delete("/{id}",status_code=status.HTTP_200_OK)
def delete_user(id:int):
    for index,user in enumerate(fake_db):
        if user["id"]==id:
            fake_db.pop(index)
            return {"message":"User deleted successfully"}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found"
    )

#update

@router.put("/{id}",response_model=UserResponse)
def update_user(id:int,updated_user:UserCreate):
    for user in fake_db:

        if user["id"]==id:
            user["name"]=updated_user.name
            user["email"]=updated_user.email
            user["age"]=updated_user.age
            return user

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found"
    )