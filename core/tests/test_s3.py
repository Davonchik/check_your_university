import pytest
from src.factories import session_factory
from src.infrastructure.database.database import Base
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from src.infrastructure.database.dao.admin_dao import AdminDao
from src.infrastructure.database.dao.s3_dao import S3Dao
from src.infrastructure.database.dao.building_dao import BuildingDao
from src.application.domain.user import UserCreate
from src.infrastructure.database.models.admin import Admin
from src.infrastructure.database.models.s3 import S3
from src.infrastructure.database.models.user import User
from src.infrastructure.database.models.building import Building
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
import pytest_asyncio

test_database_url = "sqlite+aiosqlite:///:memory:"

@pytest_asyncio.fixture()
async def session():
    engine = create_async_engine(test_database_url)
    testing_session_local = sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with testing_session_local() as session:
        yield session
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.mark.asyncio
async def test_create_file(session: AsyncSession):
    dao = S3Dao(session)
    user = User(tg_id="123user")
    session.add(user)
    await session.commit()
    await session.refresh(user)

    s3 = await dao.create_file(user_id=user.id, file_name="test", file_url="test_url")
    assert s3.file_name == "test"