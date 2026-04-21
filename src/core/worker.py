from src.db.session import AsyncSessionLocal
from src.monitor.services import MonitorService
from .checker import check_monitor, CheckResult
import asyncio
from src.probe import Probe
import httpx
from datetime import datetime, timezone
from .checker import is_monitor_due


async def worker(client: httpx.AsyncClient):
    async with httpx.AsyncClient() as client:

        while True:

            now = datetime.now(timezone.utc)

            async with AsyncSessionLocal() as session:

                service = MonitorService(session)
                monitors = await service.get_all_monitors()

                due_monitors = [
                    monitor for monitor in monitors if is_monitor_due(monitor, now)
                ]
                if not due_monitors:
                    await asyncio.sleep(3)
                    continue

                tasks = [check_monitor(monitor, client) for monitor in monitors]

                results = await asyncio.gather(*tasks, return_exceptions=True)

                for monitor, result in zip(monitors, results):
                    if isinstance(result, Exception):
                        normalized = CheckResult(
                            is_up=False, latency_ms=None, error_message=str(result)
                        )
                    else:
                        normalized = result

                    probe = Probe(
                        monitor_id=monitor.id,
                        latency_ms=normalized.latency_ms,
                        is_up=normalized.is_up,
                        error_message=normalized.error_message,
                    )
                    monitor.last_checked_at = now
                    session.add(probe)

                await session.commit()
            await asyncio.sleep(10)
