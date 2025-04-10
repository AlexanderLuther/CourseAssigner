from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class CourseModel(Base):
    __tablename__ = 'COURSE'

    code = Column(String(10), primary_key=True, autoincrement=False)
    name = Column(String(255), nullable=False)
    id_career = Column(Integer, nullable=False)
    id_semester = Column(Integer, nullable=False)
    id_section = Column(Integer, nullable=False)
    id_course_type = Column(Integer, nullable=False)

    def __init__(self, code, name, id_career, id_semester, id_section, id_course_type):
        self.code = code
        self.name = name
        self.id_career = id_career
        self.id_semester = id_semester
        self.id_section = id_section
        self.id_course_type = id_course_type
