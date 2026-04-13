from pydantic import BaseModel
import uuid
from datetime import datetime


class ProbeRead(BaseModel):
    id: uuid.UUID
    monitor_id: uuid.UUID
    timestamp: datetime
    is_up: bool
    latency_ms: float
    error_message: str
