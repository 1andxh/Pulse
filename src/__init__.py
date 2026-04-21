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


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting Pulse...")
    yield
    print("Shutting down")
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
app.include_router(sentry)
