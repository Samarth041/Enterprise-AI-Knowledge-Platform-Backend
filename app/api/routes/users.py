from fastapi import APIRouter,status,HTTPException
from app.schemas.user import UserCreate,UserResponse
from typing import Optional

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
    




@router.post("/",response_model=UserResponse,status_code=status.HTTP_201_CREATED)
def create_user(user:UserCreate):
    #generate a unique id
    user_id=len(fake_db)+1

    #create a dictionary representing the new user
    new_user={
        "id":user_id,
        "name":user.name,
        "email":user.email,
        "age":user.age
    }

    #store the user in the fake db
    fake_db.append(new_user)

    return new_user
 

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