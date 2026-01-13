from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey
from sqlalchemy.sql import func
from .base import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(String, default="system")
    action_type = Column(String)  # UPLOAD, CLOSE, EDIT, EXPORT
    entity_affected = Column(String) # Table name or component
    details = Column(JSON) # Store before/after or specific parameters
