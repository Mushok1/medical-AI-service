CREATE TYPE document_status AS ENUM (
    'queued',
    'processing_ocr',
    'processing_extraction',
    'needs_review',
    'approved',
    'generating_protocol',
    'done',
    'failed'
);

CREATE TABLE documents (
    id UUID PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    content_type VARCHAR(255) NOT NULL,
    status document_status NOT NULL DEFAULT 'queued',
    progress INTEGER NOT NULL DEFAULT 0,
    error VARCHAR(500),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_documents_status_created_at ON documents(status, created_at);
