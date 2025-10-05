from datetime import datetime

from pydantic import BaseModel


class MediaBase(BaseModel):
	file_name: str
	file_path: str
	thumb_path: str | None = None
	event_id: int | None = None


class MediaCreate(BaseModel):
	event_id: int | None = None


class MediaOut(MediaBase):
	id: int
	uploaded_at: datetime

	model_config = {
		"from_attributes": True
	}
