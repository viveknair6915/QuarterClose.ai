from sqlalchemy.orm import Session
from ..models.audit import AuditLog
from ..schemas.base import AuditCreate
import json

class AuditService:
    @staticmethod
    def log_action(db: Session, action_type: str, entity: str, details: dict, user_id: str = "system"):
        audit_entry = AuditLog(
            action_type=action_type,
            entity_affected=entity,
            details=details, # SQLAlchemy JSON type handles dict automatically
            user_id=user_id
        )
        db.add(audit_entry)
        db.commit()
        db.refresh(audit_entry)
        return audit_entry
