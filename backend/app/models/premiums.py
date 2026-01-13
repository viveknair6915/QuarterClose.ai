from sqlalchemy import Column, Integer, String, Float, Date
from .base import Base, TimestampMixin

class Premium(Base, TimestampMixin):
    __tablename__ = "premiums"

    id = Column(Integer, primary_key=True, index=True)
    policy_id = Column(String, index=True)
    
    segment = Column(String)
    product_line = Column(String)
    
    written_premium = Column(Float)
    earned_premium = Column(Float)
    
    period_year = Column(Integer)
    period_month = Column(Integer)
    period_quarter = Column(Integer)
    
    currency = Column(String, default="USD")
