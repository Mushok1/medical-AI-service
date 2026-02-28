from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

from app.core.config import settings


def save_uploaded_file(file: UploadFile) -> str:
    settings.storage_dir.mkdir(parents=True, exist_ok=True)

    suffix = Path(file.filename or "upload.bin").suffix
    stored_name = f"{uuid4()}{suffix}"
    destination = settings.storage_dir / stored_name

    with destination.open("wb") as handle:
        while chunk := file.file.read(1024 * 1024):
            handle.write(chunk)

    return str(destination)
