from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
	APP_NAME: str = "Couple Journal API"
	SECRET_KEY: str = "please_change_me"
	ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
	FRONTEND_ORIGIN: str = "http://localhost:5173"

	DB_PATH: str = str(Path(__file__).resolve().parent.parent.parent / "couple.db")
	SQLALCHEMY_DATABASE_URI: str | None = None
	UPLOAD_DIR: str = str(Path(__file__).resolve().parent.parent.parent / "uploads")

	class Config:
		env_file = ".env"

	def db_uri(self) -> str:
		if self.SQLALCHEMY_DATABASE_URI:
			return self.SQLALCHEMY_DATABASE_URI
		return f"sqlite:///{self.DB_PATH}"


def ensure_upload_dirs(path: str) -> None:
	dir_path = Path(path)
	dir_path.mkdir(parents=True, exist_ok=True)
	upload_assets = dir_path / "assets"
	upload_assets.mkdir(parents=True, exist_ok=True)


settings = Settings()
ensure_upload_dirs(settings.UPLOAD_DIR)
