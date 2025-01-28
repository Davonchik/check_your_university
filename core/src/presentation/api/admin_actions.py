from fastapi import APIRouter
from src.application.domain.request import RequestUpdate
from src.factories import RequestServiceAnnotated, AdminServiceAnnotated
from src.application.domain.annotated import TokenAnnotated

router_admin_actions = APIRouter(prefix="/admin_actions", tags=["actions"])

@router_admin_actions.post('/update', response_model=RequestUpdate)
async def update_request(request_id: int, request_in: RequestUpdate, service: RequestServiceAnnotated, _: TokenAnnotated):
    return await service.update_request(request_id, request_in)


@router_admin_actions.post('/create-building')
async def create_building(name: str, service: AdminServiceAnnotated, _: TokenAnnotated):
    return await service.create_building(name=name)

@router_admin_actions.post('/delete-building')
async def delete_building(id: int, service: AdminServiceAnnotated, _: TokenAnnotated):
    return await service.delete_building(id=id)

@router_admin_actions.get('/')
async def get_requests(service: RequestServiceAnnotated, _: TokenAnnotated):
    requests = await service.get_requests()
    return requests
