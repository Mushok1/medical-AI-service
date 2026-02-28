from datetime import datetime
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.document import Document


class DocumentRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, filename: str, content_type: str) -> Document:
        now = datetime.utcnow()
        record = Document(filename=filename, content_type=content_type, created_at=now, updated_at=now)
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record

    def get(self, job_id: UUID) -> Document | None:
        return self.db.query(Document).filter(Document.id == str(job_id)).first()
