from time import sleep
from uuid import UUID

from app.core.db import SessionLocal
from app.models.status import DocumentStatus
from app.repositories import DocumentRepository


def run_processing_pipeline(job_id: UUID) -> None:
    with SessionLocal() as db:
        repo = DocumentRepository(db)

        repo.update_status(job_id, DocumentStatus.PROCESSING_OCR, 25)
        sleep(0.2)

        repo.update_status(job_id, DocumentStatus.PROCESSING_EXTRACTION, 65)
        sleep(0.2)

        repo.update_status(job_id, DocumentStatus.NEEDS_REVIEW, 100)
