from src.application.abstractions.dao.base import Dao
from abc import ABC, abstractmethod
from src.application.domain.user import UserCreate
from src.infrastructure.database.models.user import User

class IUserDao(Dao, ABC):
    @abstractmethod
    async def create_user(self, user_in: UserCreate) -> User:
        raise NotImplementedError
    