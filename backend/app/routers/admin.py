from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..services.closing import ClosingService
from ..models.audit import AuditLog

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.post("/close-period")
def close_period(year: int, quarter: int, user_id: str = "admin", db: Session = Depends(get_db)):
    try:
        return ClosingService.close_period(db, year, quarter, user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/audit-log")
def get_audit_log(db: Session = Depends(get_db)):
    return db.query(AuditLog).order_by(AuditLog.timestamp.desc()).limit(100).all()
