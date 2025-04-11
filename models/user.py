from sqlalchemy.orm import Mapped, mapped_column
from models.base import Base
from sqlalchemy import String, Integer
from sqlalchemy.orm import relationship
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String)
    created_at: Mapped[int] = mapped_column(
        Integer, default=lambda: int(datetime.now().timestamp())
    )
    updated_at: Mapped[int] = mapped_column(
        Integer, default=lambda: int(datetime.now().timestamp())
    )

    leads: Mapped[list] = relationship("Lead", back_populates="assigned_salesperson")
    