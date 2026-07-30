from sqlalchemy.orm import Session,selectinload
from app.models.user import User
from sqlalchemy import select
from fastapi import HTTPException
from app.schemas.user import UserCreate
from app.core.logging import logger


#create user
def create_user(db: Session, user: UserCreate):
    db_user=User(
        name=user.name,
        email=user.email,
        age=user.age,
        phone=user.phone
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    logger.info(
        f"User created :{db_user.email}"
    )
    return db_user


#get all users
def get_users(
    db:Session,
    min_age: int | None=None,
    name: str | None=None,
    page: int=1,
    limit: int=10
):
    
    stmt=select(User)
    if min_age is not None:
        stmt=stmt.where(User.age>=min_age)
    if name is not None:
        stmt=stmt.where(User.name==name)
    offset=(page-1)*limit
    stmt=stmt.offset(offset).limit(limit)
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

        logger.warning(
            f"User not found. ID={user_id}"
        )
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
    user.phone = updated_user.phone

    db.commit()
    db.refresh(user)
    logger.info(
        f"User updated . ID={user_id}"
    )
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

    logger.info(
        f"User deleted. ID={user_id}"
    )

    db.delete(user)
    db.commit()