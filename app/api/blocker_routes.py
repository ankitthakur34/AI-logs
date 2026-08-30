from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db

from app.schemas.blocker_queue import (
    BlockerQueueResponse,
    BlockerQueueStatusUpdate
)

from app.repositories.blocker_queue_repository import (
    BlockerQueueRepository
)

from app.services.blocker_processing_service import (
    BlockerProcessingService
)


router = APIRouter(
    prefix="/blockers",
    tags=["Blockers"]
)


# =========================================================
# Process raw blocker events
#
# blocker_events:
#
# NEW
#   ↓
# PriorityService
#   ↓
# blocker_processing_queue
#   ↓
# blocker_event = QUEUED
# =========================================================
@router.post("/process-priority")
def process_priority(
    db: Session = Depends(get_db)
):
    try:

        result = (
            BlockerProcessingService.process_new_events(
                db
            )
        )

        return {
            "message": "Priority processing completed",
            **result
        }

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=f"Priority processing failed: {str(exc)}"
        )


# =========================================================
# Get complete queue
# =========================================================
@router.get(
    "/queue",
    response_model=list[BlockerQueueResponse]
)
def get_queue(
    db: Session = Depends(get_db)
):

    return BlockerQueueRepository.get_all(db)


# =========================================================
# Get only pending records
#
# Sorted:
#
# CRITICAL
# HIGH
# MEDIUM
# LOW
# =========================================================
@router.get(
    "/queue/pending",
    response_model=list[BlockerQueueResponse]
)
def get_pending_queue(
    db: Session = Depends(get_db)
):

    return BlockerQueueRepository.get_pending(db)


# =========================================================
# Get next highest priority record
#
# This endpoint will later be consumed by our Agent.
# =========================================================
@router.get(
    "/queue/next",
    response_model=BlockerQueueResponse
)
def get_next_queue_item(
    db: Session = Depends(get_db)
):

    queue_item = (
        BlockerQueueRepository.get_next_pending(db)
    )

    if not queue_item:
        raise HTTPException(
            status_code=404,
            detail="No pending blocker events found"
        )

    return queue_item


# =========================================================
# Update processing status
#
# PENDING
#    ↓
# PROCESSING
#    ↓
# COMPLETED
#
# OR
#
# FAILED
# =========================================================
@router.patch(
    "/queue/{queue_id}/status",
    response_model=BlockerQueueResponse
)
def update_queue_status(
    queue_id: int,
    status_data: BlockerQueueStatusUpdate,
    db: Session = Depends(get_db)
):

    queue_item = (
        BlockerQueueRepository.get_by_id(
            db=db,
            queue_id=queue_id
        )
    )

    if not queue_item:
        raise HTTPException(
            status_code=404,
            detail="Queue item not found"
        )

    allowed_statuses = {
        "PENDING",
        "PROCESSING",
        "COMPLETED",
        "FAILED"
    }

    new_status = (
        status_data.processing_status
        .strip()
        .upper()
    )

    if new_status not in allowed_statuses:

        raise HTTPException(
            status_code=400,
            detail=(
                "Invalid status. Allowed values: "
                "PENDING, PROCESSING, COMPLETED, FAILED"
            )
        )

    try:

        BlockerQueueRepository.update_status(
            queue_item=queue_item,
            status=new_status
        )

        db.commit()
        db.refresh(queue_item)

        return queue_item

    except Exception as exc:

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Failed to update queue status: {str(exc)}"
        )