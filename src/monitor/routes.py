from fastapi import APIRouter, status, Depends
from typing import Annotated
from .schemas import MonitorRead, MonitorCreate, MonitorUpdate
from .services import MonitorService
from .dependency import get_monitor_service
from src.db.session import get_session
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

_service = Annotated[MonitorService, Depends(get_monitor_service)]


monitor_router = APIRouter()


@monitor_router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=MonitorRead
)
async def create_monitor_route(payload: MonitorCreate, service: _service):
    monitor = await service.create_monitor(payload)
    return monitor


@monitor_router.get("/{monitor_id}", response_model=MonitorRead)
async def get_monitor(monitor_id: uuid.UUID, service: _service):
    return await service.get_monitor_by_id(monitor_id)


@monitor_router.get("/", response_model=list[MonitorRead])
async def list_monitors(service: _service):
    monitors = await service.get_all_monitors()
    return monitors


@monitor_router.patch("/{monitor_monitor_id}", response_model=MonitorRead)
async def update_monitor(
    monitor_id: uuid.UUID,
    payload: MonitorUpdate,
    service: _service,
):
    return await service.update_monitor(monitor_id, payload)


@monitor_router.delete("/{monitor_monitor_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_monitor(monitor_id: uuid.UUID, service: _service):
    return await service.delete_monitor(monitor_id)
