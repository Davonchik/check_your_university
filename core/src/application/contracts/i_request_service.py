from abc import ABC, abstractmethod
from src.application.contracts.base import Service
from src.application.abstractions.dao.i_request_dao import IRequestDao
from src.application.domain.request import RequestCreate, RequestUpdate

class IRequestService(Service, ABC):
    def __init__(self, request_dao: IRequestDao):
        self.request_dao = request_dao

    @abstractmethod
    async def create_request(self, request_in: RequestCreate):
        raise NotImplementedError
    
    @abstractmethod
    async def get_requests(self):
        raise NotImplementedError
    
    # @abstractmethod
    # async def get_request(self, request_id: int):
    #     raise NotImplementedError
    
    @abstractmethod
    async def update_request(self, request_id: int, request_in: RequestUpdate):
        raise NotImplementedError
    
    @abstractmethod
    async def delete_request(self, request_id: int):
        raise NotImplementedError
