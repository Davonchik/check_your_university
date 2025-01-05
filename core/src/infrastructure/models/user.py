import uuid
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import VARCHAR, INTEGER, UUID, DATE
from src.infrastructure.database.database import Base

class User(Base):
    __tablename__="user"
    id: Mapped[int]=mapped_column(INTEGER, primary_key=True)
    tg_id: Mapped[str]=mapped_column(VARCHAR, nullable=True)
    created_at: Mapped[datetime]=mapped_column(DATE, default=datetime.now())

