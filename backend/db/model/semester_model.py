from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class SemesterModel(Base):
    __tablename__ = 'SEMESTER'

    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(255), nullable=False)

    def __init__(self, id, description):
        self.id = id
        self.description = description