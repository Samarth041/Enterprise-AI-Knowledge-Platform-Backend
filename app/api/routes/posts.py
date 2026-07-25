from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.post import PostCreate,PostResponse
from app.services.post_service import create_post as create_post_service


router=APIRouter(prefix="/posts",tags=["Posts"])

@router.post("/",response_model=PostResponse,status_code=status.HTTP_201_CREATED)
def create_post_route(post:PostCreate,db:Session=Depends(get_db)):
    return create_post_service(db,post)