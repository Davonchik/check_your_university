import pytest
from src.factories import session_factory
from src.infrastructure.database.database import Base
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from src.application.domain.admin import AuthAdmin
from src.infrastructure.database.dao.admin_dao import AdminDao
from src.infrastructure.database.dao.building_dao import BuildingDao
from src.application.services.admin_service import AdminService
from src.application.domain.admin import AuthAdmin
from src.application.domain.admin import AdminResponse
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
async def test_login(session: AsyncSession):
    admin_dao = AdminDao(session)
    building_dao = BuildingDao(session)
    service = AdminService(admin_dao, building_dao)
    
    building = Building(name="pokra")
    admin = Admin(email="test", password="1111", building=building)
    session.add(admin)
    await session.commit()

    admin_in = AuthAdmin(
        email='test',
        password='1111'
    )
    response = await service.login(admin_in)
    assert response.email == admin_in.email
    assert response.access_token != None
    assert response.refresh_token != None

@pytest.mark.asyncio
async def test_create_building(session: AsyncSession):
    admin_dao = AdminDao(session)
    building_dao = BuildingDao(session)
    service = AdminService(admin_dao, building_dao)

    building = await service.create_building("pokra")
    query = await session.execute(select(Building))

    buildings = query.scalars().all()

    assert len(buildings) == 1
    assert buildings[0].name == building.name

@pytest.mark.asyncio
async def test_delete_building(session: AsyncSession):
    admin_dao = AdminDao(session)
    building_dao = BuildingDao(session)
    service = AdminService(admin_dao, building_dao)

    building = await service.create_building("pokra")

    query = await session.execute(select(Building))
    buildings = query.scalars().all()
    assert len(buildings) == 1
    assert buildings[0].name == "pokra"

    await service.delete_building(building.id)

    query = await session.execute(select(Building))
    buildings = query.scalars().all()
    assert len(buildings) == 0

@pytest.mark.asyncio
async def test_get_buildings(session: AsyncSession):
    admin_dao = AdminDao(session)
    building_dao = BuildingDao(session)
    service = AdminService(admin_dao, building_dao)

    buildingA = await service.create_building("Building A")
    buildingB = await service.create_building("Building B")

    buildings = await service.get_buildings()

    assert len(buildings) == 2
    assert buildings[0].name == "Building A"
    assert buildings[1].name == "Building B"