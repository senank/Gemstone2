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
    
    # for better looking edit form
    # highlights = Column(Text)
    # operation = Column(Text)
    # strategy = Column(Text)
    # customer_gained = Column(Text)
    # orders = Column(Text)
    
    highlight1 = Column(Text)
    highlight2 = Column(Text)
    highlight3 = Column(Text)
    highlight4 = Column(Text)
    highlight5 = Column(Text)
    highlight6 = Column(Text)
    highlight7 = Column(Text)
    highlight8 = Column(Text)
    highlight9 = Column(Text)

    operation1 = Column(Text)
    operation2 = Column(Text)
    operation3 = Column(Text)
    operation4 = Column(Text)
    operation5 = Column(Text)
    operation6 = Column(Text)
    operation7 = Column(Text)
    operation8 = Column(Text)
    operation9 = Column(Text)

    strategy1 = Column(Text)
    strategy2 = Column(Text)
    strategy3 = Column(Text)
    strategy4 = Column(Text)
    strategy5 = Column(Text)
    strategy6 = Column(Text)
    strategy7 = Column(Text)
    strategy8 = Column(Text)
    strategy9 = Column(Text)
    
    customer_gained1 = Column(Text)
    customer_gained2 = Column(Text)
    customer_gained3 = Column(Text)
    customer_gained4 = Column(Text)
    customer_gained5 = Column(Text)
    customer_gained6 = Column(Text)
    customer_gained7 = Column(Text)
    customer_gained8 = Column(Text)
    customer_gained9 = Column(Text)
    
    order1 = Column(Text)
    order2 = Column(Text)
    order3 = Column(Text)
    order4 = Column(Text)
    order5 = Column(Text)
    order6 = Column(Text)
    order7 = Column(Text)
    order8 = Column(Text)
    order9 = Column(Text)

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
