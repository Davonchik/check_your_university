import uuid
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import VARCHAR, INTEGER, DATE
from src.infrastructure.database.database import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from src.infrastructure.database.models.user import User

class S3(Base):
    __tablename__="s3"
    id: Mapped[int]=mapped_column(INTEGER, primary_key=True)
    user_id: Mapped[int]=mapped_column(ForeignKey("user.id"))
    file_name: Mapped[str]=mapped_column(VARCHAR, nullable=True)
    file_url: Mapped[str]=mapped_column(VARCHAR, nullable=True)
    created_at: Mapped[datetime]=mapped_column(DATE, default=datetime.now())
    updated_at: Mapped[datetime]=mapped_column(DATE, default=datetime.now())
    user: Mapped["User"] = relationship("User", back_populates="s3", lazy = "selectin")
    