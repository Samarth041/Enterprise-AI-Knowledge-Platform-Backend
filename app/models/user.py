from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, Mapped,mapped_column
from app.db.database import Base
from app.models.refresh_token import RefreshToken

class User(Base):
    __tablename__="users"

    id:Mapped[int]=mapped_column(
        Integer,
        primary_key=True,
        index=True
    )
    name:Mapped[str]=mapped_column(
        String(50),
        nullable=False
    )
    email:Mapped[str]=mapped_column(
        String(50),
        unique=True,
        nullable=False
    )
    age:Mapped[int]=mapped_column(
        Integer,
        nullable=False
    )

    phone:Mapped[str]=mapped_column(
        String(15),
        nullable=True
    )

    hashed_password:Mapped[str]=mapped_column(
        String(255),
        nullable=False
    )

    #RBAC role:- role based access control
    role:Mapped[str]=mapped_column(
        String(20),
        default="user",
        nullable=False
    )


    #relationship extablishment b/w user and post
    posts:Mapped[list["Post"]]=relationship(
        back_populates="user",
        cascade="all,delete"
    )

    refresh_tokens:Mapped[list["RefreshToken"]]=relationship(
        back_populates="user",
        cascade="all,delete-orphan"
    )

    chat_sessions=relationship(
        "ChatSession",
        back_populates="user",
        cascade="all,delete-orphan"
    )

    documents=relationship(
        "Document",
        back_populates="user",
        cascade="all,delete-orphan"
    )


