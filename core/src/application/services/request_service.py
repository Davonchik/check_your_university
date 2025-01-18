from src.application.abstractions.dao.i_request_dao import IRequestDao
from src.application.contracts.i_request_service import IRequestService
from src.application.domain.request import RequestCreate, RequestUpdate
from src.logger import logger
from src.application.domain.admin import StatusUpdate

class RequestService(IRequestService):
    async def create_request(self, request_in: RequestCreate):
        logger.info("Create request try")
        try:
            request_in.user_id = await self.user_dao.get_id_by_tg_id(str(request_in.user_id))
            
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

    async def get_request_by_id(self, request_id: int):
        logger.info("Get request by id try")
        try:
            return await self.request_dao.get_request_by_id(request_id)
        except Exception as e:
            logger.error(f"Exception in get request by id: {e}")
            raise

    async def update_request(self, request_id: int, request_in: RequestUpdate):
        logger.info("Update request try")
        try:
            request = await self.request_dao.update_request(request_id, request_in)
            print(request.user)
            self.kafka_producer.send_message(str(request.user.tg_id) + ' ' + str(request.status))
            return request
        except Exception as e:
            logger.error(f"Exception in update request: {e}")
            raise