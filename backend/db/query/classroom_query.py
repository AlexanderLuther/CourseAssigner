from backend.db.connection.database_connection import DatabaseSession
from backend.db.model.classroom_model import ClassroomModel

class ClassroomQuery:

    def save_classroom(self, classroom: ClassroomModel):
        with DatabaseSession.get_session() as session:
            session.add(classroom)
            session.commit()

    def update_classroom(self, classroom: ClassroomModel):
        with DatabaseSession.get_session() as session:
            session.merge(classroom)
            session.commit()

    def find_classroom_by_description(self, description: str):
        with DatabaseSession.get_session() as session:
            return (
                session.query(ClassroomModel)
                .filter(ClassroomModel.description == description)
                .first()
            )

    def find_all_classrooms(self):
        with DatabaseSession.get_session() as session:
            return session.query(ClassroomModel).all()

    def delete_classroom(self, id: int):
        with DatabaseSession.get_session() as session:
            session.query(ClassroomModel).filter(ClassroomModel.id == id).delete()
            session.commit()
