from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from fastapi import HTTPException
from passlib.context import CryptContext

from ..config import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
	return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
	return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict[str, Any], expires_delta: int | None = None) -> str:
	to_encode = data.copy()
	expire = datetime.now(timezone.utc) + timedelta(minutes=expires_delta or settings.ACCESS_TOKEN_EXPIRE_MINUTES)
	to_encode.update({"exp": expire})
	return jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")


def decode_access_token(token: str) -> dict[str, Any] | None:
	try:
		return jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
	except jwt.PyJWTError as exc:
		raise HTTPException(status_code=401, detail="Invalid token") from exc
