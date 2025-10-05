from datetime import datetime

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..db import Base


class User(Base):
	__tablename__ = "users"

	id: Mapped[int] = mapped_column(primary_key=True, index=True)
	email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
	hashed_password: Mapped[str]
	created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

	events: Mapped[list["Event"]] = relationship(back_populates="owner", cascade="all, delete-orphan")
	media: Mapped[list["Media"]] = relationship(back_populates="owner", cascade="all, delete-orphan")
