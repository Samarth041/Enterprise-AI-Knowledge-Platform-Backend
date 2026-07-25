from sqlalchemy import ForeignKey, Column, Integer, String, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.db.database import Base

class Post(Base):
    __tablename__ = "posts"

    id:Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    title:Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    content:Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    user_id:Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    #relationship extablishment b/w post and user
    user:Mapped["User"]=relationship(
        back_populates="posts"
    )