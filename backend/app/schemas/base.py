from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AuditBase(BaseModel):
    pass

class AuditCreate(AuditBase):
    action_type: str
    entity_affected: str
    details: dict
    user_id: str

class AuditResponse(AuditCreate):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True
