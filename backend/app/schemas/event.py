from datetime import datetime

from pydantic import BaseModel, Field

from .media import MediaOut


class EventBase(BaseModel):
	title: str
	description: str | None = None
	event_date: datetime


class EventCreate(EventBase):
	media_ids: list[int] | None = None


class EventUpdate(BaseModel):
	title: str | None = None
	description: str | None = None
	event_date: datetime | None = None
	media_ids: list[int] | None = None


class EventOut(EventBase):
	id: int
	created_at: datetime
	media_items: list[MediaOut] = Field(default_factory=list)

	model_config = {
		"from_attributes": True
	}
