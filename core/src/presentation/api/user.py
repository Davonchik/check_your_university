from fastapi import APIRouter
from src.application.domain.user import UserCreate
from src.factories import UserServiceAnnotated
from src.factories import AdminServiceAnnotated

router_user = APIRouter(prefix="/user", tags=["users"])

@router_user.post('/', response_model=UserCreate)
async def create_new_user(user_in: UserCreate, service: UserServiceAnnotated):
    return await service.create_user(user_in)

@router_user.get('/get-buildings')
async def get_buildings(service: AdminServiceAnnotated):
    buildings = await service.get_buildings()
    res = []
    for building in buildings:
        res.append(building.name)
    return res