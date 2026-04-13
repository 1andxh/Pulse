from typing import Any
from typing_extensions import Self
from pydantic import BaseModel, HttpUrl, field_validator, ConfigDict, Field
import uuid
from urllib.parse import urlparse


def url_validator(v: str | None) -> str | None:
    if v is None:
        return v

    v = v.strip().lower()

    parsed = urlparse(v)
    if parsed.scheme != "https":
        raise ValueError("URL must use https")

    if v.endswith("/"):
        v = v[:-1]

    return v


class MonitorCreate(BaseModel):
    name: str = Field(min_length=8, max_length=255)
    url: str
    check_interval: int = Field(default=30, ge=10, le=3600)

    @field_validator("url")
    @classmethod
    def validate_url(cls, v: str):
        return url_validator(v)


class MonitorUpdate(BaseModel):
    name: str | None
    url: str | None
    is_active: bool | None
    check_interval: int | None

    @field_validator("url")
    @classmethod
    def validate_url(cls, v: str):
        return url_validator(v)


class MonitorRead(BaseModel):
    id: uuid.UUID
    name: str
    url: str
    is_active: bool
    check_interval: int

    model_config = ConfigDict(from_attributes=True)
