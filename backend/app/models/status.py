from enum import Enum


class DocumentStatus(str, Enum):
    QUEUED = "queued"
    PROCESSING_OCR = "processing_ocr"
    PROCESSING_EXTRACTION = "processing_extraction"
    NEEDS_REVIEW = "needs_review"
    APPROVED = "approved"
    GENERATING_PROTOCOL = "generating_protocol"
    DONE = "done"
    FAILED = "failed"
