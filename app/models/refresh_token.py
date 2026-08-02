from datetime import datetime
from sqlalchemy import ForeignKey,String,DateTime,Boolean,Integer,String
from sqlalchemy.orm import Mapped, mapped_column,relationship

from app.db.database import Base

class RefreshToken(Base):

    __tablename__="refresh_tokens"

    id:Mapped[int]=mapped_column(primary_key=True)

    token_hash:Mapped[str]=mapped_column(String(64),unique=True,nullable=False)

    user_id:Mapped[int]=mapped_column(ForeignKey("users.id"),nullable=False)

    expires_at:Mapped[datetime]=mapped_column(DateTime,nullable=False)

    created_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow)

    revoked:Mapped[bool]=mapped_column(Boolean,default=False)

    user:Mapped["User"]=relationship(back_populates="refresh_tokens")