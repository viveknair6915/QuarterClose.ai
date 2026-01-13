from sqlalchemy.orm import Session
from sqlalchemy import func
from ..models.claims import Claim
from ..schemas.reports import AvEResult, LossRatioMetric, LargeLossItem
import pandas as pd

class CalculationService:
    @staticmethod
    def identify_large_losses(db: Session, threshold: float = 100000.0):
        """
        Flag claims exceeding the large loss threshold.
        """
        claims = db.query(Claim).filter(Claim.incurred_amount > threshold).all()
        for claim in claims:
            claim.is_large_loss = "YES"
        db.commit()
        return [LargeLossItem(claim_id=c.claim_id, incurred_amount=c.incurred_amount, segment=c.segment) for c in claims]

    @staticmethod
    def calculate_loss_ratios(db: Session, year: int, quarter: int):
        """
        Compute loss ratios by segment.
        """
        # Simplified: Sum incurred / Sum premiums (mocking premiums for now if not joined)
        # In a real system, we'd join with the Premium table.
        results = db.query(
            Claim.segment,
            Claim.product_line,
            func.sum(Claim.incurred_amount).label('total_incurred')
        ).filter(
            Claim.period_year == year,
            Claim.period_quarter == quarter
        ).group_by(Claim.segment, Claim.product_line).all()
        
        metrics = []
        for r in results:
            # Mock earned premium for demonstration to avoid div by zero if no premium data
            earned_premium = 1000000.0 
            loss_ratio = r.total_incurred / earned_premium
            metrics.append(LossRatioMetric(
                segment=r.segment,
                product_line=r.product_line,
                incurred_loss=r.total_incurred,
                earned_premium=earned_premium,
                loss_ratio=loss_ratio
            ))
        return metrics

    @staticmethod
    def actual_vs_expected(db: Session, year: int):
        """
        Compare actuals vs expected (using a simple flat expected loss ratio assumption).
        """
        # Assumption: Expected Loss Ratio = 60%
        EXPECTED_LR = 0.60
        
        actuals = db.query(
            Claim.segment,
            func.sum(Claim.incurred_amount).label('total_incurred')
        ).filter(Claim.period_year == year).group_by(Claim.segment).all()
        
        comparison = []
        for r in actuals:
            # Mock premium again
            premium = 5000000.0 
            expected_loss = premium * EXPECTED_LR
            variance = r.total_incurred - expected_loss
            pct = (variance / expected_loss) * 100
            
            comparison.append(AvEResult(
                segment=r.segment or "Unknown",
                actual_loss=r.total_incurred or 0.0,
                expected_loss=expected_loss,
                variance=variance,
                variance_pct=pct
            ))
        return comparison
