from abc import ABC, abstractmethod
from src.application.contracts.base import Service
from src.application.abstractions.dao.i_admin_dao import IAdminDao
from src.application.domain.admin import AuthAdmin


class IAdminService(Service, ABC):
    def __init__(self, admin_dao: IAdminDao):
        self.admin_dao = admin_dao
        
    @abstractmethod
    async def login(self, admin_in: AuthAdmin) -> str:
        raise NotImplementedError