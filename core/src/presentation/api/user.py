from fastapi import APIRouter
from src.application.domain.user import UserCreate
from src.factories import UserServiceAnnotated

router2 = APIRouter(prefix="/user", tags=["users"])

@router2.post('/', response_model=UserCreate)
def create_new_user(user_in: UserCreate, service: UserServiceAnnotated):
    return service.create_user(user_in)