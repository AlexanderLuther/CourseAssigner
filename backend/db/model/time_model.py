from sqlalchemy import Column, Integer, Time
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class TimeModel(Base):
    __tablename__ = 'TIME'

    id = Column(Integer, primary_key=True, autoincrement=True)
    time = Column(Time, nullable=False)