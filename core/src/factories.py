from src.infrastructure.database.database import async_session_maker
from src.infrastructure.database.dao.request_dao import RequestDao
from src.infrastructure.database.dao.user_dao import UserDao
from src.infrastructure.database.dao.admin_dao import AdminDao
from src.infrastructure.database.dao.s3_dao import S3Dao
from src.infrastructure.database.dao.building_dao import BuildingDao
from src.application.services.request_service import RequestService
from src.application.services.user_service import UserService
from src.application.services.admin_service import AdminService
from src.application.services.s3_service import S3Service
from typing_extensions import Annotated
from src.application.contracts.i_request_service import IRequestService
from src.application.contracts.i_user_service import IUserService
from src.application.contracts.i_admin_service import IAdminService
from src.application.contracts.i_s3_service import IS3Service
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.utils.kafka_producer import KafkaProducer
from functools import lru_cache
from src.infrastructure.utils.s3_client import S3BucketService

async def session_factory():
    session = async_session_maker()
    try:
        yield session
    finally:
        await session.close()

@lru_cache
def kafka_producer_factory():
    return KafkaProducer(broker="kafka:9092", topic="test")

def s3_bucket_service_factory() -> S3BucketService:
    return S3BucketService(
        "test-bucket",
        "http://minio:9000",
        "USERNAME",
        "PASSWORD",
    )

async def s3_dao_factory(session: AsyncSession = Depends(session_factory)):
    return S3Dao(session)

async def user_dao_factory(session: AsyncSession = Depends(session_factory)):
    return UserDao(session)

async def s3_service_factory(dao: S3Dao = Depends(s3_dao_factory), s3_bucket_service: S3BucketService = Depends(s3_bucket_service_factory), user_dao: UserDao = Depends(user_dao_factory)):
    return S3Service(dao, s3_bucket_service, user_dao)

async def request_dao_factory(session: AsyncSession = Depends(session_factory)):
    return RequestDao(session)

async def building_dao_factory(session: AsyncSession = Depends(session_factory)):
    return BuildingDao(session)

async def request_service_factory(dao: RequestDao = Depends(request_dao_factory), kafka_producer: KafkaProducer = Depends(kafka_producer_factory), 
                                  user_dao: UserDao = Depends(user_dao_factory), building_dao: BuildingDao = Depends(building_dao_factory)):
    return RequestService(dao, kafka_producer, user_dao, building_dao)

async def user_service_factory(dao: UserDao = Depends(user_dao_factory)):
    return UserService(dao)

async def admin_dao_factory(session: AsyncSession = Depends(session_factory)):
    return AdminDao(session)

async def admin_service_factory(dao: AdminDao = Depends(admin_dao_factory), building_dao: BuildingDao = Depends(building_dao_factory)):
    return AdminService(dao, building_dao)

RequestServiceAnnotated = Annotated[IRequestService, Depends(request_service_factory)]
UserServiceAnnotated = Annotated[IUserService, Depends(user_service_factory)]
AdminServiceAnnotated = Annotated[IAdminService, Depends(admin_service_factory)]
S3BucketServiceAnnotated = Annotated[S3BucketService, Depends(s3_bucket_service_factory)]
S3ServiceAnnotated = Annotated[IS3Service, Depends(s3_service_factory)]
