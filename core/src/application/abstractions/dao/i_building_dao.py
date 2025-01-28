from src.application.abstractions.dao.base import Dao
from abc import ABC, abstractmethod

class IBuildingDao(Dao, ABC):
    @abstractmethod
    async def get_by_id(self, id: int):
        raise NotImplementedError
    
    @abstractmethod
    async def create_building(self, name: str):
        raise NotImplementedError
    
    @abstractmethod
    async def delete_building(self, id: int):
        raise NotImplementedError
    
    @abstractmethod
    async def get_id_by_name(self, name: str):
        raise NotImplementedError
    
    @abstractmethod
    async def get_buildings(self):
        raise NotImplementedError
