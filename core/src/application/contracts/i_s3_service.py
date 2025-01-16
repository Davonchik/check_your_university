from abc import ABC, abstractmethod
from src.application.contracts.base import Service
from src.application.abstractions.dao.i_s3_dao import IS3Dao



class IAdminService(Service, ABC):
    def __init__(self, s3_dao: IS3Dao):
        self.s3_dao = s3_dao
        
    