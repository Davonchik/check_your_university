from fastapi import APIRouter
from src.application.domain.request import RequestCreate, RequestOut, RequestUpdate
from src.factories import RequestServiceAnnotated

router = APIRouter(prefix="/request", tags=["requests"])

@router.post('/', response_model=RequestOut)
async def create_new_request(request_in: RequestCreate, service: RequestServiceAnnotated):
    return await service.create_request(request_in)

@router.post('/update', response_model=RequestUpdate)
async def update_request(request_id: int, request_in: RequestUpdate, service: RequestServiceAnnotated):
    return await service.update_request(request_id, request_in)

