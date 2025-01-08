from src.application.domain.user import UserCreate
from src.infrastructure.database.models.user import User
from src.application.abstractions.dao.i_user_dao import IUserDao

class UserDao(IUserDao):
    async def create_user(self, user_in: UserCreate) -> User:
        user = User(**user_in.dict())
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user