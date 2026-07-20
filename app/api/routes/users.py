from fastapi import APIRouter,status,HTTPException
from app.schemas.user import UserCreate,UserResponse

router=APIRouter(prefix="/users",tags=["Users"])
fake_db=[]


#routing
@router.get("/")
def get_users():
    return fake_db

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