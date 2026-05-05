import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ProbeRead(BaseModel):
    id: uuid.UUID
    monitor_id: uuid.UUID
    timestamp: datetime
    is_up: bool
    latency_ms: float
    error_message: str

    model_config = ConfigDict(from_attributes=True)
