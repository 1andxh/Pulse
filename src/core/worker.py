from src.db.session import AsyncSessionLocal
from src.monitor.services import MonitorService
from .checker import check_monitor
import asyncio
from src.probe import Probe


async def worker():
    while True:
        async with AsyncSessionLocal() as session:
            service = MonitorService(session)
            monitors = await service.get_all_monitors()

            for monitor in monitors:
                tasks = [check_monitor(monitor.url) for m in monitors]
            results = await asyncio.gather(*tasks, return_exceptions=True)

            for monitor, result in zip(monitors, results):
                if result isinstance(Exception):
                    result

                probe = Probe(
                    monitor_id=monitor.id,
                    latency_ms=result.latency_ms,
                    is_up=result.is_up,
                    error_message=result.error_message
                )

                session.add(probe)

            await session.commit()
        await asyncio.sleep(10)
