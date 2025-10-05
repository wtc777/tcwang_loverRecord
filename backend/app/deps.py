from collections.abc import Generator
from typing import TYPE_CHECKING

from fastapi import Depends
from sqlalchemy.orm import Session

from .db import SessionLocal
from .utils.security import hash_password

if TYPE_CHECKING:
        from .models.user import User


def get_db() -> Generator[Session, None, None]:
	db = SessionLocal()
	try:
		yield db
        finally:
                db.close()


DEFAULT_USER_EMAIL = "couple@lover.record"


def _ensure_default_user(db: Session) -> "User":
        from .models.user import User

        user = db.query(User).order_by(User.id).first()
        if user:
                return user
        user = User(email=DEFAULT_USER_EMAIL, hashed_password=hash_password("love-story"))
        db.add(user)
        db.commit()
        db.refresh(user)
        return user


async def get_current_user(db: Session = Depends(get_db)) -> "User":
        return _ensure_default_user(db)
