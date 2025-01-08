from src.application.abstractions.dao.i_user_dao import IUserDao
from src.application.contracts.i_user_service import IUserService
from src.application.domain.user import UserCreate

class UserService(IUserService):
    async def create_user(self, user_in: UserCreate):
        return await self.user_dao.create_user(user_in)
    
    # async def get_user(self, tg_id: str):
    #     return await self.user_dao.get_user(tg_id)