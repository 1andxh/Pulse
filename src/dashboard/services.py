from sqlalchemy import select, func, Integer, cast
from sqlalchemy.ext.asyncio import AsyncSession
from src.monitor.models import Monitor
from src.probe.models import Probe
from .schemas import DashboardStats


class DashboardService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_statistics(self) -> DashboardStats:
        """monitor-probe count, overall up and response time"""
        monitor_count = select(func.count(Monitor.id))
        total_monitors = await self.session.scalar(monitor_count) or 0

        probe_count = select(func.count(Probe.id))
        total_probes = await self.session.scalar(probe_count) or 0

        uptime = select(func.avg(cast(Probe.is_up, Integer)))
        uptime_average = await self.session.scalar(uptime) or 0.0
        uptime_percentage = round(uptime_average * 100, 2)

        latency = select(func.avg(Probe.latency_ms))
        average_latency = await self.session.scalar(latency) or 0.0

        return DashboardStats(
            total_monitors=total_monitors,
            total_probes_recorded=total_probes,
            overall_uptime_percentage=uptime_percentage,
            average_response_time=round(average_latency, 2),
        )
