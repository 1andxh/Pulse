from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import status, HTTPException
from datetime import datetime, timezone
import uuid
from .models import Monitor
from src.monitor.schemas import MonitorCreate, MonitorUpdate
from sqlalchemy import select, desc
from ..exceptions import DuplicateMonitorError, MonitorNotFoundError
from src.core.logger import logger
from sqlalchemy.exc import IntegrityError


class MonitorService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_monitor(self, data: MonitorCreate):
        logger.info(f"creating monitor for URL: {data.url}")
        normalized_url = data.url

        existing = await self.session.execute(
            select(Monitor).where(Monitor.url == normalized_url)
        )
        if existing.scalar_one_or_none():
            logger.warning(f"Duplicate monitor attempt: {data.url}")
            raise DuplicateMonitorError

        payload = data.model_dump()
        payload["url"] = normalized_url

        new_monitor = Monitor(**payload)

        try:
            self.session.add(new_monitor)
            await self.session.commit()
            await self.session.refresh(new_monitor)
            return new_monitor

        except IntegrityError:
            await self.session.rollback()
            raise DuplicateMonitorError

    async def get_all_monitors(self) -> list[Monitor]:
        stmt = select(Monitor).order_by(desc(Monitor.created_at))
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_monitor_by_id(self, id: uuid.UUID) -> Monitor:
        statement = await self.session.execute(select(Monitor).where(Monitor.id == id))
        monitor = statement.scalar_one_or_none()
        if monitor is None:
            logger.info("monitor not found")
            raise MonitorNotFoundError
        return monitor

    async def update_monitor(self, id: uuid.UUID, data: MonitorUpdate) -> Monitor:
        monitor = await self.get_monitor_by_id(id)

        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(monitor, key, value)

        await self.session.commit()
        await self.session.refresh(monitor)
        return monitor

    async def delete_monitor(self, monitor_id: uuid.UUID) -> None:
        monitor = await self.get_monitor_by_id(monitor_id)
        await self.session.delete(monitor)
        await self.session.commit()
        return
