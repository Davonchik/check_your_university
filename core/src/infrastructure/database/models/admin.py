import uuid
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import VARCHAR, INTEGER, UUID, DATE
from src.infrastructure.database.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey

class Admin(Base):
    __tablename__="admin"
    id: Mapped[int]=mapped_column(INTEGER, primary_key=True)
    email: Mapped[str]=mapped_column(VARCHAR, nullable=True)
    password: Mapped[str]=mapped_column(VARCHAR, nullable=True)
    building_id: Mapped[int]=mapped_column(ForeignKey("building.id"))
    building = relationship("Building", back_populates="admin")
