from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from config import config

Base = DeclarativeBase()

engine = create_async_engine(config.database_url, echo=True)

AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)
