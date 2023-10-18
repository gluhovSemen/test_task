from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base

from config import settings

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)

Base = declarative_base()


async def get_session():
    async with AsyncSession(
        bind=engine,
        expire_on_commit=False,
    ) as session:
        yield session
