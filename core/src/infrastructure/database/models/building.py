from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import VARCHAR, INTEGER, UUID, DATE
from src.infrastructure.database.database import Base
from typing import List

class Building(Base):
    __tablename__="building"
    id: Mapped[int]=mapped_column(INTEGER, primary_key=True)
    name: Mapped[str]=mapped_column(VARCHAR, nullable=True, unique=True)
    admin: Mapped[List['Admin']]=relationship('Admin', back_populates='building')
    request: Mapped[List['Request']]=relationship('Request', back_populates='building')
    