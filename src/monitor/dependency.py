from .services import MonitorService
from sqlalchemy.ext.asyncio import AsyncSession


async def get_monitor_service(session: AsyncSession) -> MonitorService:
    return MonitorService(session)
