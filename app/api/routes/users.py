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
#get all users
@router.get("/",response_model=list[UserResponse])
def get_users(db:Session=Depends(get_db)):
    stmt=select(User)
    result=db.execute(stmt)
    users=result.scalars().all()
    return users


#get user by id
@router.get("/{user_id}",response_model=UserResponse)
def get_user(user_id:int,db:Session=Depends(get_db)):
    pass
    stmt=select(User).where(User.id==user_id)
    result=db.execute(stmt)
    user=result.scalar_one_or_none()
    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user
    



#create user
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



#delete user
@router.delete("/{user_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id:int,db:Session=Depends(get_db)):
    stmt=select(User).where(User.id==user_id)
    user=db.execute(stmt).scalar_one_or_none()
    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    db.delete(user)
    db.commit()

#update user details

@router.put("/{user_id}",response_model=UserResponse)
def update_user(user_id:int,updated_user:UserCreate,db:Session=Depends(get_db)):
    stmt=select(User).where(User.id==user_id)
    user=db.execute(stmt).scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    user.name=updated_user.name
    user.email=updated_user.email
    user.age=updated_user.age

    db.commit()
    db.refresh(user)
    return user