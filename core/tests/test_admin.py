import pytest
from src.factories import session_factory
from src.infrastructure.database.database import Base
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from src.infrastructure.database.dao.admin_dao import AdminDao
from src.application.domain.user import UserCreate
from src.infrastructure.database.models.admin import Admin
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
async def test_get_password_by_email(session: AsyncSession):
    dao = AdminDao(session)
    building = Building(name="pokra")
    admin = Admin(email="test", password="test", building=building)
    session.add(admin)
    await session.commit()
    password = await dao.get_password_by_email("test")
    assert password == "test"