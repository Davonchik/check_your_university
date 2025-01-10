from src.application.abstractions.dao.i_admin_dao import IAdminDao
from src.infrastructure.database.models.admin import Admin
from sqlalchemy.future import select

class AdminDao(IAdminDao):
    async def get_password_by_email(self, email: str) -> str:
        admin = await self.session.execute(select(Admin).where(Admin.email == email))
        return admin.scalars().one().password