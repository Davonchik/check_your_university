from src.application.abstractions.dao.i_request_dao import IRequestDao
from src.application.contracts.i_request_service import IRequestService
from src.application.domain.request import RequestCreate, RequestUpdate

class RequestService(IRequestService):
    async def create_request(self, request_in: RequestCreate):
        return await self.request_dao.create_request(request_in)

    async def get_requests(self):
        return await self.request_dao.get_requests()

    async def delete_request(self, request_id: int):
        return await self.request_dao.delete_request(request_id)
