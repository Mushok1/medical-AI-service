from dataclasses import dataclass, field
from datetime import datetime, UTC
from threading import Lock
from uuid import UUID, uuid4

from app.models.status import DocumentStatus


@dataclass
class DocumentRecord:
    job_id: UUID
    filename: str
    content_type: str
    status: DocumentStatus = DocumentStatus.QUEUED
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    progress: int = 0
    error: str | None = None


class InMemoryDocumentStore:
    def __init__(self) -> None:
        self._lock = Lock()
        self._records: dict[UUID, DocumentRecord] = {}

    def create(self, filename: str, content_type: str) -> DocumentRecord:
        record = DocumentRecord(
            job_id=uuid4(),
            filename=filename,
            content_type=content_type,
        )
        with self._lock:
            self._records[record.job_id] = record
        return record

    def get(self, job_id: UUID) -> DocumentRecord | None:
        with self._lock:
            return self._records.get(job_id)


store = InMemoryDocumentStore()
