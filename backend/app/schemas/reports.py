from pydantic import BaseModel
from typing import List, Optional

class LossRatioMetric(BaseModel):
    segment: str
    product_line: str
    incurred_loss: float
    earned_premium: float
    loss_ratio: float

class LargeLossItem(BaseModel):
    claim_id: str
    incurred_amount: float
    description: str = "Large Loss Event"
    segment: str

class AvEResult(BaseModel):
    segment: str
    actual_loss: float
    expected_loss: float
    variance: float
    variance_pct: float
