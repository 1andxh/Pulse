from dataclasses import dataclass
import time
import httpx
from src.monitor import Monitor
from src.probe import Probe
import asyncio


@dataclass
class CheckResult:
    is_up: bool
    latency_ms: float | None
    error_message: str | None


async def check_monitor(monitor: Monitor):

    start = time.perf_counter()
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(monitor.url, timeout=5.0)

            latency_ms = (time.perf_counter() - start) * 1000

            if response.status_code < 400:
                Probe.is_up = True
            Probe.is_up = False

            return CheckResult(
                is_up=Probe.is_up, latency_ms=latency_ms, error_message=None
            )
    except Exception as e:
        latency_ms = (time.perf_counter() - start) * 1000

        return CheckResult(is_up=False, latency_ms=latency_ms, error_message=str(e))

    await asyncio.sleep(10)
