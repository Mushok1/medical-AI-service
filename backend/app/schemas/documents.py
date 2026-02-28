from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from app.models.status import DocumentStatus


class UploadDocumentResponse(BaseModel):
    job_id: UUID
    filename: str
    content_type: str
    status: DocumentStatus = DocumentStatus.QUEUED
    created_at: datetime


class DocumentStatusResponse(BaseModel):
    job_id: UUID
    status: DocumentStatus
    created_at: datetime
    updated_at: datetime
    progress: int = Field(default=0, ge=0, le=100)
    error: str | None = None
