from backend.db.connection.database_connection import DatabaseSession
from backend.db.model.TeacherModel import TeacherModel

class TeacherQuery:
    def __init__(self):
        self.db_session = DatabaseSession.get_session()

    def save_teacher(self, teacher: TeacherModel):
        self.db_session.add(teacher)
        self.db_session.commit()

    def find_teacher_by_id(self, id: str):
        return (
            self.db_session
                .query(TeacherModel)
                .filter(TeacherModel.id == id)
                .first()
        )

    def find_all_teachers(self):
        return (
            self.db_session
                .query(TeacherModel)
                .all()
        )

    def update_teacher(self, teacher: TeacherModel):
        self.db_session.merge(teacher)
        self.db_session.commit()

    def delete_teacher(self, id: str):
        self.db_session.query(TeacherModel).filter(TeacherModel.id == id).delete()
        self.db_session.commit()