from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import deps
from ..models.user import User
from ..schemas.auth import Token, UserCreate, UserLogin, UserOut
from ..utils.security import create_access_token, hash_password, verify_password


router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register(payload: UserCreate, db: Session = Depends(deps.get_db)) -> User:
	existing = db.query(User).filter(User.email == payload.email).first()
	if existing:
		raise HTTPException(status_code=400, detail="Email already registered")
	user = User(email=payload.email, hashed_password=hash_password(payload.password))
	db.add(user)
	db.commit()
	db.refresh(user)
	return user


@router.post("/login", response_model=Token)
async def login(payload: UserLogin, db: Session = Depends(deps.get_db)) -> Token:
	user = db.query(User).filter(User.email == payload.email).first()
	if not user or not verify_password(payload.password, user.hashed_password):
		raise HTTPException(status_code=400, detail="Incorrect email or password")
	token = create_access_token({"sub": str(user.id)})
	return Token(access_token=token)


@router.get("/me", response_model=UserOut)
async def read_current_user(current_user: User = Depends(deps.get_current_user)) -> User:
	return current_user
