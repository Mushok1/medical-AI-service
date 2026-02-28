from fastapi import FastAPI

from app.api.routes.documents import router as documents_router
from app.api.routes.health import router as health_router
from app.core.db import Base, engine
from app.models.document import Document  # noqa: F401

app = FastAPI(title="Medical AI Service", version="0.2.0")


@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)


app.include_router(health_router)
app.include_router(documents_router)
