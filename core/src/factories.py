from src.infrastructure.database.database import async_session_maker
from src.infrastructure.database.dao.request_dao import RequestDao
from src.infrastructure.database.dao.user_dao import UserDao
from src.infrastructure.database.dao.admin_dao import AdminDao
from src.application.services.request_service import RequestService
from src.application.services.user_service import UserService
from src.application.services.admin_service import AdminService
from typing_extensions import Annotated
from src.application.contracts.i_request_service import IRequestService
from src.application.contracts.i_user_service import IUserService
from src.application.contracts.i_admin_service import IAdminService
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

async def session_factory():
    session = async_session_maker()
    try:
        yield session
    finally:
        await session.close()

async def request_dao_factory(session: AsyncSession = Depends(session_factory)):
    return RequestDao(session)

async def request_service_factory(dao: RequestDao = Depends(request_dao_factory)):
    return RequestService(dao)

async def user_dao_factory(session: AsyncSession = Depends(session_factory)):
    return UserDao(session)

async def user_service_factory(dao: UserDao = Depends(user_dao_factory)):
    return UserService(dao)

async def admin_dao_factory(session: AsyncSession = Depends(session_factory)):
    return AdminDao(session)

async def admin_service_factory(dao: AdminDao = Depends(admin_dao_factory)):
    return AdminService(dao)

RequestServiceAnnotated = Annotated[IRequestService, Depends(request_service_factory)]
UserServiceAnnotated = Annotated[IUserService, Depends(user_service_factory)]
AdminServiceAnnotated = Annotated[IAdminService, Depends(admin_service_factory)]
