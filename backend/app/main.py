from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import analytics, tickets
from app.core.config import get_settings
from app.core.logging import configure_logging

configure_logging()
settings = get_settings()
app = FastAPI(title=settings.app_name, version="0.1.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(tickets.router, prefix="/api/v1")
app.include_router(analytics.router, prefix="/api/v1")

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": settings.app_name}
