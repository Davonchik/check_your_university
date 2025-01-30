import pytest
from src.factories import session_factory
from src.infrastructure.database.database import Base
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from src.infrastructure.database.dao.user_dao import UserDao
from src.application.domain.user import UserCreate
from src.infrastructure.database.models.user import User
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
import pytest_asyncio

test_database_url = "postgresql+asyncpg://test:test@test_database_container:5432/test"
engine = create_async_engine(test_database_url)
testing_session_local = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)

@pytest_asyncio.fixture()
async def session():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with testing_session_local() as session:
        yield session
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.mark.asyncio
async def test_create_user(session: AsyncSession):  
    dao = UserDao(session)
    user = await dao.create_user(UserCreate(tg_id="123"))
    assert user.tg_id == "123"
    querry = await session.execute(select(User).where(User.tg_id == "123"))
    assert querry.scalars().one().tg_id == "123"
