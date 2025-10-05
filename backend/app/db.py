from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from .config import settings



def get_database_url() -> str:
	return settings.db_uri()



def get_engine():
	database_url = get_database_url()
	connect_args = {"check_same_thread": False} if database_url.startswith("sqlite") else {}
	return create_engine(database_url, connect_args=connect_args)



engine = get_engine()
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)



class Base(DeclarativeBase):
	pass



def init_db() -> None:
	from . import models  # noqa: F401
	Base.metadata.create_all(bind=engine)
