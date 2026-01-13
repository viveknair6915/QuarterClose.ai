from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..services.ingestion import IngestionService
from ..services.closing import ClosingService

router = APIRouter(prefix="/data", tags=["Data"])

@router.post("/upload/claims")
async def upload_claims(
    year: int,
    quarter: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Check if period is closed
    if ClosingService.is_period_closed(db, year, quarter):
        raise HTTPException(status_code=400, detail="Quarter is closed for data entry")
    
    content = await file.read()
    return IngestionService.process_claims_file(db, content, file.filename, year, quarter)
