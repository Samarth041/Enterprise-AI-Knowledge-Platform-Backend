from sqlalchemy.orm import Session,selectinload
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
def get_users(
    db:Session,
    min_age: int | None=None,
    name: str | None=None
):
    stmt=select(User)
    if min_age is not None:
        stmt=stmt.where(User.age>=min_age)
    if name is not None:
        stmt=stmt.where(User.name==name)
    result=db.execute(stmt)
    users=result.scalars().all()
    return users

#get user by id
def get_user(db:Session,user_id:int):
    stmt=(
        select(User)
        .options(selectinload(User.posts)) #early loading
        .where(User.id==user_id)
    )
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