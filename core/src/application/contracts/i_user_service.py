from abc import ABC, abstractmethod
from src.application.contracts.base import Service
from src.application.abstractions.dao.i_user_dao import IUserDao
from src.application.domain.user import UserCreate

class IUserService(Service, ABC):
    def __init__(self, user_dao: IUserDao):
        self.user_dao = user_dao

    @abstractmethod
    async def create_user(self, user_in: UserCreate):
        raise NotImplementedError