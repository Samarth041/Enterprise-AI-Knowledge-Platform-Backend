from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, Mapped,mapped_column

from app.db.database import Base

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
