from src.application.abstractions.dao.i_building_dao import IBuildingDao
from src.infrastructure.database.models.building import Building
from sqlalchemy.future import select
from src.logger import logger

class BuildingDao(IBuildingDao):
    async def get_by_id(self, id: int):
        logger.info("Get building by id")
        try:
            building = await self.session.execute(select(Building).where(Building.id == id))
            return building.scalars().one().name
        except Exception as e:
            logger.error(e)
            raise
    
    
    async def create_building(self, name: str):
        logger.info("Create building try")
        try:
            building = Building(name=name)
            self.session.add(building)
            await self.session.commit()
            await self.session.refresh(building)
            return building
        except Exception as e:
            logger.error(f"Exception in create building: {e}")
            raise
    
    
    async def delete_building(self, id: int):
        logger.info("Delete building try")
        try:
            building = await self.session.execute(select(Building).where(Building.id == id))
            get_b = building.scalars().one_or_none()
            print(get_b)
            await self.session.delete(get_b)
            await self.session.commit()
            return get_b
        except Exception as e:
            logger.error(f"Exception in delete building: {e}")
            raise

    async def get_id_by_name(self, name: str):
        logger.info("Get id by name")
        try:
            building = await self.session.execute(select(Building).where(Building.name == name))
            return building.scalars().one().id
        except Exception as e:
            logger.error(e)
            raise

    async def get_buildings(self):
        logger.info("Get buildings try")
        try:
            query = await self.session.execute(select(Building))
            return query.scalars().all()
        except Exception as e:
            logger.error(e)
            raise
