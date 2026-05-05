from fastapi import APIRouter

from .logger import logger

sentry = APIRouter()


@sentry.get("/sentry-debug")
async def trigger_error():
    logger.info("Manual error trigger via API")
    return 1 / 0
