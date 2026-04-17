from pydantic import BaseModel
from typing import Optional, List

class IncidentCreate(BaseModel):
    title: str
    service: str
    severity: str
    symptoms: str
    logs: Optional[str] = None

class IncidentOut(BaseModel):
    id: int
    title: str
    service: str
    severity: str
    symptoms: str
    logs: Optional[str]
    status: str
    root_cause: Optional[str]
    resolution: Optional[str]
    latest_diagnosis: Optional[str]

    class Config:
        from_attributes = True

class DiagnoseResponse(BaseModel):
    incident_id: int
    diagnosis: str
    recalled_memories: List[str]

class ResolveRequest(BaseModel):
    root_cause: str
    resolution: str
