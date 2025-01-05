from src.infrastructure.schemas.request import RequestCreate, RequestOut, RequestUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.models.request import Request

def create_request(session: AsyncSession, request_in: RequestCreate) -> RequestOut:
    querry = Request(
        building_name=request_in.building_name,
        category=request_in.category,
        room=request_in.room,
        text=request_in.text,
        photo_url=request_in.photo_url,
    )
    session.add(querry)
    session.commit()
    session.refresh(querry)
    return querry

def get_request(session: AsyncSession, request_id: int) -> RequestOut:
    return session.querry(Request).filter(Request.id == request_id).first()

def get_requests(session: AsyncSession) -> list[RequestOut]:
    return session.querry(Request).all()

def update_request(session: AsyncSession, request_id: int, new_status: RequestUpdate) -> RequestOut:
    querry = session.querry(Request).filter(Request.id == request_id).first()
    querry.status = new_status.status
    session.commit()
    session.refresh(querry)
    return querry
