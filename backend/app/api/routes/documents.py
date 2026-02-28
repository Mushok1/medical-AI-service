from uuid import UUID

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.repositories import DocumentRepository
from app.schemas.documents import DocumentStatusResponse, UploadDocumentResponse

router = APIRouter(prefix="/v1/documents", tags=["documents"])


@router.post("/upload", response_model=UploadDocumentResponse)
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
) -> UploadDocumentResponse:
    if not file.filename:
        raise HTTPException(status_code=400, detail="Filename is required")

    content_type = file.content_type or "application/octet-stream"
    record = DocumentRepository(db).create(filename=file.filename, content_type=content_type)

    return UploadDocumentResponse(
        job_id=UUID(record.id),
        filename=record.filename,
        content_type=record.content_type,
        status=record.status,
        created_at=record.created_at,
    )


@router.get("/{job_id}/status", response_model=DocumentStatusResponse)
def get_document_status(job_id: UUID, db: Session = Depends(get_db)) -> DocumentStatusResponse:
    record = DocumentRepository(db).get(job_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Job not found")

    return DocumentStatusResponse(
        job_id=UUID(record.id),
        status=record.status,
        created_at=record.created_at,
        updated_at=record.updated_at,
        progress=record.progress,
        error=record.error,
    )
