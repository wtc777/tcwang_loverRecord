from datetime import datetime

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..db import Base


class Event(Base):
	__tablename__ = "events"

	id: Mapped[int] = mapped_column(primary_key=True, index=True)
	title: Mapped[str] = mapped_column(String(255))
	description: Mapped[str | None] = mapped_column(Text(), default=None)
	event_date: Mapped[datetime]
	created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
	owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

	owner: Mapped["User"] = relationship(back_populates="events")
	media_items: Mapped[list["Media"]] = relationship(back_populates="event", cascade="all, delete-orphan")
