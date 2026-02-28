from datetime import datetime
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.document import Document
from app.models.extracted_item import ExtractedItem
from app.models.status import DocumentStatus


class DocumentRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, filename: str, content_type: str, input_uri: str) -> Document:
        now = datetime.utcnow()
        record = Document(
            filename=filename,
            content_type=content_type,
            input_uri=input_uri,
            created_at=now,
            updated_at=now,
            status=DocumentStatus.QUEUED,
            progress=0,
        )
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record

    def get(self, job_id: UUID) -> Document | None:
        return self.db.query(Document).filter(Document.id == str(job_id)).first()

    def update_status(
        self,
        job_id: UUID,
        status: DocumentStatus,
        progress: int,
        error: str | None = None,
    ) -> Document | None:
        record = self.get(job_id)
        if record is None:
            return None

        record.status = status
        record.progress = progress
        record.error = error
        record.updated_at = datetime.utcnow()
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record

    def set_output_uri(self, job_id: UUID, output_uri: str) -> Document | None:
        record = self.get(job_id)
        if record is None:
            return None
        record.output_uri = output_uri
        record.updated_at = datetime.utcnow()
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record


class ExtractedItemRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create_many(self, document_id: str, items: list[dict]) -> None:
        now = datetime.utcnow()
        records = [
            ExtractedItem(
                document_id=document_id,
                analyte_name=item["analyte_name"],
                value=item["value"],
                unit=item["unit"],
                reference_range=item.get("reference_range"),
                confidence=item.get("confidence", 0.0),
                source_text=item.get("source_text"),
                review_status=item.get("review_status", "pending"),
                created_at=now,
                updated_at=now,
            )
            for item in items
        ]
        self.db.add_all(records)
        self.db.commit()

    def list_by_document(self, document_id: str) -> list[ExtractedItem]:
        return self.db.query(ExtractedItem).filter(ExtractedItem.document_id == document_id).order_by(ExtractedItem.id).all()

    def patch_items(self, document_id: str, updates: list[dict]) -> list[ExtractedItem]:
        update_map = {item["id"]: item for item in updates}
        records = self.list_by_document(document_id)
        now = datetime.utcnow()

        for record in records:
            patch = update_map.get(record.id)
            if not patch:
                continue
            if patch.get("value") is not None:
                record.value = patch["value"]
            if patch.get("unit") is not None:
                record.unit = patch["unit"]
            if patch.get("review_status") is not None:
                record.review_status = patch["review_status"]
            record.updated_at = now
            self.db.add(record)

        self.db.commit()
        return self.list_by_document(document_id)
