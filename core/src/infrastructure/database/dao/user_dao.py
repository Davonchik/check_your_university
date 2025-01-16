from src.application.domain.user import UserCreate
from src.infrastructure.database.models.user import User
from src.application.abstractions.dao.i_user_dao import IUserDao
from src.logger import logger
from sqlalchemy.future import select

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

    async def get_id_by_tg_id(self, tg_id: str) -> int:
        logger.info("Get id by tg id try")
        try:
            user = await self.session.execute(select(User).where(User.tg_id == tg_id))
            return user.scalars().one().id
        except Exception as e:
            logger.error(f"Exception in get id by tg id: {e}")
            raise
  