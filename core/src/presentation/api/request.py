from fastapi import APIRouter
from src.application.domain.request import RequestCreate, RequestOut, RequestUpdate
from src.factories import RequestServiceAnnotated

router = APIRouter(prefix="/request", tags=["requests"])

@router.post('/', response_model=RequestOut)
async def create_new_request(request_in: RequestCreate, service: RequestServiceAnnotated):
    return await service.create_request(request_in)


