from datetime import datetime, timezone

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from sqlalchemy import select

from src.core.logger import logger
from src.db.session import AsyncSessionLocal

health = APIRouter()


@health.get("/health")
async def health_check(request: Request):
    now = datetime.now(timezone.utc)
    checks = {}
    logger.info("Health check requested")

    # worker check
    worker_last_seen = getattr(request.app.state, "worker_last_seen", None)
    if worker_last_seen is None:
        checks["worker"] = "not_started"
        worker_ok = False
    else:
        delta = (now - worker_last_seen).total_seconds()
        worker_ok = delta < 10
        if worker_ok:
            checks["worker"] = "healthy"
        else:
            checks["worker"] = "stale"

    # check db
    db_ok = True
    try:
        async with AsyncSessionLocal() as session:
            await session.execute(select(1))
            checks["database"] = "healthy"
    except Exception:
        db_ok = False
        checks["database"] = "unhealthy"
        logger.error("Database health check failed", exc_info=True)

    # overall health
    overall_ok = worker_ok and db_ok
    status_code = 200 if overall_ok else 503

    return JSONResponse(
        status_code=status_code,
        content={
            "status": "healthy" if overall_ok else "unhealthy",
            "checks": checks,
        },
    )
