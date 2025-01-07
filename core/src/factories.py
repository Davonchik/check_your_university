from src.infrastructure.database.database import async_session_maker
from src.infrastructure.database.dao.request_dao import RequestDao
from src.application.services.request_service import RequestService
from typing_extensions import Annotated
from src.application.contracts.i_request_service import IRequestService
from fastapi import Depends

def session_factory():
    session = async_session_maker()
    try:
        return session
    finally:
        session.close()

async def request_dao_factory():
    session = session_factory()
    return RequestDao(session)

async def request_service_factory():
    dao = await request_dao_factory()
    return RequestService(dao)

RequestServiceAnnotated = Annotated[IRequestService, Depends(request_service_factory)]
