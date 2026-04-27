from sqlalchemy.ext.asyncio import AsyncSession
import uuid
from src.monitor.models import Probe
from sqlalchemy import select, desc


class ProbeService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_latest_probes(self, monitor_id: uuid.UUID, limit: int = 20):
        stmt = await self.session.execute(
            select(Probe)
            .where(Probe.monitor_id == monitor_id)
            .order_by(desc(Probe.timestamp))
            .limit(limit)
        )
        probes = stmt.scalars().all()
        return probes
