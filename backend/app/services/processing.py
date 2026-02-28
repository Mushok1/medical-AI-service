from time import sleep
from uuid import UUID

from app.core.db import SessionLocal
from app.models.status import DocumentStatus
from app.repositories import DocumentRepository, ExtractedItemRepository


MOCK_EXTRACTED_ITEMS = [
    {
        "analyte_name": "Glucose",
        "value": "5.8",
        "unit": "mmol/L",
        "reference_range": "3.9-6.1",
        "confidence": 0.94,
        "source_text": "Glucose 5.8 mmol/L",
        "review_status": "pending",
    },
    {
        "analyte_name": "Hemoglobin",
        "value": "138",
        "unit": "g/L",
        "reference_range": "120-160",
        "confidence": 0.91,
        "source_text": "Hemoglobin 138 g/L",
        "review_status": "pending",
    },
]


def run_processing_pipeline(job_id: UUID) -> None:
    with SessionLocal() as db:
        document_repo = DocumentRepository(db)
        item_repo = ExtractedItemRepository(db)

        document = document_repo.update_status(job_id, DocumentStatus.PROCESSING_OCR, 25)
        if document is None:
            return
        sleep(0.2)

        document = document_repo.update_status(job_id, DocumentStatus.PROCESSING_EXTRACTION, 65)
        if document is None:
            return
        sleep(0.2)

        item_repo.create_many(document_id=document.id, items=MOCK_EXTRACTED_ITEMS)
        document_repo.update_status(job_id, DocumentStatus.NEEDS_REVIEW, 100)
