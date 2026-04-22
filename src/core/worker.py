from src.db.session import AsyncSessionLocal
from src.monitor.services import MonitorService
from .checker import check_monitor, CheckResult
import asyncio
from src.probe import Probe
import httpx
from datetime import datetime, timezone
from .checker import is_monitor_due
from src.core.logger import logger


async def worker(client: httpx.AsyncClient):
    try:
        while True:

            now = datetime.now(timezone.utc)

            async with AsyncSessionLocal() as session:

                service = MonitorService(session)
                monitors = await service.get_all_monitors()

                due_monitors = [
                    monitor for monitor in monitors if is_monitor_due(monitor, now)
                ]
                if not due_monitors:
                    logger.debug(f"no monitors due, skipping check cycle")

                    await asyncio.sleep(3)
                    continue
                logger.info(f"checking {len(due_monitors)} monitors")

                tasks = [check_monitor(monitor, client) for monitor in due_monitors]

                results = await asyncio.gather(*tasks, return_exceptions=True)

                for monitor, result in zip(due_monitors, results):
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
                logger.info(f"Successfully processed {len(due_monitors)} probes")

            await asyncio.sleep(10)
    except asyncio.CancelledError:
        logger.info("worker shutting down..")
        raise

    except Exception as e:
        logger.error("worker crashed", exc_info=True)
        await asyncio.sleep(5)
