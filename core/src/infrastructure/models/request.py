import uuid
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import VARCHAR, INTEGER, UUID, DATE, TEXT
from src.infrastructure.database.database import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Request(Base):
    __tablename__="request"
    id: Mapped[int]=mapped_column(INTEGER, primary_key=True)
    user_id: Mapped[int]=mapped_column(ForeignKey("user.id"))
    building_name: Mapped[str]=mapped_column(VARCHAR, nullable=True)
    category: Mapped[str]=mapped_column(VARCHAR, nullable=True)
    room: Mapped[str]=mapped_column(VARCHAR, nullable=True)
    text: Mapped[str]=mapped_column(TEXT, nullable=True)
    photo_url: Mapped[str]=mapped_column(VARCHAR, nullable=True)
    status: Mapped[str]=mapped_column(VARCHAR, nullable=True)
    created_at: Mapped[datetime]=mapped_column(DATE, default=datetime.now())
    updated_at: Mapped[datetime]=mapped_column(DATE, default=datetime.now())

