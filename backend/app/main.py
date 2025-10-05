from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .config import settings
from .db import init_db
from .routers import events, media, settings as settings_router


init_db()


app = FastAPI(title=settings.APP_NAME)


app.add_middleware(
	CORSMiddleware,
	allow_origins=[settings.FRONTEND_ORIGIN],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)


app.mount("/static", StaticFiles(directory=settings.UPLOAD_DIR), name="static")


@app.get("/health")
async def health_check() -> dict[str, str]:
	return {"status": "ok"}


app.include_router(events.router)
app.include_router(media.router)
app.include_router(settings_router.router)
