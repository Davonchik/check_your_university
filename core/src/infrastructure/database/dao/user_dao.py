from src.application.domain.user import UserCreate
from src.infrastructure.database.models.user import User
from src.application.abstractions.dao.i_user_dao import IUserDao
from src.logger import logger

class UserDao(IUserDao):
    async def create_user(self, user_in: UserCreate) -> User:
        logger.info("Create user try")
        try:
            user = User(**user_in.dict())
            self.session.add(user)
            await self.session.commit()
            await self.session.refresh(user)
            return user
        except Exception as e:
            logger.error(f"Exception in create user: {e}")
            raise
  