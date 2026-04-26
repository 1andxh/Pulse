from .services import MonitorService
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.session import get_session
from fastapi import Depends


async def get_monitor_service(
    session: AsyncSession = Depends(get_session),
) -> MonitorService:
    return MonitorService(session)
