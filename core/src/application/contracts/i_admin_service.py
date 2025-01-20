from abc import ABC, abstractmethod
from src.application.contracts.base import Service
from src.application.abstractions.dao.i_admin_dao import IAdminDao
from src.application.abstractions.dao.i_building_dao import IBuildingDao
from src.application.domain.admin import AuthAdmin


class IAdminService(Service, ABC):
    def __init__(self, admin_dao: IAdminDao, building_dao: IBuildingDao):
        self.admin_dao = admin_dao
        self.building_dao = building_dao
        
    @abstractmethod
    async def login(self, admin_in: AuthAdmin) -> str:
        raise NotImplementedError
    
    @abstractmethod
    async def create_building(self, name: str):
        raise NotImplementedError
    
    @abstractmethod
    async def delete_building(self, id: int):
        raise NotImplementedError