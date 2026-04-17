from fastapi import APIRouter, HTTPException
from app.models.db import SessionLocal
from app.models.incident import Incident
from app.models.schemas import IncidentCreate, IncidentOut

router = APIRouter()

@router.post("", response_model=IncidentOut)
def create_incident(payload: IncidentCreate):
    db = SessionLocal()
    try:
        obj = Incident(
            title=payload.title,
            service=payload.service,
            severity=payload.severity,
            symptoms=payload.symptoms,
            logs=payload.logs,
        )
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj
    finally:
        db.close()

@router.get("/{incident_id}", response_model=IncidentOut)
def get_incident(incident_id: int):
    db = SessionLocal()
    try:
        obj = db.query(Incident).filter(Incident.id == incident_id).first()
        if not obj:
            raise HTTPException(status_code=404, detail="Incident not found")
        return obj
    finally:
        db.close()
