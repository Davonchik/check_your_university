from src.application.domain.request import RequestCreate
from src.infrastructure.database.models.request import Request
from src.application.abstractions.dao.i_request_dao import IRequestDao
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound

class RequestDao(IRequestDao):
    async def create_request(self, request_in: RequestCreate) -> Request:
        request = Request(**request_in.dict())
        self.session.add(request)
        await self.session.commit()
        await self.session.refresh(request)
        return request
    
    async def get_requests(self) -> list[Request]:
        return await self.session.query(Request).all()
    
<<<<<<< HEAD
    async def delete_request(self, request_id: int):
        query = select(Request).where(Request.id == request_id)
        result = await self.session.execute(query)
        request_to_delete = result.scalar_one_or_none()
        if not request_to_delete:
            raise NoResultFound(f"Request with id {request_id} not found.")
        await self.session.delete(request_to_delete)
        await self.session.commit()
        return request_to_delete
=======
    async def update_request(self, request_id: int, request_in: RequestCreate) -> Request:
        query = select(Request).where(Request.id == request_id)
        result = await self.session.execute(query)
        existing_request = result.scalar_one_or_none()
        if not existing_request:
            return NoResultFound(f"Request with id {request_id} not found")
        
        for key, value in request_in.dict().items():    
            setattr(existing_request, key, value)
        
        self.session.add(existing_request)
        await self.session.commit()
        await self.session.refresh(existing_request)
        return existing_request
>>>>>>> update_method_feature
