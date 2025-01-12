from fastapi import APIRouter
from src.application.domain.request import RequestUpdate
from src.factories import RequestServiceAnnotated
from src.application.domain.annotated import TokenAnnotated

router_admin_actions = APIRouter(prefix="/admin_actions", tags=["actions"])

@router_admin_actions.post('/update', response_model=RequestUpdate)
async def update_request(request_id: int, request_in: RequestUpdate, service: RequestServiceAnnotated, _: TokenAnnotated):
    return await service.update_request(request_id, request_in)
