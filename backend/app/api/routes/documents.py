from uuid import UUID

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.schemas.documents import DocumentStatusResponse, UploadDocumentResponse
from app.services.document_store import store

router = APIRouter(prefix="/v1/documents", tags=["documents"])


@router.post("/upload", response_model=UploadDocumentResponse)
async def upload_document(file: UploadFile = File(...)) -> UploadDocumentResponse:
    if not file.filename:
        raise HTTPException(status_code=400, detail="Filename is required")

    content_type = file.content_type or "application/octet-stream"
    record = store.create(filename=file.filename, content_type=content_type)

    return UploadDocumentResponse(
        job_id=record.job_id,
        filename=record.filename,
        content_type=record.content_type,
        status=record.status,
        created_at=record.created_at,
    )


@router.get("/{job_id}/status", response_model=DocumentStatusResponse)
def get_document_status(job_id: UUID) -> DocumentStatusResponse:
    record = store.get(job_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Job not found")

    return DocumentStatusResponse(
        job_id=record.job_id,
        status=record.status,
        created_at=record.created_at,
        updated_at=record.updated_at,
        progress=record.progress,
        error=record.error,
    )
