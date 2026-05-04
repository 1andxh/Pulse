from .services import DashboardService
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.session import get_session
from fastapi import Depends


async def get_dashboard_service(
    session: AsyncSession = Depends(get_session),
) -> DashboardService:
    return DashboardService(session)
