from src.application.abstractions.dao.base import Dao
from abc import ABC, abstractmethod
from src.application.domain.admin import AuthAdmin


class IAdminDao(Dao, ABC):
    @abstractmethod
    async def get_password_by_email(self, email: str) -> str:
        raise NotImplementedError
    
    