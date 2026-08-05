from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Text, func
from sqlalchemy.orm import Mapped,mapped_column,relationship

from app.db.database import Base

class ChatMessage(Base):
    __tablename__="chat_messages"

    id:Mapped[int]=mapped_column(primary_key=True,index=True)

    session_id:Mapped[int]=mapped_column(
        ForeignKey("chat_sessions.id",ondelete="CASCADE"),
        nullable=False
    )

    role:Mapped[str]=mapped_column(nullable=False)

    content:Mapped[str]=mapped_column(
        Text,
        nullable=False
    )

    created_at:Mapped[datetime]=mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    session=relationship(
        "ChatSession",
        back_populates="messages"
    )