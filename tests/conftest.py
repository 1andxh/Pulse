import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from httpx import AsyncClient, ASGITransport
from src import app

from src.db.base import Base
from src.db.session import get_session

DATABASE_URL = "sqlite+aiosqlite:///.test.db"

engine = create_async_engine(url=DATABASE_URL, echo=False)


TestingSessionLocal = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


@pytest_asyncio.fixture(scope="function", autouse=True)
async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture()
async def db_session():
    async with TestingSessionLocal() as session:
        yield session


@pytest_asyncio.fixture()
async def override_get_session(db_session):
    async def _override():
        yield db_session

    app.dependency_overrides[get_session] = _override
    yield
    app.dependency_overrides.clear()


@pytest_asyncio.fixture()
async def client(override_get_session):
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
