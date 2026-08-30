from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.database.database import Base


class BlockerQueue(Base):
    __tablename__ = "blocker_processing_queue"

    id = Column(Integer, primary_key=True, index=True)

    blocker_event_id = Column(
        Integer,
        ForeignKey("blocker_events.id"),
        nullable=False,
        unique=True,
        index=True
    )

    priority = Column(
        String,
        nullable=False
    )

    processing_status = Column(
        String,
        nullable=False,
        default="PENDING"
    )

    retry_count = Column(
        Integer,
        nullable=False,
        default=0
    )

    error_message = Column(
        Text,
        nullable=True
    )

    created_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    updated_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    processing_started_at = Column(
        DateTime,
        nullable=True
    )

    processing_completed_at = Column(
        DateTime,
        nullable=True
    )

    blocker_event = relationship(
        "BlockerEvent"
    )