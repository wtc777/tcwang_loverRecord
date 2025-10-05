from datetime import datetime

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..db import Base


class Media(Base):
	__tablename__ = "media"

	id: Mapped[int] = mapped_column(primary_key=True, index=True)
	file_name: Mapped[str]
	file_path: Mapped[str]
	thumb_path: Mapped[str | None]
	uploaded_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
	owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
	event_id: Mapped[int | None] = mapped_column(ForeignKey("events.id", ondelete="SET NULL"), default=None)

	owner: Mapped["User"] = relationship(back_populates="media")
	event: Mapped["Event" | None] = relationship(back_populates="media_items")
