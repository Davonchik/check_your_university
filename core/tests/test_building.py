import pytest
from src.factories import session_factory
from src.infrastructure.database.database import Base
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from src.infrastructure.database.dao.admin_dao import AdminDao
from src.infrastructure.database.dao.building_dao import BuildingDao
from src.application.domain.user import UserCreate
from src.infrastructure.database.models.admin import Admin
from src.infrastructure.database.models.building import Building
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
import pytest_asyncio

test_database_url = "postgresql+asyncpg://test:test@test_database_container:5432/test"

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
async def test_get_by_id(session: AsyncSession):
    dao = BuildingDao(session)
    building = Building(name="pokra")
    session.add(building)
    await session.commit()
    b_name = await dao.get_by_id(1)
    assert b_name == "pokra"

@pytest.mark.asyncio
async def test_create_building(session: AsyncSession):  
    dao = BuildingDao(session)
    building = await dao.create_building("pokra")
    assert building.name == "pokra"
    querry = await session.execute(select(Building).where(Building.name == "pokra"))
    assert querry.scalars().one().name == "pokra"

@pytest.mark.asyncio
async def test_delete_building(session: AsyncSession):  
    dao = BuildingDao(session)
    building = await dao.create_building("pokra")
    await dao.delete_building(building.id)
    querry = await session.execute(select(Building).where(Building.name == "pokra"))
    assert querry.scalars().one_or_none() is None

@pytest.mark.asyncio
async def test_get_id_by_name(session: AsyncSession):  
    dao = BuildingDao(session)
    building = await dao.create_building("pokra")
    id = await dao.get_id_by_name("pokra")
    assert id == 1

@pytest.mark.asyncio
async def test_get_buildings(session: AsyncSession):
    dao = BuildingDao(session)
    building = await dao.create_building("pokra")
    buildings = await dao.get_buildings()
    assert len(buildings) == 1
