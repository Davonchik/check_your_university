import pytest
from src.factories import session_factory
from src.infrastructure.database.database import Base
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from src.infrastructure.database.dao.user_dao import UserDao
from src.infrastructure.database.dao.admin_dao import AdminDao
from src.infrastructure.database.dao.building_dao import BuildingDao
from src.infrastructure.database.dao.request_dao import RequestDao
from src.application.domain.user import UserCreate
from src.application.domain.request import RequestCreate, RequestDto, RequestUpdate
from src.infrastructure.database.models.request import Request
from src.infrastructure.database.models.user import User
from src.infrastructure.database.models.admin import Admin
from src.infrastructure.database.models.building import Building
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
import pytest_asyncio
from unittest.mock import AsyncMock

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
async def test_create_request(session: AsyncSession):
    dao = RequestDao(session)
    user_dao = UserDao(session)
    building_dao = BuildingDao(session)

    user = User(tg_id="123user")
    building = Building(name="pokra")
    session.add(user)
    session.add(building)
    await session.commit()
    await session.refresh(user)
    await session.refresh(building)

    request_in = RequestCreate(
        user_id=user.id,
        building_name="pokra",
        category="test",
        room="test",
        text="test"
    )
    
    building_id = await building_dao.get_id_by_name(request_in.building_name)
    dto = RequestDto(user_id=request_in.user_id, building_id=building_id, 
                        category=request_in.category, room=request_in.room, text=request_in.text)
    
    req = await dao.create_request(dto)
    assert req.user_id == user.id

@pytest.mark.asyncio
async def test_get_requests(session: AsyncSession):
    # Arrange
    request_dao = RequestDao(session)

    # Мок для выполнения запроса
    mock_request = Request(id=1, user_id=1, building_id=1, category="repair", room="305", text="Broken window", status="open")
    
    session.add(mock_request)
    await session.commit()
    await session.refresh(mock_request)

    # Act
    result = await request_dao.get_requests()

    # Assert
    assert len(result) == 1
    assert isinstance(result[0], Request)

@pytest.mark.asyncio
async def test_update_request(session: AsyncSession):
    # Arrange
    request_dao = RequestDao(session)

    # Мок для выполнения запроса
    mock_request = Request(id=1, user_id=1, building_id=1, category="repair", room="305", text="Broken window", status="open")
    session.add(mock_request)
    await session.commit()
    await session.refresh(mock_request)

    # Act
    result = await request_dao.update_request(1, RequestUpdate(status="closed"))

    # Assert
    assert result.status == "closed"

@pytest.mark.asyncio
async def test_filter_by_building(session: AsyncSession):
    # Arrange
    request_dao = RequestDao(session)

    # Мок для выполнения запроса
    mock_request = Request(id=1, user_id=1, building_id=1, category="repair", room="305", text="Broken window", status="open")
    session.add(mock_request)
    await session.commit()
    await session.refresh(mock_request)

    # Act
    result = await request_dao.filter_by_building("main_building")

    # Assert
    assert len(result) == 0
