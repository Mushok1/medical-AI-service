# Backend (Step 1.3 — persistence + async processing stub)

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

## What Step 1.3 adds

- Upload files are persisted to local storage path (`MEDICAL_AI_STORAGE_DIR`).
- `documents` now stores `input_uri`.
- A background processing stub simulates async pipeline transitions:
  - `queued -> processing_ocr -> processing_extraction -> needs_review`

## Data layer

- SQLAlchemy ORM model: `app/models/document.py`
- DB session/config: `app/core/db.py`, `app/core/config.py`
- SQL migrations:
  - `migrations/0001_create_documents.sql`
  - `migrations/0002_add_input_uri_to_documents.sql`

> Note: on startup the service calls `Base.metadata.create_all(...)` for local bootstrap.
> For production PostgreSQL, apply SQL migrations from `backend/migrations` via your migration pipeline.
