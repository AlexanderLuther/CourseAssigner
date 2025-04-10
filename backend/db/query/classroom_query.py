from backend.db.connection.database_connection import DatabaseSession
from backend.db.model.classroom_model import ClassroomModel

class ClassroomQuery:

    def __init__(self):
        self.db_session = DatabaseSession.get_session()

    def save_classroom(self, classroom: ClassroomModel):
        self.db_session.add(classroom)
        self.db_session.commit()
        pass

    def update_classroom(self, classroom: ClassroomModel):
        self.db_session.merge(classroom)
        self.db_session.commit()

    def find_classroom_by_description(self, description: str):
        return (
            self.db_session
                .query(ClassroomModel)
                .filter(ClassroomModel.description == description)
                .first()
        )

    def find_all_classrooms(self):
        return (
            self.db_session
                .query(ClassroomModel)
                .all()
        )

    def delete_classroom(self, id: int):
        self.db_session.query(ClassroomModel).filter(ClassroomModel.id == id).delete()
        self.db_session.commit()