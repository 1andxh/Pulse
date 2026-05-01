from fastapi import APIRouter, Depends
from .schemas import ProbeRead
import uuid
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from ..db.session import get_session
from .services import ProbeService

probe_router = APIRouter()


async def _get_probe_service(
    session: AsyncSession = Depends(get_session),
) -> ProbeService:
    return ProbeService(session)


@probe_router.get("stats/{monitor_id}", response_model=list[ProbeRead])
async def get_probe_history(
    monitor_id: uuid.UUID, service: Annotated[ProbeService, Depends(_get_probe_service)]
):
    return service.get_latest_probes(monitor_id)
