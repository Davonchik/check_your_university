from fastapi import APIRouter
from src.application.domain.admin import AuthAdmin, AdminResponse
from src.factories import AdminServiceAnnotated

router_admin = APIRouter(prefix="/admin", tags=["admins"])

@router_admin.post('/', response_model=AdminResponse)
async def login(admin_in: AuthAdmin, service: AdminServiceAnnotated):
    return await service.login(admin_in)

@router_admin.post('/refresh', response_model=AdminResponse)
async def refresh_token(refresh_token: str, service: AdminServiceAnnotated):
    return await service.refresh_token(refresh_token)