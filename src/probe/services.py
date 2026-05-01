from sqlalchemy.ext.asyncio import AsyncSession
import uuid
from src.probe.models import Probe
from sqlalchemy import select, desc
from fastapi import HTTPException, status


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
        if not probes:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No probe data found for this monitor",
            )
        return {
            "monitor_id": monitor_id,
            "latest_status": probes[0].is_up,
            "history": probes,
        }
