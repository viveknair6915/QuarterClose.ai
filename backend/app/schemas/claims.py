from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

class ClaimBase(BaseModel):
    claim_id: str
    policy_id: str
    date_of_loss: date
    report_date: date
    segment: str
    product_line: str
    incurred_amount: float
    paid_amount: float
    outstanding_amount: float
    status: str
    is_large_loss: str = "NO"

class ClaimCreate(ClaimBase):
    period_year: int
    period_month: int
    period_quarter: int

class ClaimResponse(ClaimCreate):
    id: int

    class Config:
        orm_mode = True
