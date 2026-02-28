ALTER TABLE documents
ADD COLUMN output_uri VARCHAR(500);

CREATE TABLE extracted_items (
    id SERIAL PRIMARY KEY,
    document_id UUID NOT NULL REFERENCES documents(id),
    analyte_name VARCHAR(255) NOT NULL,
    value VARCHAR(255) NOT NULL,
    unit VARCHAR(64) NOT NULL,
    reference_range VARCHAR(128),
    confidence DOUBLE PRECISION NOT NULL DEFAULT 0,
    source_text TEXT,
    review_status VARCHAR(32) NOT NULL DEFAULT 'pending',
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_extracted_items_document_id ON extracted_items(document_id);
