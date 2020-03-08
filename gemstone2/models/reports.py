from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    DateTime
)

from .meta import Base


class Report(Base):
    __tablename__ = 'reports'
    id = Column(Integer, primary_key=True)
    company = Column(Text, nullable=False)
    quarter = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)
    
    highlights = Column(Text)
    operation = Column(Text)
    strategy = Column(Text)
    customer_gained = Column(Text)
    orders = Column(Text)
    
    revenue = Column(Integer)
    profit = Column(Integer)
    EBITDA = Column(Integer)
    cash_flow = Column(Integer)
    
    explain = Column(Text)

    last_updated = Column(DateTime)


Index('my_index', Report.year.desc(), Report.quarter.desc(), unique=False)
