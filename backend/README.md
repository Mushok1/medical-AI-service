# Backend (Step 1.4 — review + protocol flow API)

## Run locally

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Optional: set PostgreSQL URL (defaults to local SQLite file)
export MEDICAL_AI_DATABASE_URL='postgresql+psycopg2://user:pass@localhost:5432/medical_ai'

# Optional: configure local file storage directory for uploads
export MEDICAL_AI_STORAGE_DIR='./storage'

uvicorn app.main:app --reload
```

## Endpoints

- `GET /health`
- `POST /v1/documents/upload`
- `GET /v1/documents/{job_id}/status`
- `GET /v1/documents/{job_id}/extracted-items`
- `PATCH /v1/documents/{job_id}/extracted-items`
- `POST /v1/documents/{job_id}/approve`
- `POST /v1/documents/{job_id}/generate-protocol`
- `GET /v1/documents/{job_id}/download`

## What Step 1.4 adds

- Stores extracted lab items in DB (`extracted_items`) after async processing stub.
- Supports manual edits to extracted items via PATCH endpoint.
- Adds review gate (`approve`) before protocol generation.
- Adds protocol generation stub and download endpoint (`output_uri`).

## Data layer

- SQLAlchemy ORM models:
  - `app/models/document.py`
  - `app/models/extracted_item.py`
- DB session/config:
  - `app/core/db.py`
  - `app/core/config.py`
- SQL migrations:
  - `migrations/0001_create_documents.sql`
  - `migrations/0002_add_input_uri_to_documents.sql`
  - `migrations/0003_add_extracted_items_and_output_uri.sql`

> Note: on startup the service calls `Base.metadata.create_all(...)` for local bootstrap.
> For production PostgreSQL, apply SQL migrations from `backend/migrations` via your migration pipeline.
