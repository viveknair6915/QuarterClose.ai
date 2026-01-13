from sqlalchemy import Column, Integer, String, Boolean, Date
from .base import Base, TimestampMixin

class AccountingPeriod(Base, TimestampMixin):
    __tablename__ = "accounting_periods"

    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer)
    quarter = Column(Integer)
    month = Column(Integer)
    
    is_closed = Column(Boolean, default=False)
    closed_at = Column(Date, nullable=True)
    closed_by = Column(String, nullable=True)
