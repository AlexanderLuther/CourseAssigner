from sqlalchemy import Column, String, Time
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class TeacherModel(Base):
    __tablename__ = 'TEACHER'

    id = Column(String(10), primary_key=True, autoincrement=False)
    name = Column(String(255), nullable=False)
    entry_time = Column(Time, nullable=False)
    departure_time = Column(Time, nullable=False)

    def __init__(self, id, name, entry_time, departure_time):
        self.id = id
        self.name = name
        self.entry_time = entry_time
        self.departure_time = departure_time