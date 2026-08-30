from sqlalchemy.orm import Session

from app.models.blocker_event import BlockerEvent


class BlockerEventRepository:

    @staticmethod
    def get_by_id(
        db: Session,
        event_id: int
    ) -> BlockerEvent | None:

        return (
            db.query(BlockerEvent)
            .filter(BlockerEvent.id == event_id)
            .first()
        )

    @staticmethod
    def get_new_events(
        db: Session
    ) -> list[BlockerEvent]:

        return (
            db.query(BlockerEvent)
            .filter(
                BlockerEvent.queue_status == "NEW"
            )
            .order_by(
                BlockerEvent.created_at.asc()
            )
            .all()
        )

    @staticmethod
    def update_queue_status(
        event: BlockerEvent,
        status: str
    ) -> BlockerEvent:

        event.queue_status = status

        return event