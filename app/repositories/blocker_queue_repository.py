from sqlalchemy.orm import Session
from sqlalchemy import case

from app.models.blocker_queue import BlockerQueue


class BlockerQueueRepository:

    @staticmethod
    def create(
        db: Session,
        blocker_event_id: int,
        priority: str
    ) -> BlockerQueue:

        queue_item = BlockerQueue(
            blocker_event_id=blocker_event_id,
            priority=priority,
            processing_status="PENDING"
        )

        db.add(queue_item)
        db.flush()

        return queue_item

    @staticmethod
    def get_by_id(
        db: Session,
        queue_id: int
    ) -> BlockerQueue | None:

        return (
            db.query(BlockerQueue)
            .filter(BlockerQueue.id == queue_id)
            .first()
        )

    @staticmethod
    def get_by_event_id(
        db: Session,
        blocker_event_id: int
    ) -> BlockerQueue | None:

        return (
            db.query(BlockerQueue)
            .filter(
                BlockerQueue.blocker_event_id == blocker_event_id
            )
            .first()
        )

    @staticmethod
    def get_pending(
        db: Session
    ) -> list[BlockerQueue]:

        priority_order = case(
            (BlockerQueue.priority == "CRITICAL", 1),
            (BlockerQueue.priority == "HIGH", 2),
            (BlockerQueue.priority == "MEDIUM", 3),
            (BlockerQueue.priority == "LOW", 4),
            else_=5
        )

        return (
            db.query(BlockerQueue)
            .filter(
                BlockerQueue.processing_status == "PENDING"
            )
            .order_by(
                priority_order,
                BlockerQueue.created_at.asc()
            )
            .all()
        )

    @staticmethod
    def get_next_pending(
        db: Session
    ) -> BlockerQueue | None:

        priority_order = case(
            (BlockerQueue.priority == "CRITICAL", 1),
            (BlockerQueue.priority == "HIGH", 2),
            (BlockerQueue.priority == "MEDIUM", 3),
            (BlockerQueue.priority == "LOW", 4),
            else_=5
        )

        return (
            db.query(BlockerQueue)
            .filter(
                BlockerQueue.processing_status == "PENDING"
            )
            .order_by(
                priority_order,
                BlockerQueue.created_at.asc()
            )
            .first()
        )

    @staticmethod
    def get_all(
        db: Session
    ) -> list[BlockerQueue]:

        return (
            db.query(BlockerQueue)
            .order_by(BlockerQueue.created_at.desc())
            .all()
        )

    @staticmethod
    def update_status(
        queue_item: BlockerQueue,
        status: str
    ) -> BlockerQueue:

        queue_item.processing_status = status

        return queue_item