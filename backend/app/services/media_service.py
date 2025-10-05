from pathlib import Path
from typing import Tuple
from uuid import uuid4

from fastapi import HTTPException, UploadFile
from PIL import Image


ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png", "image/gif", "video/mp4", "audio/mpeg"}


def save_upload_file(upload_file: UploadFile, upload_dir: Path) -> Tuple[str, str, str | None]:
	if upload_file.content_type not in ALLOWED_CONTENT_TYPES:
		raise HTTPException(status_code=400, detail="Unsupported file type")
	upload_dir.mkdir(parents=True, exist_ok=True)
	original_suffix = Path(upload_file.filename or "").suffix
	safe_name = f"{uuid4().hex}{original_suffix}"
	target_path = upload_dir / safe_name
	upload_file.file.seek(0)
	with target_path.open("wb") as buffer:
		buffer.write(upload_file.file.read())
	thumb_path: str | None = None
	if upload_file.content_type.startswith("image/"):
		thumb_fs_path = _generate_thumbnail(target_path)
		if thumb_fs_path:
			thumb_path = f"/static/{Path(thumb_fs_path).name}"
	return safe_name, f"/static/{safe_name}", thumb_path


def _generate_thumbnail(image_path: Path) -> Path | None:
	thumb_path = image_path.with_name(f"thumb_{image_path.name}")
	try:
		with Image.open(image_path) as img:
			img.thumbnail((512, 512))
			img.save(thumb_path)
		return thumb_path
	except Exception:
		return None
