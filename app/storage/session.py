import os

from dotenv import load_dotenv, find_dotenv
from sqlalchemy import URL
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

load_dotenv(find_dotenv())

DB_URL = URL.create(
    drivername='postgresql+asyncpg',
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    database=os.getenv("DB_NAME")
)

engine = create_async_engine(DB_URL)
SessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def get_db():
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()



async def create_tables():
    from app.storage.models import Base
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


if __name__ == '__main__':
    import asyncio
    asyncio.run(create_tables())
