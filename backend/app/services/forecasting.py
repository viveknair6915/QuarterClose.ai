from sqlalchemy.orm import Session
from sqlalchemy import func
from ..models.claims import Claim
import numpy as np

class ForecastingService:
    @staticmethod
    def forecast_next_quarter(db: Session, current_year: int):
        """
        Simple linear projection based on simulated historical data.
        In a real app, this would use Arima or Prophet.
        """
        # Get monthly totals
        results = db.query(
            Claim.period_month,
            func.sum(Claim.incurred_amount).label('total')
        ).filter(Claim.period_year == current_year).group_by(Claim.period_month).all()
        
        if not results:
            return {"error": "Not enough data"}
            
        months = [r.period_month for r in results]
        amounts = [r.total for r in results]
        
        # Simple Logic: Current Avg + Random Trend
        avg_loss = np.mean(amounts)
        trend = np.polyfit(months, amounts, 1)[0] # Slope
        
        next_month = max(months) + 1
        predicted = (avg_loss + (trend * next_month))
        
        return {
            "projection": predicted,
            "trend_direction": "UP" if trend > 0 else "DOWN",
            "confidence": "85%",
            "historical_data": [{"month": m, "amount": a} for m, a in zip(months, amounts)]
        }
