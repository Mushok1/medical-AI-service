# Backend (Step 1.1 MVP skeleton)

## Run locally

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Endpoints

- `GET /health`
- `POST /v1/documents/upload`
- `GET /v1/documents/{job_id}/status`
