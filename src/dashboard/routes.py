from fastapi import APIRouter, Depends
from typing import Annotated
from src.dashboard.schemas import DashboardStats
from src.dashboard.services import DashboardService
from src.dashboard.dependency import get_dashboard_service

dashboard_router = APIRouter()

_service = Annotated[DashboardService, Depends(get_dashboard_service)]


@dashboard_router.get("/stats", response_model=DashboardStats)
async def get_dashboard_statistics(service: _service):
    return await service.get_statistics()
