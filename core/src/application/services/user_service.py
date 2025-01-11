from src.application.abstractions.dao.i_user_dao import IUserDao
from src.application.contracts.i_user_service import IUserService
from src.application.domain.user import UserCreate
from src.logger import logger

class UserService(IUserService):
    async def create_user(self, user_in: UserCreate):
        logger.info("Create user try")
        try:
            return await self.user_dao.create_user(user_in)
        except Exception as e:
            logger.error(f"Exception in create user: {e}")
            raise
    
    # async def get_user(self, tg_id: str):
    #     return await self.user_dao.get_user(tg_id)