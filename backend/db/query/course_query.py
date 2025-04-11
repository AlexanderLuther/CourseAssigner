from backend.db.connection.database_connection import DatabaseSession
from backend.db.model.course_model import CourseModel

class CourseQuery:

    def save_course(self, course: CourseModel):
        with DatabaseSession.get_session() as session:
            session.add(course)
            session.commit()

    def update_course(self, course: CourseModel):
        with DatabaseSession.get_session() as session:
            session.merge(course)
            session.commit()

    def find_course_by_code(self, code: str):
        with DatabaseSession.get_session() as session:
            return (
                session.query(CourseModel)
                .filter(CourseModel.code == code)
                .first()
            )

    def find_all_courses(self):
        with DatabaseSession.get_session() as session:
            return session.query(CourseModel).all()

    def delete_course(self, code: str):
        with DatabaseSession.get_session() as session:
            session.query(CourseModel).filter(CourseModel.code == code).delete()
            session.commit()
