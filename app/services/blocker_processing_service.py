from sqlalchemy.orm import Session

from app.repositories.blocker_event_repository import (
    BlockerEventRepository
)

from app.repositories.blocker_queue_repository import (
    BlockerQueueRepository
)

from app.services.priority_service import (
    PriorityService
)


class BlockerProcessingService:

    @staticmethod
    def process_new_events(
        db: Session
    ) -> dict:

        # ----------------------------------
        # 1. Fetch all unprocessed events
        # ----------------------------------
        events = BlockerEventRepository.get_new_events(db)

        counts = {
            "CRITICAL": 0,
            "HIGH": 0,
            "MEDIUM": 0,
            "LOW": 0
        }

        processed = 0
        already_queued = 0

        try:

            for event in events:

                # ----------------------------------
                # 2. Duplicate safety check
                # ----------------------------------
                existing_queue_item = (
                    BlockerQueueRepository.get_by_event_id(
                        db=db,
                        blocker_event_id=event.id
                    )
                )

                if existing_queue_item:

                    # Queue entry already exists.
                    # Sync blocker event status.
                    BlockerEventRepository.update_queue_status(
                        event=event,
                        status="QUEUED"
                    )

                    already_queued += 1
                    continue

                # ----------------------------------
                # 3. Calculate priority
                # ----------------------------------
                priority = (
                    PriorityService.calculate_priority(
                        event
                    )
                )

                # ----------------------------------
                # 4. Insert into priority queue
                # ----------------------------------
                BlockerQueueRepository.create(
                    db=db,
                    blocker_event_id=event.id,
                    priority=priority
                )

                # ----------------------------------
                # 5. Update source event
                #
                # NEW → QUEUED
                # ----------------------------------
                BlockerEventRepository.update_queue_status(
                    event=event,
                    status="QUEUED"
                )

                counts[priority] += 1
                processed += 1

            # ----------------------------------
            # 6. Commit everything together
            # ----------------------------------
            db.commit()

            return {
                "processed": processed,
                "already_queued": already_queued,
                "critical": counts["CRITICAL"],
                "high": counts["HIGH"],
                "medium": counts["MEDIUM"],
                "low": counts["LOW"]
            }

        except Exception:
            db.rollback()
            raise