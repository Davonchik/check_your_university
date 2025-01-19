from abc import ABC, abstractmethod
from src.application.contracts.base import Service
from src.application.abstractions.dao.i_s3_dao import IS3Dao
from src.infrastructure.utils.s3_client import S3BucketService
from src.application.abstractions.dao.i_user_dao import IUserDao



class IS3Service(Service, ABC):
    def __init__(self, s3_dao: IS3Dao, s3_service: S3BucketService, user_dao: IUserDao):
        self.s3_dao = s3_dao
        self.s3_service = s3_service
        self.user_dao = user_dao

    @abstractmethod
    async def create_file(self, user_id: int, file_name: str, file_content):
        raise NotImplementedError
    
    @abstractmethod
    async def get_file_by_user_id(self, user_id: int):
        raise NotImplementedError
        
    