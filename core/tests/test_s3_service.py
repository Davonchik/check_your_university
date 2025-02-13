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
from src.application.services.s3_service import S3Service
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
import pytest_asyncio
from unittest.mock import AsyncMock, MagicMock

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
async def test_create_file():
    # Arrange
    user_dao = AsyncMock()
    s3_service = MagicMock()
    s3_dao = AsyncMock()

    user_dao.get_id_by_tg_id.return_value = 123
    s3_service.generate_url.return_value = "https://s3.example.com/image_report/test_file.jpg"
    s3_dao.create_file.return_value = {"file_id": 1, "file_name": "test_file.jpg", "file_url": "https://s3.example.com/image_report/test_file.jpg"}

    service = S3Service(
        user_dao=user_dao,
        s3_service=s3_service,
        s3_dao=s3_dao
    )

    user_id = 123
    file_name = "test_file.jpg"
    file_content = b"test_file_content"

    # Act
    result = await service.create_file(user_id, file_name, file_content)

    # Assert
    user_dao.get_id_by_tg_id.assert_called_once_with(str(user_id))

    s3_service.upload_file_object.assert_called_once_with("image_report", file_name, file_content)

    s3_service.generate_url.assert_called_once_with("image_report", file_name)

    s3_dao.create_file.assert_called_once_with(123, file_name, "https://s3.example.com/image_report/test_file.jpg")

    assert result == {"file_id": 1, "file_name": "test_file.jpg", "file_url": "https://s3.example.com/image_report/test_file.jpg"}
