from fastapi import FastAPI
from app.api.incidents import router as incidents_router
from app.api.diagnose import router as diagnose_router
from app.models.db import init_db

app = FastAPI(title="Incident Response Agent with Hindsight")

@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(incidents_router, prefix="/incidents", tags=["incidents"])
app.include_router(diagnose_router, prefix="/incidents", tags=["diagnose"])

@app.get("/")
def health():
    return {"status": "ok", "service": "incident-response-agent"}
