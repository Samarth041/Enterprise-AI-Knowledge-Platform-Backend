from fastapi import APIRouter,status
from app.schemas.user import UserCreate,UserResponse

router=APIRouter(prefix="/users",tags=["Users"])

#routing
@router.get("/")
def get_users():
    return[
        {
            "id":1,
            "name":"Alice",
            "email":"alice@example.com"
        },
        {
            "id":2,
            "name":"Bob",
            "email":"bob@example.com"
        }
    ]

@router.get("/{user_id}")
def get_user(user_id:int):
    return{
        "id":user_id,
        "name":"Bob",
        "email":"bob@example.com"
    }
    




@router.post("/",response_model=UserResponse,status_code=status.HTTP_201_CREATED)
def create_user(user:UserCreate):
    return {
        "id":1,
        "name":user.name,
        "email":user.email
    }