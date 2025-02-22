import pytest
from src.factories import session_factory
from src.infrastructure.database.database import Base
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from src.application.domain.admin import AuthAdmin
from src.infrastructure.database.dao.admin_dao import AdminDao
from src.infrastructure.database.dao.user_dao import UserDao
from src.infrastructure.database.dao.request_dao import RequestDao
from src.infrastructure.database.dao.building_dao import BuildingDao
from src.application.services.request_service import RequestService
from src.application.domain.request import RequestCreate
from src.application.domain.request import RequestUpdate
from src.application.domain.admin import AuthAdmin
from src.application.domain.admin import AdminResponse
from src.application.domain.user import UserCreate
from src.infrastructure.database.models.admin import Admin
from src.infrastructure.database.models.user import User
from src.infrastructure.database.models.request import Request
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
async def test_create_request_success(session: AsyncSession):
    # Arrange
    user_dao = UserDao(session)
    building_dao = BuildingDao(session)
    request_dao = RequestDao(session)

    kafka_producer = AsyncMock()

    service = RequestService(
        user_dao=user_dao, 
        building_dao=building_dao, 
        request_dao=request_dao,
        kafka_producer=kafka_producer
    )

    # Создаем тестовые данные
    test_user = User(tg_id=123)
    test_building = Building(name="main_building")
    
    session.add_all([test_user, test_building])
    await session.commit()
    await session.refresh(test_user)
    await session.refresh(test_building)

    request_in = RequestCreate(
        user_id=123,
        building_name="main_building",
        category="repair",
        room="305",
        text="Broken window"
    )

    # Act
    result = await service.create_request(request_in)
    
    # Assert
    assert result is not None
    
    # Проверяем запись в БД
    db_request = await request_dao.get_request_by_id(result.id)
    assert db_request.user_id == test_user.id
    assert db_request.building_id == test_building.id
    assert db_request.category == "repair"
    assert db_request.room == "305"
    assert db_request.text == "Broken window"

@pytest.mark.asyncio
async def test_create_request_invalid_user(session: AsyncSession):
    kafka_producer = AsyncMock()

    # Arrange
    service = RequestService(
        user_dao=UserDao(session),
        building_dao=BuildingDao(session),
        request_dao=RequestDao(session),
        kafka_producer=kafka_producer  # Передаем мок
    )

    request_in = RequestCreate(
        user_id=4,
        building_name="main_building",
        category="repair",
        room="305",
        text="Broken window"
    )

    # Act & Assert
    with pytest.raises(Exception):
        await service.create_request(request_in)

@pytest.mark.asyncio
async def test_create_request_invalid_building(session: AsyncSession):
    kafka_producer = AsyncMock()

    # Arrange
    test_user = User(tg_id=12)
    session.add(test_user)
    await session.commit()

    service = RequestService(
        user_dao=UserDao(session),
        building_dao=BuildingDao(session),
        request_dao=RequestDao(session),
        kafka_producer=kafka_producer  # Передаем мок
    )

    request_in = RequestCreate(
        user_id=12,
        building_name="non_existent_building",
        category="repair",
        room="305",
        text="Broken window"
    )

    # Act & Assert
    with pytest.raises(Exception):
        await service.create_request(request_in)

@pytest.mark.asyncio
async def test_get_requests():
    # Arrange
    request_dao = AsyncMock()

    test_building = Building(id=1, name="main_building")
    test_request_1 = Request(
        id=1,
        user_id=123,
        building=test_building,
        category="repair",
        room="305",
        text="Broken window",
        status="open"
    )
    test_request_2 = Request(
        id=2,
        user_id=456,
        building=test_building,
        category="cleaning",
        room="101",
        text="Clean the room",
        status="closed"
    )

    # Настраиваем мок, чтобы он возвращал тестовые данные
    request_dao.get_requests.return_value = [test_request_1, test_request_2]

    service = RequestService(
        request_dao=request_dao,
        user_dao=AsyncMock(),
        building_dao=AsyncMock(),
        kafka_producer=AsyncMock()
    )

    # Act
    result = await service.get_requests()

    # Assert
    assert len(result) == 2  # Проверяем, что вернулось два элемента

    assert result[0].id == 1
    assert result[0].user_id == 123
    assert result[0].building_name == "main_building"
    assert result[0].category == "repair"
    assert result[0].room == "305"
    assert result[0].text == "Broken window"
    assert result[0].status == "open"

    assert result[1].id == 2
    assert result[1].user_id == 456
    assert result[1].building_name == "main_building"
    assert result[1].category == "cleaning"
    assert result[1].room == "101"
    assert result[1].text == "Clean the room"
    assert result[1].status == "closed"

    request_dao.get_requests.assert_called_once()


@pytest.mark.asyncio
async def test_get_statistics():
    # Arrange
    request_dao = AsyncMock()
    request_dao.get_statistics.return_value = {"total": 10, "closed": 5}

    service = RequestService(
        request_dao=request_dao,
        user_dao=AsyncMock(),
        building_dao=AsyncMock(),
        kafka_producer=AsyncMock()
    )

    # Act
    result = await service.get_statistics()

    # Assert
    assert result == {"total": 10, "closed": 5}
    request_dao.get_statistics.assert_called_once()

@pytest.mark.asyncio
async def test_get_request_by_id():
    # Arrange
    request_dao = AsyncMock()
    test_request = Request(id=1, user_id=123, building=Building(name="main_building"), category="repair", room="305", text="Broken window", status="open")
    request_dao.get_request_by_id.return_value = test_request

    service = RequestService(
        request_dao=request_dao,
        user_dao=AsyncMock(),
        building_dao=AsyncMock(),
        kafka_producer=AsyncMock()
    )

    # Act
    result = await service.get_request_by_id(request_id=1)

    # Assert
    assert result == test_request
    request_dao.get_request_by_id.assert_called_once_with(1)

@pytest.mark.asyncio
async def test_update_request():
    # Arrange
    request_dao = AsyncMock()
    kafka_producer = AsyncMock()

    # Мок обновленного запроса
    test_user = User(tg_id="test_tg_123")
    test_request = Request(id=1, user=test_user, building=Building(name="main_building"), category="repair", room="305", text="Broken window", status="closed")
    request_dao.update_request.return_value = test_request

    service = RequestService(
        request_dao=request_dao,
        user_dao=AsyncMock(),
        building_dao=AsyncMock(),
        kafka_producer=kafka_producer
    )

    # Мок входных данных для обновления
    request_in = RequestUpdate(request_id=1, status="closed")

    # Act
    result = await service.update_request(request_id=request_in.request_id, request_in=request_in)

    # Assert
    assert result == test_request
    request_dao.update_request.assert_called_once_with(1, request_in)
    kafka_producer.send_message.assert_called_once_with("test_tg_123 closed")

@pytest.mark.asyncio
async def test_filter_by_building():
    # Arrange
    request_dao = AsyncMock()
    test_requests = [
        Request(id=1, user_id=123, building=Building(name="main_building"), category="repair", room="305", text="Broken window", status="open"),
        Request(id=2, user_id=456, building=Building(name="main_building"), category="cleaning", room="101", text="Clean the room", status="closed")
    ]
    request_dao.filter_by_building.return_value = test_requests  # Мок запросов

    service = RequestService(
        request_dao=request_dao,
        user_dao=AsyncMock(),
        building_dao=AsyncMock(),
        kafka_producer=AsyncMock()
    )

    # Act
    result = await service.filter_by_building(building_name="main_building")

    # Assert
    assert result == test_requests
    request_dao.filter_by_building.assert_called_once_with("main_building")
    