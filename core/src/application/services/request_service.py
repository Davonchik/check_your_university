from src.application.abstractions.dao.i_request_dao import IRequestDao
from src.application.contracts.i_request_service import IRequestService
from src.application.domain.request import RequestCreate, RequestUpdate
from src.logger import logger

class RequestService(IRequestService):
    async def create_request(self, request_in: RequestCreate):
        logger.info("Create request try")
        try:
            return await self.request_dao.create_request(request_in)
        except Exception as e:
            logger.error(f"Exception in create request: {e}")
            raise

    async def get_requests(self):
        logger.info("Get requests try")
        try:
            return await self.request_dao.get_requests()
        except Exception as e:
            logger.error(f"Exception in get requests: {e}")
            raise
    

    async def update_request(self, request_id: int, request_in: RequestUpdate):
        logger.info("Update request try")
        try:
            return await self.request_dao.update_request(request_id, request_in)
        except Exception as e:
            logger.error(f"Exception in update request: {e}")
            raise