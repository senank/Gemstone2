from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    Boolean,
    DateTime
)

from .meta import Base


class Report(Base):
    __tablename__ = 'reports'
    id = Column(Integer, primary_key=True)
    company = Column(Text, nullable=False)
    quarter = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)
    
    highlight = Column(Text)
    operation = Column(Text)
    strategy = Column(Text)
    customer_gained = Column(Text)
    order = Column(Text)
    
    revenue_1 = Column(Integer)
    revenue_2= Column(Integer)
    revenue_3 = Column(Integer)
    revenue_4 = Column(Integer)
    revenue_YTD = Column(Integer)
    revenue_FY = Column(Integer)
    revenue_plan = Column(Integer)

    profit_1 = Column(Integer)
    profit_2= Column(Integer)
    profit_3 = Column(Integer)
    profit_4 = Column(Integer)
    profit_YTD = Column(Integer)
    profit_FY = Column(Integer)
    profit_plan = Column(Integer)

    EBITDA_1 = Column(Integer)
    EBITDA_2= Column(Integer)
    EBITDA_3 = Column(Integer)
    EBITDA_4 = Column(Integer)
    EBITDA_YTD = Column(Integer)
    EBITDA_FY = Column(Integer)
    EBITDA_plan = Column(Integer)
    
    cf_1 = Column(Integer)
    cf_2= Column(Integer)
    cf_3 = Column(Integer)
    cf_4 = Column(Integer)
    cf_YTD = Column(Integer)
    cf_FY = Column(Integer)
    cf_plan = Column(Integer)
    
    explain = Column(Text)

    last_updated = Column(DateTime)

    filename = Column(Text)
    unique_filename = Column(Text)

    published = Column(Boolean, nullable=False, default=False, server_default=u'false')


Index('my_index', Report.year.desc(), Report.quarter.desc(), unique=False)
