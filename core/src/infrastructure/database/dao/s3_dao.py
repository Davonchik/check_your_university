from src.application.abstractions.dao.i_s3_dao import IS3Dao
from src.infrastructure.database.models.s3 import S3
from src.logger import logger


class S3Dao(IS3Dao):
    async def create_file(self, user_id: int, file_name: str, file_url: str):
        logger.info("Create user try")
        try:
            
            s3 = S3(user_id=user_id, file_name=file_name, file_url=file_url)
            self.session.add(s3)
            await self.session.commit()
            await self.session.refresh(s3)
            return s3
        except Exception as e:
            logger.error(f"Exception in create user: {e}")
            raise
    
    
    async def get_file_by_user_id(self, user_id: int):
        raise NotImplementedError
