from typing import Annotated

from fastapi import APIRouter, Depends

from src.dashboard.dependency import get_dashboard_service
from src.dashboard.schemas import DashboardStats
from src.dashboard.services import DashboardService

dashboard_router = APIRouter()

_service = Annotated[DashboardService, Depends(get_dashboard_service)]


@dashboard_router.get("/stats", response_model=DashboardStats)
async def get_dashboard_statistics(service: _service):
    return await service.get_statistics()
