from src.application.abstractions.dao.i_admin_dao import IAdminDao
from src.infrastructure.database.models.admin import Admin
from sqlalchemy.future import select
from src.logger import logger

class AdminDao(IAdminDao):
    async def get_password_by_email(self, email: str) -> str:
        logger.info("Get password by email try")
        try:
            admin = await self.session.execute(select(Admin).where(Admin.email == email))
            return admin.scalars().one().password
        except Exception as e:
            logger.error(e)
            raise