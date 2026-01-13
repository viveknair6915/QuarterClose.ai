from sqlalchemy.orm import Session
from datetime import date
from ..models.periods import AccountingPeriod
from .audit import AuditService

class ClosingService:
    @staticmethod
    def close_period(db: Session, year: int, quarter: int, user_id: str):
        # Check if already closed
        period = db.query(AccountingPeriod).filter_by(year=year, quarter=quarter).first()
        if not period:
            period = AccountingPeriod(year=year, quarter=quarter, month=quarter*3) # Approx month
            db.add(period)
        
        if period.is_closed:
            raise ValueError("Period already closed")
            
        period.is_closed = True
        period.closed_at = date.today()
        period.closed_by = user_id
        db.commit()
        
        AuditService.log_action(db, "CLOSE", "Quarter", {"year": year, "quarter": quarter}, user_id)
        return {"status": "closed", "period": f"{year}Q{quarter}"}
    
    @staticmethod
    def is_period_closed(db: Session, year: int, quarter: int):
        period = db.query(AccountingPeriod).filter_by(year=year, quarter=quarter).first()
        return period.is_closed if period else False
