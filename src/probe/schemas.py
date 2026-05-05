import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ProbeRead(BaseModel):
    id: uuid.UUID
    monitor_id: uuid.UUID
    timestamp: datetime
    is_up: bool
    latency_ms: float
    error_message: str | None = None

    model_config = ConfigDict(from_attributes=True)


class ProbeHistoryResponse(BaseModel):
    monitor_id: uuid.UUID
    latest_status: bool
    history: list[ProbeRead]

    model_config = ConfigDict(from_attributes=True)
