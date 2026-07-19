from fastapi import APIRouter

router=APIRouter(prefix="/users",tags=["Users"])


users = [
    "Alice",
    "Bob",
    "Charlie",
    "David",
    "Emma",
    "Frank",
    "Grace",
    "Harry",
    "Ivy",
    "Jack",
    "Kevin",
    "Liam",
    "Mia",
    "Noah",
    "Olivia"
]

#routing
@router.get("/")
def get_users(limit:int=10,skip:int=0):
    return{
        "limit":limit,
        "skip":skip
    }
    


#routing parameters
@router.get("/{user_id}")
def get_user(user_id:int):
    return{"user_id":user_id}