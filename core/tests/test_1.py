import pytest
from src.infrastructure.database.database import Base
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine


# Создаём тестовую сессию
@pytest.fixture(scope='module')
async def test_db():
    # Создание базы данных в памяти
    engine = create_async_engine("postgresql+asyncpg://postgres:postgres@database_container:5432/postgres")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    TestingSessionLocal = async_sessionmaker(engine, class_=AsyncSession)
    
    # Контекст выполнения тестов
    yield TestingSessionLocal()
    
    # Чистка после тестов
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope='function')
async def db_session(test_db):
    # Получение сессии
    session = test_db
    try:
        yield session
    finally:
        await session.close()
    

from src.infrastructure.database.models.admin import Admin
from src.infrastructure.database.dao.admin_dao import AdminDao


class TestAdminDao:
    @pytest.mark.asyncio
    async def test_get_password_by_email(self, db_session):
        admin_dao = AdminDao(db_session)
        admin = Admin(email='player', password='12345')
        db_session.add(admin)
        await db_session.commit()
        
        password_out = await admin_dao.get_password_by_email('player')
        assert password_out == '12345'