from datetime import datetime
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.document import Document
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
