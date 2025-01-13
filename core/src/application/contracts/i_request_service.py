from abc import ABC, abstractmethod
from src.application.contracts.base import Service
from src.application.abstractions.dao.i_request_dao import IRequestDao
from src.application.domain.request import RequestCreate, RequestUpdate
from src.application.domain.admin import StatusUpdate
from src.infrastructure.utils.kafka_producer import KafkaProducer

class IRequestService(Service, ABC):
    def __init__(self, request_dao: IRequestDao, kafka_producer: KafkaProducer):
        self.request_dao = request_dao
        self.kafka_producer = kafka_producer

    @abstractmethod
    async def create_request(self, request_in: RequestCreate):
        raise NotImplementedError
    
    @abstractmethod
    async def get_requests(self):
        raise NotImplementedError
    
    @abstractmethod
    async def get_request_by_id(self, request_id: int):
        raise NotImplementedError
    
    # @abstractmethod
    # async def get_request(self, request_id: int):
    #     raise NotImplementedError
    
    @abstractmethod
    async def update_request(self, request_id: int, request_in: RequestUpdate):
        raise NotImplementedError
    
    # @abstractmethod
    # async def delete_request(self, request_id: int):
    #     raise NotImplementedError