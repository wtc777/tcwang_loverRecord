import logging
from pathlib import Path

from ..config import settings


log_dir = Path(settings.UPLOAD_DIR).parent / "logs"
log_dir.mkdir(parents=True, exist_ok=True)


logger = logging.getLogger("couple_journal")
logger.setLevel(logging.INFO)

handler = logging.FileHandler(log_dir / "app.log")
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)

if not logger.handlers:
	logger.addHandler(handler)
