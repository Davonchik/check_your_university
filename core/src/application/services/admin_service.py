from src.application.contracts.i_admin_service import IAdminService
from src.application.domain.admin import AuthAdmin
from src.infrastructure.utils.token_service import TokenService
from src.application.domain.admin import AdminResponse
from src.logger import logger

class AdminService(IAdminService):
    async def login(self, admin_in: AuthAdmin) -> str:
        logger.info("Login try")
        try:
            found_password = await self.admin_dao.get_password_by_email(admin_in.email)
            if found_password != admin_in.password:
                raise Exception("Invalid password")
            access_token = await TokenService.create_access_token(admin_in.email)
            refresh_token = await TokenService.create_refresh_token(admin_in.email)
            return AdminResponse(email=admin_in.email, access_token=access_token, refresh_token=refresh_token)
        except Exception as e:
            logger.error(f"Exception in login: {e}")
            raise
    
    async def refresh_token(self, refresh_token: str) -> str:
        logger.info("Update Token try")
        try:
            payload = await TokenService.decode_refresh_token(refresh_token)
            email = payload['sub']
            # добавить проверку refresh_token
            access_token = await TokenService.create_access_token(email)
            refresh_token = await TokenService.create_refresh_token(email)
            return AdminResponse(email=email, access_token=access_token, refresh_token=refresh_token)
        except Exception as e:
            logger.error(f"Exception in update token: {e}")
            raise

    async def create_building(self, name: str):
        logger.info("Create building try")
        return await self.building_dao.create_building(name=name)

    
    async def delete_building(self, id: int):
        logger.info("Delete building try")
        return await self.building_dao.delete_building(id=id)
