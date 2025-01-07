from src.application.domain.request import RequestCreate
from src.infrastructure.database.models.request import Request
from src.application.abstractions.dao.i_request_dao import IRequestDao

class RequestDao(IRequestDao):
    async def create_request(self, request_in: RequestCreate) -> Request:
        request = Request(**request_in.dict())
        self.session.add(request)
        await self.session.commit()
        await self.session.refresh(request)
        return request
    
    async def get_requests(self) -> list[Request]:
        return await self.session.query(Request).all()
    
    
