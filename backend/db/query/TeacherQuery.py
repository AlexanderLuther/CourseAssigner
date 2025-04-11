from backend.db.connection.database_connection import DatabaseSession
from backend.db.model.teacher_model import TeacherModel

class TeacherQuery:

    def save_teacher(self, teacher: TeacherModel):
        with DatabaseSession.get_session() as session:
            session.add(teacher)
            session.commit()

    def find_teacher_by_id(self, id: str):
        with DatabaseSession.get_session() as session:
            return (
                session.query(TeacherModel)
                .filter(TeacherModel.id == id)
                .first()
            )

    def find_all_teachers(self):
        with DatabaseSession.get_session() as session:
            return session.query(TeacherModel).all()

    def update_teacher(self, teacher: TeacherModel):
        with DatabaseSession.get_session() as session:
            session.merge(teacher)
            session.commit()

    def delete_teacher(self, id: str):
        with DatabaseSession.get_session() as session:
            session.query(TeacherModel).filter(TeacherModel.id == id).delete()
            session.commit()
