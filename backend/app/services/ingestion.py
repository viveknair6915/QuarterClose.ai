import pandas as pd
from sqlalchemy.orm import Session
from ..models.claims import Claim
from ..models.premiums import Premium
from ..utils.logging import get_logger
from .audit import AuditService

logger = get_logger(__name__)

class IngestionService:
    @staticmethod
    def process_claims_file(db: Session, file_content: bytes, filename: str, period_year: int, period_quarter: int):
        logger.info(f"Processing claims file: {filename}")
        
        try:
            if filename.endswith(".csv"):
                df = pd.read_csv(pd.io.common.BytesIO(file_content))
            else:
                df = pd.read_excel(pd.io.common.BytesIO(file_content))
            
            # Basic validation
            required_cols = ['claim_id', 'policy_id', 'incurred_amount', 'segment']
            missing = [col for col in required_cols if col not in df.columns]
            if missing:
                raise ValueError(f"Missing required columns: {missing}")

            records_count = 0
            for _, row in df.iterrows():
                # Upsert logic (simple deletion of existing for this period/file could be better but basic upsert here)
                # For quarter close, usually we replace data for the open period.
                
                # Check duplication based on claim_id
                existing = db.query(Claim).filter(Claim.claim_id == str(row['claim_id'])).first()
                if existing:
                    # Update existing
                    existing.incurred_amount = row.get('incurred_amount', 0)
                    existing.paid_amount = row.get('paid_amount', 0)
                    existing.outstanding_amount = row.get('outstanding_amount', 0)
                    existing.status = row.get('status', 'Open')
                else:
                    claim = Claim(
                        claim_id=str(row['claim_id']),
                        policy_id=str(row.get('policy_id', '')),
                        date_of_loss=pd.to_datetime(row.get('date_of_loss')).date() if not pd.isna(row.get('date_of_loss')) else None,
                        report_date=pd.to_datetime(row.get('report_date')).date() if not pd.isna(row.get('report_date')) else None,
                        segment=row.get('segment'),
                        product_line=row.get('product_line'),
                        incurred_amount=row.get('incurred_amount', 0),
                        paid_amount=row.get('paid_amount', 0),
                        outstanding_amount=row.get('outstanding_amount', 0),
                        status=row.get('status', 'Open'),
                        period_year=period_year,
                        period_quarter=period_quarter,
                        period_month=row.get('period_month', 1), # Default to 1 if missing
                        is_large_loss="NO", # Default, logic elsewhere will update this
                        latitude=row.get('latitude'),
                        longitude=row.get('longitude')
                    )
                    db.add(claim)
                records_count += 1
            
            db.commit()
            
            AuditService.log_action(db, "UPLOAD", "Claims", {"filename": filename, "records": records_count, "period": f"{period_year}Q{period_quarter}"})
            return {"status": "success", "processed": records_count}

        except Exception as e:
            db.rollback()
            logger.error(f"Ingestion failed: {str(e)}")
            raise e
