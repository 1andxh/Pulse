from fastapi import APIRouter, status, Depends
from typing import Annotated
from .schemas import MonitorRead, MonitorCreate
from .services import MonitorService
from .dependency import get_monitor_service
from src.db.session import get_session
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

_service = Annotated[MonitorService, Depends(get_monitor_service)]
session = Annotated[AsyncSession, Depends(get_session)]

monitor_router = APIRouter()


@monitor_router.post(
    "/", response_model=MonitorRead, status_code=status.HTTP_201_CREATED
)
async def create_monitor_route(payload: MonitorCreate, service: _service):
    monitor = await service.create_monitor(payload)
    return monitor


@monitor_router.get("/{monitor_id}", response_model=MonitorRead)
async def get_monitor(id: uuid.UUID, service: _service):
    return await service.get_monitor_by_id(id)
