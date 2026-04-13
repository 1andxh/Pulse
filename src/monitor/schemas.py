from pydantic import BaseModel, HttpUrl
import uuid


class MonitorCreate(BaseModel):
    name: str
    url: HttpUrl
    check_interval: int = 30


class MonitorUpdate(BaseModel):
    name: str | None
    url: HttpUrl | None
    is_active: bool | None
    check_interval: int | None


class MonitorRead(BaseModel):
    id: uuid.UUID
    name: str
    url: HttpUrl
    is_active: bool
    check_interval: int


# field validator for strict https?
