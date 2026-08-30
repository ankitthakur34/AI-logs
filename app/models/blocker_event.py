from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime

from app.database.database import Base


class BlockerEvent(Base):
    __tablename__ = "blocker_events"

    id = Column(Integer, primary_key=True, index=True)

    # Blocker details
    blocker_command = Column(String, nullable=True)
    blocker_database_name = Column(String, nullable=True)
    blocker_host_name = Column(String, nullable=True)
    blocker_login_name = Column(String, nullable=True)
    blocker_object_name = Column(String, nullable=True)
    blocker_program_name = Column(String, nullable=True)
    blocker_schema_name = Column(String, nullable=True)
    blocker_session_id = Column(String, nullable=True)
    blocker_wait_type = Column(String, nullable=True)

    # Waiter details
    waiter_command = Column(String, nullable=True)
    waiter_database_name = Column(String, nullable=True)
    waiter_host_name = Column(String, nullable=True)
    waiter_login_name = Column(String, nullable=True)
    waiter_program_name = Column(String, nullable=True)
    waiter_session_id = Column(String, nullable=True)
    waiter_wait_type = Column(String, nullable=True)

    # Grafana / environment metadata
    app = Column(String, nullable=True)
    env = Column(String, nullable=True)
    instance = Column(String, nullable=True)
    job = Column(String, nullable=True)
    node_name = Column(String, nullable=True)
    os = Column(String, nullable=True)
    product_id = Column(String, nullable=True)
    provider = Column(String, nullable=True)
    region = Column(String, nullable=True)
    server_type = Column(String, nullable=True)
    sql_version = Column(String, nullable=True)
    user_metrics = Column(String, nullable=True)

    # Has this blocker event been added to the priority queue?
    queue_status = Column(
        String,
        nullable=False,
        default="NEW"
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