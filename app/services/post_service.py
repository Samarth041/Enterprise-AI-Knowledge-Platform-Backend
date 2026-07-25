from sqlalchemy.orm import Session
from app.models.post import Post
from app.schemas.post import PostCreate,PostResponse


def create_post(db:Session,post:PostCreate):
    db_post=Post(
        title=post.title,
        content=post.content,
        user_id=post.user_id
    )

    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post