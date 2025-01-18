from src.application.contracts.i_s3_service import IS3Service
from src.logger import logger

class S3Service(IS3Service):
    async def create_file(self, user_id: int, file_name: str, file_content):
        logger.info("Create user try")
        try:
            print(self.s3_service.generate_url("image_report", file_name))
            file_url = self.s3_service.generate_url("image_report", file_name)
            self.s3_service.upload_file_object("image_report", file_name, file_content)
            return await self.s3_dao.create_file(user_id, file_name, file_url)
        except Exception as e:
            logger.error(f"Exception in create user: {e}")
            raise
    
    async def get_file_by_user_id(self, user_id: int):
        raise NotImplementedError

        
    