from sqlalchemy import Column, Integer, Time, String
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class PeriodModel(Base):
    __tablename__ = 'PERIOD'

    id = Column(Integer, primary_key=True, autoincrement=True)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    description = Column(String(255), nullable=False)