from src.application.abstractions.dao.base import Dao
from abc import ABC, abstractmethod


class IS3Dao(Dao, ABC):
    @abstractmethod
    async def create_file(self, user_id: int, file_name: str, file_url: str):
        raise NotImplementedError
    
    @abstractmethod
    async def get_file_by_user_id(self, user_id: int):
        raise NotImplementedError