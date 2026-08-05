from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column , relationship
from app.db.database import Base

class ChatSession(Base):
    __tablename__="chat_sessions"

    id:Mapped[int]=mapped_column(primary_key=True,index=True)

    user_id:Mapped[int]=mapped_column(
        ForeignKey("users.id",ondelete="CASCADE"),
        nullable=False
    )

    title:Mapped[str]=mapped_column(
        String(255),
        default="New Chat"
    )

    created_at:Mapped[datetime]=mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at:Mapped[datetime]=mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    user=relationship(
        "User",
        back_populates="chat_sessions"
    )

    messages=relationship(
        "ChatMessage",
        back_populates="session",
        cascade="all,delete-orphan",
        order_by="ChatMessage.created_at"
    )