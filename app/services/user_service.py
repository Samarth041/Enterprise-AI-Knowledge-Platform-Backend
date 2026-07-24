from sqlalchemy.orm import Session
from app.models.user import User
from sqlalchemy import select
from fastapi import HTTPException
from app.schemas.user import UserCreate


#create user
def create_user(db: Session, user: UserCreate):
    db_user=User(
        name=user.name,
        email=user.email,
        age=user.age
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


#get all users
def get_users(db:Session):
    stmt=select(User)
    result=db.execute(stmt)
    users=result.scalars().all()
    return users

#get user by id
def get_user(db:Session,user_id:int):
    stmt=select(User).where(User.id==user_id)
    result=db.execute(stmt)
    user=result.scalar_one_or_none()
    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user

#update user details

def update_user(db:Session,user_id:int,updated_user:UserCreate):
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

#delete user
def delete_user(db:Session,user_id:int):
    stmt=select(User).where(User.id==user_id)
    user=db.execute(stmt).scalar_one_or_none()
    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    db.delete(user)
    db.commit()