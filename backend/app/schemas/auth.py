from datetime import datetime

from pydantic import BaseModel, EmailStr


class Token(BaseModel):
	access_token: str
	token_type: str = "bearer"


class UserBase(BaseModel):
	email: EmailStr


class UserCreate(UserBase):
	password: str


class UserLogin(UserBase):
	password: str


class UserOut(UserBase):
	id: int
	created_at: datetime

	model_config = {
		"from_attributes": True
	}
