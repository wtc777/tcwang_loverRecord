from collections.abc import Generator

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from .db import SessionLocal
from .utils.security import decode_access_token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def get_db() -> Generator[Session, None, None]:
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
	from .models.user import User

	payload = decode_access_token(token)
	if not payload:
		raise HTTPException(status_code=401, detail="Invalid credentials")
	user_id = int(payload["sub"])
	user = db.get(User, user_id)
	if not user:
		raise HTTPException(status_code=401, detail="User not found")
	return user
