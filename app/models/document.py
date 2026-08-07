from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base

class Document(Base):
    __tablename__="documents"

    id:Mapped[int]=mapped_column(primary_key=True)

    user_id:Mapped[int]=mapped_column(
        ForeignKey("users.id")
    )

    filename:Mapped[str]=mapped_column(String)

    file_path:Mapped[str]=mapped_column(String)

    status:Mapped[str]=mapped_column(
        default="indexed"
    )

    created_at:Mapped[datetime]=mapped_column(
        DateTime,
        default=datetime.utcnow,

    )

    user=relationship(
        "User",
        back_populates="documents"
    )