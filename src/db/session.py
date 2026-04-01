from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.config import settings


engine = create_async_engine(settings.database_url, echo=True)

AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)
