# Backend (Step 1.2 — DB integration)

## Run locally

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Optional: set PostgreSQL URL (defaults to local SQLite file)
export MEDICAL_AI_DATABASE_URL='postgresql+psycopg2://user:pass@localhost:5432/medical_ai'

uvicorn app.main:app --reload
```

## Endpoints

- `GET /health`
- `POST /v1/documents/upload`
- `GET /v1/documents/{job_id}/status`

## Data layer

- SQLAlchemy ORM model: `app/models/document.py`
- DB session/config: `app/core/db.py`, `app/core/config.py`
- SQL migration starter: `migrations/0001_create_documents.sql`

> Note: on startup the service calls `Base.metadata.create_all(...)` for local bootstrap.
> For production PostgreSQL, apply SQL migrations from `backend/migrations` via your migration pipeline.
