from backend.db.connection.database_connection import DatabaseSession
from backend.db.model.course_type_model import CourseTypeModel

class CourseTypeQuery:
    def find_all_course_types(self):
        with DatabaseSession.get_session() as session:
            return session.query(CourseTypeModel).all()
