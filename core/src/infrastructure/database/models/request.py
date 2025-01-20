import uuid
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import VARCHAR, INTEGER, UUID, DATE, TEXT
from src.infrastructure.database.database import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from src.infrastructure.database.models.user import User

class Request(Base):
    __tablename__="request"
    id: Mapped[int]=mapped_column(INTEGER, primary_key=True)
    user_id: Mapped[int]=mapped_column(ForeignKey("user.id"))
    building_id: Mapped[int]=mapped_column(ForeignKey("building.id"))
    category: Mapped[str]=mapped_column(VARCHAR, nullable=True)
    room: Mapped[str]=mapped_column(VARCHAR, nullable=True)
    text: Mapped[str]=mapped_column(TEXT, nullable=True)
    photo_url: Mapped[str]=mapped_column(VARCHAR, nullable=True)
    status: Mapped[str]=mapped_column(VARCHAR, nullable=True, default="pending")
    created_at: Mapped[datetime]=mapped_column(DATE, default=datetime.now())
    updated_at: Mapped[datetime]=mapped_column(DATE, default=datetime.now())
    user: Mapped["User"] = relationship("User", back_populates="request", lazy = "selectin")
    building: Mapped["Building"] = relationship("Building", back_populates="request", lazy = "selectin")
    