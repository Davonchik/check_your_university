from fastapi import APIRouter
from infrastructure.database.database import async_session_maker
from infrastructure.schemas.request import RequestCreate, RequestOut, RequestUpdate
from infrastructure.crud.request import create_request, get_requests, update_request, get_request

router = APIRouter(prefix="/request", tags=["requests"])

def get_db():
    db = async_session_maker()
    try:
        yield db
    finally:
        db.close()

@router.post('/', response_model=RequestOut)
def create_new_request(request_in: RequestCreate, db: get_db):
    return create_request(db, request_in)

@router.get('/', response_model=list[RequestOut])
def read_requests(db: get_db):
    return get_requests(db)

