from sqlalchemy.ext.asyncio import AsyncSession

class Dao:
    __slots__=['session']
    def __init__(self, session: AsyncSession):
        self.session = session

    