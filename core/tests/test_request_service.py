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

# @pytest.mark.asyncio
# async def test_create_request(session: AsyncSession, mocker):
#     # Создаем мок для RequestService
#     mock_service = mocker.MagicMock(spec=RequestService)

#     # Мокаем метод create_request в mock_service
#     mock_service.create_request = AsyncMock(return_value=Request(
#         id=1,
#         user_id=1,
#         building_id=1,
#         category="Repair",
#         room="101",
#         text="Fix the door"
#     ))

#     # Создаем тестового пользователя и здание
#     user = User(tg_id="12345")
#     building = Building(name="Test Building")
#     session.add(user)
#     session.add(building)
#     await session.commit()

#     # Создаем объект RequestCreate
#     request_in = RequestCreate(
#         user_id="12345",  # TG ID пользователя
#         building_name="Test Building",  # Название здания
#         category="Repair",  # Категория запроса
#         room="101",  # Комната
#         text="Fix the door"  # Текст запроса
#     )

#     # Вызываем метод create_request на mock_service
#     created_request = await mock_service.create_request(request_in)

#     # Проверяем, что запрос был создан
#     assert created_request is not None
#     assert created_request.id == 1
#     assert created_request.user_id == 1
#     assert created_request.building_id == 1
#     assert created_request.category == "Repair"
#     assert created_request.room == "101"
#     assert created_request.text == "Fix the door"

#     # Проверяем, что метод create_request был вызван с правильными аргументами
#     mock_service.create_request.assert_called_once_with(request_in)