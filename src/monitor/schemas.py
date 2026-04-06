from pydantic import BaseModel, HttpUrl


class MonitorCreate(BaseModel):
    name: str
    url: HttpUrl
    check_interval: int = 30


# field validator for strict https?
