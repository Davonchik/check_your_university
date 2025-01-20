from abc import ABC, abstractmethod
from src.application.contracts.base import Service
from src.application.abstractions.dao.i_request_dao import IRequestDao
from src.application.abstractions.dao.i_user_dao import IUserDao
from src.application.abstractions.dao.i_building_dao import IBuildingDao
from src.application.domain.request import RequestCreate, RequestUpdate
from src.application.domain.admin import StatusUpdate
from src.infrastructure.utils.kafka_producer import KafkaProducer

class IRequestService(Service, ABC):
    def __init__(self, request_dao: IRequestDao, kafka_producer: KafkaProducer, user_dao: IUserDao, building_dao: IBuildingDao):
        self.request_dao = request_dao
        self.kafka_producer = kafka_producer
        self.user_dao = user_dao
        self.building_dao = building_dao

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