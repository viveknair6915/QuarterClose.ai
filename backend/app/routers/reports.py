from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..services.calculations import CalculationService
from ..services.controls import ControlService
from ..schemas.reports import AvEResult, LargeLossItem

router = APIRouter(prefix="/reports", tags=["Reports"])

@router.get("/large-loss", response_model=List[LargeLossItem])
def get_large_losses(db: Session = Depends(get_db)):
    # Trigger identification first (could be background job in prod)
    CalculationService.identify_large_losses(db) 
    return CalculationService.identify_large_losses(db)

@router.get("/ave/{year}", response_model=List[AvEResult])
def get_ave_analysis(year: int, db: Session = Depends(get_db)):
    return CalculationService.actual_vs_expected(db, year)

@router.get("/controls")
def get_controls_status(db: Session = Depends(get_db)):
    return ControlService.run_checks(db)

@router.get("/cashflow/{year}")
def get_cashflow_analysis(year: int, db: Session = Depends(get_db)):
    from ..services.cashflow import CashflowService
    return CashflowService.analyze_cashflow(db, year)

@router.get("/forecast/{year}")
def get_forecast(year: int, db: Session = Depends(get_db)):
    from ..services.forecasting import ForecastingService
    return ForecastingService.forecast_next_quarter(db, year)

@router.get("/geo-data")
def get_geo_data(db: Session = Depends(get_db)):
    from ..models.claims import Claim
    # Return lat/lon for all open claims
    results = db.query(Claim.claim_id, Claim.latitude, Claim.longitude, Claim.incurred_amount).filter(Claim.latitude != None).limit(1000).all()
    
    return [
        {
            "claim_id": r.claim_id,
            "lat": r.latitude,
            "lon": r.longitude,
            "amount": r.incurred_amount
        }
        for r in results
    ]
