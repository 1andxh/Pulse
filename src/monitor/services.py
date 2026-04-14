from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import status, HTTPException
from datetime import datetime, timezone
import uuid
from .models import Monitor
import schemas
from sqlalchemy import select, desc
from ..exceptions import DuplicateMonitorError


class MonitorService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_monitor(self, data: schemas.MonitorCreate):
        normalized_url = data.url

        existing = await self.session.execute(
            select(Monitor).where(Monitor.url == normalized_url)
        )
        if existing.scalar_one_or_none():
            raise DuplicateMonitorError

        payload = data.model_dump()
        payload["url"] = normalized_url

        new_monitor = Monitor(**payload)

        self.session.add(new_monitor)
        await self.session.commit()
        await self.session.refresh(new_monitor)

    async def get_all_monitors(self) -> list[Monitor]:
        stmt = select(Monitor).order_by(desc(Monitor.created_at))
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_monitor_by_id(self, id: uuid.UUID) -> Monitor:
        statement = await self.session.execute(select(Monitor).where(Monitor.id == id))
        monitor = statement.scalar_one_or_none()
        if monitor is None:
            raise
        return monitor

    async def delete_monitor(self, monitor_id: uuid.UUID) -> None:
        monitor = await self.get_monitor_by_id(monitor_id)
        await self.session.delete(monitor)
        await self.session.commit()
