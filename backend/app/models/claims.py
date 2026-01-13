from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from .base import Base, TimestampMixin

class Claim(Base, TimestampMixin):
    __tablename__ = "claims"

    id = Column(Integer, primary_key=True, index=True)
    claim_id = Column(String, unique=True, index=True)
    policy_id = Column(String, index=True)
    date_of_loss = Column(Date)
    report_date = Column(Date)
    
    segment = Column(String)  # e.g., Property, Casualty, Marine
    product_line = Column(String)
    
    incurred_amount = Column(Float)
    paid_amount = Column(Float)
    outstanding_amount = Column(Float)
    
    currency = Column(String, default="USD")
    status = Column(String)  # Open, Closed, Reopened
    
    period_year = Column(Integer)
    period_month = Column(Integer)
    period_quarter = Column(Integer)
    
    is_large_loss = Column(String) # YES/NO flag (using String to be explicit, or could be Boolean)
    
    # Location
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    
    # Audit fields
    data_version = Column(Integer, default=1)
