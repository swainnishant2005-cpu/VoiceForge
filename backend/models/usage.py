from sqlalchemy import Column, Integer, Date, ForeignKey
from datetime import date

from database import Base


class Usage(Base):
    __tablename__ = "usage"

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

    usage_date = Column(
        Date,
        default=date.today,
        nullable=False
    )

    speech_count = Column(
        Integer,
        default=0,
        nullable=False
    )