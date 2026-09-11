from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey
from datetime import datetime

from database import Base


class SpeechHistory(Base):
    __tablename__ = "speech_history"

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

    text = Column(
        Text,
        nullable=False
    )

    language = Column(
        String(20),
        nullable=False
    )

    voice = Column(
        String(100),
        nullable=False
    )

    speed = Column(
        Float,
        default=1.0,
        nullable=False
    )

    audio_filename = Column(
        String(255),
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )