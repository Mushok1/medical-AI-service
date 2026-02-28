from pathlib import Path
from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.models.status import DocumentStatus
from app.repositories import DocumentRepository, ExtractedItemRepository
from app.schemas.documents import (
    ApproveResponse,
    DocumentStatusResponse,
    ExtractedItemPatch,
    ExtractedItemResponse,
    GenerateProtocolResponse,
    UploadDocumentResponse,
)
from app.services.processing import run_processing_pipeline
from app.services.storage import save_uploaded_file

router = APIRouter(prefix="/v1/documents", tags=["documents"])


@router.post("/upload", response_model=UploadDocumentResponse)
async def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
) -> UploadDocumentResponse:
    if not file.filename:
        raise HTTPException(status_code=400, detail="Filename is required")

    content_type = file.content_type or "application/octet-stream"
    input_uri = save_uploaded_file(file)
    record = DocumentRepository(db).create(
        filename=file.filename,
        content_type=content_type,
        input_uri=input_uri,
    )

    background_tasks.add_task(run_processing_pipeline, UUID(record.id))

    return UploadDocumentResponse(
        job_id=UUID(record.id),
        filename=record.filename,
        content_type=record.content_type,
        input_uri=record.input_uri,
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


@router.get("/{job_id}/extracted-items", response_model=list[ExtractedItemResponse])
def list_extracted_items(job_id: UUID, db: Session = Depends(get_db)) -> list[ExtractedItemResponse]:
    record = DocumentRepository(db).get(job_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Job not found")

    items = ExtractedItemRepository(db).list_by_document(record.id)
    return [ExtractedItemResponse.model_validate(item, from_attributes=True) for item in items]


@router.patch("/{job_id}/extracted-items", response_model=list[ExtractedItemResponse])
def patch_extracted_items(
    job_id: UUID,
    patches: list[ExtractedItemPatch],
    db: Session = Depends(get_db),
) -> list[ExtractedItemResponse]:
    record = DocumentRepository(db).get(job_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Job not found")

    updates = [patch.model_dump(exclude_none=True) for patch in patches]
    items = ExtractedItemRepository(db).patch_items(record.id, updates)
    return [ExtractedItemResponse.model_validate(item, from_attributes=True) for item in items]


@router.post("/{job_id}/approve", response_model=ApproveResponse)
def approve_document(job_id: UUID, db: Session = Depends(get_db)) -> ApproveResponse:
    repo = DocumentRepository(db)
    record = repo.get(job_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Job not found")

    if record.status not in (DocumentStatus.NEEDS_REVIEW, DocumentStatus.APPROVED):
        raise HTTPException(status_code=409, detail="Document is not ready for approval")

    record = repo.update_status(job_id, DocumentStatus.APPROVED, 100)
    if record is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return ApproveResponse(job_id=job_id, status=record.status)


@router.post("/{job_id}/generate-protocol", response_model=GenerateProtocolResponse)
def generate_protocol(job_id: UUID, db: Session = Depends(get_db)) -> GenerateProtocolResponse:
    repo = DocumentRepository(db)
    record = repo.get(job_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Job not found")

    if record.status != DocumentStatus.APPROVED:
        raise HTTPException(status_code=409, detail="Document must be approved before protocol generation")

    repo.update_status(job_id, DocumentStatus.GENERATING_PROTOCOL, 100)
    output_uri = str(Path(record.input_uri).with_suffix(".protocol.docx"))
    record = repo.set_output_uri(job_id, output_uri)
    record = repo.update_status(job_id, DocumentStatus.DONE, 100)
    if record is None:
        raise HTTPException(status_code=404, detail="Job not found")

    return GenerateProtocolResponse(job_id=job_id, status=record.status, output_uri=output_uri)


@router.get("/{job_id}/download")
def download_protocol(job_id: UUID, db: Session = Depends(get_db)) -> dict[str, str]:
    record = DocumentRepository(db).get(job_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Job not found")

    if record.status != DocumentStatus.DONE or not record.output_uri:
        raise HTTPException(status_code=409, detail="Protocol is not available yet")

    return {"job_id": str(job_id), "output_uri": record.output_uri}
