from src.application.domain.request import RequestCreate
from src.infrastructure.database.models.request import Request
from src.infrastructure.database.models.building import Building
from src.application.abstractions.dao.i_request_dao import IRequestDao
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound
from src.logger import logger
from sqlalchemy import func


class RequestDao(IRequestDao):
    async def create_request(self, request_in: RequestCreate) -> Request:
        logger.info("Create request try")
        try:
            request = Request(**request_in.dict())
            self.session.add(request)
            await self.session.commit()
            await self.session.refresh(request)
            return request
        except Exception as e:
            logger.error(f"Exception in create request: {e}")
            raise
    
    async def get_requests(self) -> list[Request]:
        logger.info("Get requests try")
        try:
            query = await self.session.execute(select(Request))
            return query.scalars().all()
        except Exception as e:
            logger.error(f"Exception in get requests: {e}")
            raise

    async def get_statistics(self) -> tuple[int, int]:
        logger.info('Get statistics')
        query_all = await self.session.execute(select(func.count()).select_from(Request))
        all_requests_cnt = query_all.scalar()

        query_done = await self.session.execute(
            select(func.count()).select_from(Request).where(Request.status == 'done'))
        done_requests_cnt = query_done.scalar()

        return all_requests_cnt, done_requests_cnt
    
    async def get_request_by_id(self, request_id: int) -> Request:
        logger.info("Get request by id try")
        try:
            query = select(Request).where(Request.id == request_id)
            result = await self.session.execute(query)
            return result.scalar_one_or_none()
        except Exception as e:
            logger.error(f"Exception in get request by id: {e}")
            raise


    async def update_request(self, request_id: int, request_in: RequestCreate) -> Request:
        logger.info("Update request try")
        try:
            query = select(Request).where(Request.id == request_id)
            result = await self.session.execute(query)
            existing_request = result.scalar_one_or_none()
            if not existing_request:
                return NoResultFound(f"Request with id {request_id} not found")
            
            for key, value in request_in.dict().items():  
                setattr(existing_request, key, value)
            
            self.session.add(existing_request)
            await self.session.commit()
            await self.session.refresh(existing_request)
            return existing_request
        except Exception as e:
            logger.error(f"Exception in update request: {e}")
            raise

    async def filter_by_building(self, building_name: str) -> list[Request]:
        logger.info(f"Filter requests by building_name: {building_name}")
        try:
            # Выполняем JOIN с таблицей Building и фильтруем по имени здания
            query = (
                select(Request)
                .join(Request.building)
                .where(Building.name == building_name)
            )
            result = await self.session.execute(query)
            return result.scalars().all()
        except Exception as e:
            logger.error(f"Exception in filter_by_building_name: {e}")
            raise
    