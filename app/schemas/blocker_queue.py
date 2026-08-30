from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.schemas.blocker_event import BlockerEventResponse


class BlockerQueueResponse(BaseModel):
    id: int
    blocker_event_id: int

    priority: str
    processing_status: str

    retry_count: int
    error_message: Optional[str] = None

    created_at: datetime
    updated_at: datetime

    processing_started_at: Optional[datetime] = None
    processing_completed_at: Optional[datetime] = None

    blocker_event: Optional[BlockerEventResponse] = None

    model_config = {
        "from_attributes": True
    }


class BlockerQueueStatusUpdate(BaseModel):
    processing_status: str