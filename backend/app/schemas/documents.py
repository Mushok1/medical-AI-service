from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from app.models.status import DocumentStatus


class UploadDocumentResponse(BaseModel):
    job_id: UUID
    filename: str
    content_type: str
    input_uri: str
    status: DocumentStatus = DocumentStatus.QUEUED
    created_at: datetime


class DocumentStatusResponse(BaseModel):
    job_id: UUID
    status: DocumentStatus
    created_at: datetime
    updated_at: datetime
    progress: int = Field(default=0, ge=0, le=100)
    error: str | None = None


class ExtractedItemResponse(BaseModel):
    id: int
    analyte_name: str
    value: str
    unit: str
    reference_range: str | None
    confidence: float
    source_text: str | None
    review_status: str


class ExtractedItemPatch(BaseModel):
    id: int
    value: str | None = None
    unit: str | None = None
    review_status: str | None = None


class ApproveResponse(BaseModel):
    job_id: UUID
    status: DocumentStatus


class GenerateProtocolResponse(BaseModel):
    job_id: UUID
    status: DocumentStatus
    output_uri: str
