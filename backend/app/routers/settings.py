from fastapi import APIRouter

from ..config import settings


router = APIRouter(prefix="/api/settings", tags=["settings"])


@router.get("/public")
async def read_public_settings() -> dict[str, str]:
	return {
		"app_name": settings.APP_NAME,
		"frontend_origin": settings.FRONTEND_ORIGIN,
	
}
