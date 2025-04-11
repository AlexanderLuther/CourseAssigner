from backend.db.connection.database_connection import DatabaseSession
from backend.db.model.semester_model import SemesterModel

class SemesterQuery:
    def find_all_semesters(self):
        with DatabaseSession.get_session() as session:
            return session.query(SemesterModel).all()
