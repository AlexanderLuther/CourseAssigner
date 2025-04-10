from backend.db.connection.database_connection import DatabaseSession
from backend.db.model.course_type_model import CourseTypeModel

class CourseTypeQuery:
    def __init__(self):
        self.db_session = DatabaseSession.get_session()

    def find_all_course_types(self):
        return (
            self.db_session
                .query(CourseTypeModel)
                .all()
        )