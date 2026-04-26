from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.db.session import engine
from src.core.sentry import sentry
from .exception_handler import (
    pulse_exception_handler,
    validation_exception_handler,
    general_exception_handler,
    PulseError,
    RequestValidationError,
)
from src.core.worker import worker
import httpx
import asyncio
from src.core.health import health
from src.monitor.routes import monitor_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    client = httpx.AsyncClient()
    app.state.http_client = client

    task = asyncio.create_task(worker(client, app))

    try:
        yield
    finally:
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass

        await client.aclose()
        await engine.dispose()


app = FastAPI(title="Pulse Monitor", lifespan=lifespan)


@app.get("/")
def read_root():
    return {"Hello": "World"}


# exceptions
app.add_exception_handler(PulseError, pulse_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)


# routes
app.include_router(sentry, tags=["logs"])
app.include_router(health, tags=["health-checks"])
app.include_router(monitor_router, tags=["monitors"])
