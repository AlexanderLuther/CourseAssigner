from backend.db.connection.database_connection import DatabaseSession
from backend.db.model.semester_model import SemesterModel

class SemesterQuery:
    def __init__(self):
        self.db_session = DatabaseSession.get_session()

    def find_all_semesters(self):
        return (
            self.db_session
                .query(SemesterModel)
                .all()
        )