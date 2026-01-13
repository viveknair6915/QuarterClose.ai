from sqlalchemy.orm import Session
from sqlalchemy import func
from ..models.claims import Claim

class ControlService:
    @staticmethod
    def run_checks(db: Session):
        checks = {
            "negative_incurred": 0,
            "missing_segment": 0,
            "future_dates": 0,
            "status": "GREEN"
        }
        
        # Check 1: Negative Incurred
        neg_count = db.query(Claim).filter(Claim.incurred_amount < 0).count()
        checks["negative_incurred"] = neg_count
        
        # Check 2: Missing Segment
        missing_seg = db.query(Claim).filter((Claim.segment == None) | (Claim.segment == "")).count()
        checks["missing_segment"] = missing_seg
        
        # Status Logic
        if neg_count > 0 or missing_seg > 0:
            checks["status"] = "RED" if (neg_count + missing_seg) > 10 else "YELLOW"
            
        return checks
