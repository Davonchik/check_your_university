# from tests.test import db_session
# from src.infrastructure.database.models.admin import Admin
# from src.application.domain.admin import AuthAdmin
# from src.infrastructure.database.dao.admin_dao import AdminDao


# class TestAdminDao:
#     async def test_get_password_by_email(self, db_session):
#         admin_dao = AdminDao(db_session)
#         admin = Admin(email='player', password='12345')
#         db_session.add(admin)
#         await db_session.commit()
        
#         password_out = await admin_dao.get_password_by_email('player')
#         assert password_out == '12345'