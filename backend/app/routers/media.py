from pathlib import Path

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from .. import deps
from ..config import settings
from ..models.media import Media
from ..schemas.media import MediaOut
from ..services.media_service import save_upload_file


router = APIRouter(prefix="/api/media", tags=["media"])


@router.get("/", response_model=list[MediaOut])
async def list_media(db: Session = Depends(deps.get_db), current_user=Depends(deps.get_current_user)) -> list[Media]:
	media_items = db.query(Media).filter(Media.owner_id == current_user.id).order_by(Media.uploaded_at.desc()).all()
	return media_items


@router.post("/upload", response_model=MediaOut, status_code=status.HTTP_201_CREATED)
async def upload_media(
	file: UploadFile = File(...),
	event_id: int | None = Form(default=None),
	db: Session = Depends(deps.get_db),
	current_user=Depends(deps.get_current_user),
) -> Media:
	if not file.filename:
		raise HTTPException(status_code=400, detail="Invalid file")
	file_name, stored_path, thumb_path = save_upload_file(file, Path(settings.UPLOAD_DIR))
	media = Media(
		file_name=file_name,
		file_path=stored_path,
		thumb_path=thumb_path,
		owner_id=current_user.id,
		event_id=event_id,
	)
	db.add(media)
	db.commit()
	db.refresh(media)
	return media
