from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

engine = create_async_engine("postgresql+asyncpg://postgres:postgres@database_container:5432/postgres")
async_session_maker = async_sessionmaker(engine, class_=AsyncSession)

class Base(DeclarativeBase):
    pass

async def get_session():
    session = async_session_maker()
    try:
        yield session
    finally:
        await session.close()
