from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class BlockerEventResponse(BaseModel):
    id: int

    # Blocker details
    blocker_command: Optional[str] = None
    blocker_database_name: Optional[str] = None
    blocker_host_name: Optional[str] = None
    blocker_login_name: Optional[str] = None
    blocker_object_name: Optional[str] = None
    blocker_program_name: Optional[str] = None
    blocker_schema_name: Optional[str] = None
    blocker_session_id: Optional[str] = None
    blocker_wait_type: Optional[str] = None

    # Waiter details
    waiter_command: Optional[str] = None
    waiter_database_name: Optional[str] = None
    waiter_host_name: Optional[str] = None
    waiter_login_name: Optional[str] = None
    waiter_program_name: Optional[str] = None
    waiter_session_id: Optional[str] = None
    waiter_wait_type: Optional[str] = None

    # Metadata
    app: Optional[str] = None
    env: Optional[str] = None
    instance: Optional[str] = None
    job: Optional[str] = None
    node_name: Optional[str] = None
    os: Optional[str] = None
    product_id: Optional[str] = None
    provider: Optional[str] = None
    region: Optional[str] = None
    server_type: Optional[str] = None
    sql_version: Optional[str] = None
    user_metrics: Optional[str] = None

    queue_status: str

    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }