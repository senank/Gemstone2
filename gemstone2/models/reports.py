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
    
    revenue_1 = Column(Text)
    revenue_2= Column(Text)
    revenue_3 = Column(Text)
    revenue_4 = Column(Text)
    revenue_YTD = Column(Text)
    revenue_FY = Column(Text)
    revenue_plan = Column(Text)

    profit_1 = Column(Text)
    profit_2= Column(Text)
    profit_3 = Column(Text)
    profit_4 = Column(Text)
    profit_YTD = Column(Text)
    profit_FY = Column(Text)
    profit_plan = Column(Text)

    EBITDA_1 = Column(Text)
    EBITDA_2= Column(Text)
    EBITDA_3 = Column(Text)
    EBITDA_4 = Column(Text)
    EBITDA_YTD = Column(Text)
    EBITDA_FY = Column(Text)
    EBITDA_plan = Column(Text)
    
    cf_1 = Column(Text)
    cf_2= Column(Text)
    cf_3 = Column(Text)
    cf_4 = Column(Text)
    cf_YTD = Column(Text)
    cf_FY = Column(Text)
    cf_plan = Column(Text)
    
    explain = Column(Text)

    last_updated = Column(DateTime)

    filename = Column(Text)
    unique_filename = Column(Text)

    published = Column(Boolean, nullable=False, default=False, server_default=u'false')


Index('my_index', Report.year.desc(), Report.quarter.desc(), unique=False)
