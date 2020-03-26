from sqlalchemy import (
    Integer,
    Column,
    Text,
    DateTime,
)

from .meta import Base

class KPI(Base):
    __tablename__ = 'kpi'
    kpi_id = Column(Integer, primary_key=True)
    kpi_name = Column(Text, nullable = False)
    report_id = Column(Integer, nullable = False)
    value = Column(Integer, nullable = False)
    target = Column(Integer, nullable = False)