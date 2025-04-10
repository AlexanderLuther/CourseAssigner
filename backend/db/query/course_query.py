from backend.db.connection.database_connection import DatabaseSession
from backend.db.model.course_model import CourseModel

class CourseQuery:

    def __init__(self):
        self.db_session = DatabaseSession.get_session()

    def save_course(self, course: CourseModel):
        self.db_session.add(course)
        self.db_session.commit()
        pass

    def update_course(self, course: CourseModel):
        self.db_session.merge(course)
        self.db_session.commit()

    def find_course_by_code(self, code: str):
        return (
            self.db_session
                .query(CourseModel)
                .filter(CourseModel.code == code)
                .first()
        )

    def find_all_courses(self):
        return (
            self.db_session
                .query(CourseModel)
                .all()
        )

    def delete_course(self, code: str):
        self.db_session.query(CourseModel).filter(CourseModel.code == code).delete()
        self.db_session.commit()