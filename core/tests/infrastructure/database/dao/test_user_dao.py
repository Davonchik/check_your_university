# from tests.test import db_session
# from src.infrastructure.database.models.user import User
# from src.application.domain.user import UserCreate
# from src.infrastructure.database.dao.user_dao import UserDao


# class TestUserDao:
#     user_dao = UserDao(db_session)
#     async def test_create_user(self, db_session):
#         user = UserCreate(tg_id='123')
        
#         user_out = await self.user_dao.create_user(user)
#         assert user_out.tg_id == '123'