from src.application.abstractions.dao.base import Dao
from abc import ABC, abstractmethod
from src.application.domain.request import RequestCreate
from src.infrastructure.database.models.request import Request

class IRequestDao(Dao, ABC):
    @abstractmethod
    async def create_request(self, request_in: RequestCreate) -> Request:
        raise NotImplementedError
    
    @abstractmethod
    async def get_requests(self) -> list[Request]:
        raise NotImplementedError
    
    # @abstractmethod
    # async def get_request(self, request_id: int) -> Request:
    #     raise NotImplementedError
    
    @abstractmethod
    async def update_request(self, request_id: int, request_in: RequestCreate) -> Request:
        raise NotImplementedError
    
    @abstractmethod
    async def delete_request(self, request_id: int):
        raise NotImplementedError
        