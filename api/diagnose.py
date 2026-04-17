from datetime import datetime
from fastapi import APIRouter, HTTPException
from app.models.db import SessionLocal
from app.models.incident import Incident
from app.models.schemas import DiagnoseResponse, ResolveRequest, IncidentOut
from app.services.incident_engine import diagnose_incident
from app.services.hindsight_client import retain_memory

router = APIRouter()

@router.post("/{incident_id}/diagnose", response_model=DiagnoseResponse)
def diagnose(incident_id: int):
    db = SessionLocal()
    try:
        incident = db.query(Incident).filter(Incident.id == incident_id).first()
        if not incident:
            raise HTTPException(status_code=404, detail="Incident not found")

        diagnosis, memories = diagnose_incident(incident)
        incident.latest_diagnosis = diagnosis
        db.commit()

        return DiagnoseResponse(
            incident_id=incident.id,
            diagnosis=diagnosis,
            recalled_memories=memories
        )
    finally:
        db.close()

@router.post("/{incident_id}/resolve", response_model=IncidentOut)
def resolve(incident_id: int, payload: ResolveRequest):
    db = SessionLocal()
    try:
        incident = db.query(Incident).filter(Incident.id == incident_id).first()
        if not incident:
            raise HTTPException(status_code=404, detail="Incident not found")

        incident.status = "resolved"
        incident.root_cause = payload.root_cause
        incident.resolution = payload.resolution
        incident.resolved_at = datetime.utcnow()
        db.commit()
        db.refresh(incident)

        memory_text = f"""
Resolved Incident:
Title: {incident.title}
Service: {incident.service}
Severity: {incident.severity}
Symptoms: {incident.symptoms}
Logs: {incident.logs or "N/A"}
Root Cause: {incident.root_cause}
Resolution: {incident.resolution}
"""
        retain_memory(memory_text, metadata={
            "incident_id": incident.id,
            "service": incident.service,
            "severity": incident.severity,
            "status": incident.status
        })

        return incident
    finally:
        db.close()
