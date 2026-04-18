from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.db.session import engine
from src.core.sentry import sentry


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


app.include_router(sentry)
