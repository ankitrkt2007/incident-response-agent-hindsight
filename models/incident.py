from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from app.models.db import Base

class Incident(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    service = Column(String(255), nullable=False)
    severity = Column(String(50), nullable=False)
    symptoms = Column(Text, nullable=False)
    logs = Column(Text, nullable=True)

    status = Column(String(50), default="open")
    root_cause = Column(Text, nullable=True)
    resolution = Column(Text, nullable=True)
    latest_diagnosis = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)
