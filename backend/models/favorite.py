from sqlalchemy import Column, Integer, DateTime, ForeignKey
from datetime import datetime

from database import Base


class Favorite(Base):
    __tablename__ = "favorites"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    history_id = Column(
        Integer,
        ForeignKey("speech_history.id"),
        nullable=False,
        index=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )